#!/usr/bin/env python3
"""Minimal JSON task tracker using Python standard library + SQLite."""

import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

DB_PATH = Path(__file__).resolve().with_name("tasks.db")
VALID_STATUSES = {"pending", "in_progress", "completed"}


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.commit()


class TaskHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        if parsed.path == "/tasks":
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                rows = [dict(r) for r in conn.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id DESC")]
            self._send_json(200, {"tasks": rows})
            return
        if parsed.path.startswith("/tasks/"):
            task_id = parsed.path.removeprefix("/tasks/")
            if not task_id.isdigit():
                self._send_json(404, {"error": "Not found"})
                return
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT id, title, status, created_at FROM tasks WHERE id = ?",
                    (int(task_id),),
                ).fetchone()
            if row is None:
                self._send_json(404, {"error": "Task not found"})
                return
            self._send_json(200, dict(row))
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/tasks":
            self._send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
        except (ValueError, OSError):
            self._send_json(400, {"error": "Invalid request body"})
            return
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return
        if not isinstance(data, dict):
            self._send_json(400, {"error": "Request body must be a JSON object"})
            return
        title = str(data.get("title", "")).strip()
        if not title:
            self._send_json(400, {"error": "title is required"})
            return
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
            task_id = cur.lastrowid
        self._send_json(201, {"id": task_id, "title": title, "status": "pending"})

    def do_PATCH(self) -> None:
        parsed = urlparse(self.path)
        prefix = "/tasks/"
        if not parsed.path.startswith(prefix):
            self._send_json(404, {"error": "Not found"})
            return
        task_id_text = parsed.path[len(prefix):]
        if not task_id_text.isdigit():
            self._send_json(404, {"error": "Task not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "Invalid JSON"})
            return
        if not isinstance(data, dict):
            self._send_json(400, {"error": "Request body must be a JSON object"})
            return

        fields: dict[str, object] = {}
        if "title" in data:
            title = str(data["title"]).strip()
            if not title:
                self._send_json(400, {"error": "title is required"})
                return
            fields["title"] = title
        if "status" in data:
            status = str(data["status"]).strip()
            if status not in VALID_STATUSES:
                self._send_json(400, {"error": "status must be pending, in_progress, or completed"})
                return
            fields["status"] = status
        if not fields:
            self._send_json(400, {"error": "Provide title or status"})
            return

        task_id = int(task_id_text)
        assignments = ", ".join(f"{key} = ?" for key in fields)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                f"UPDATE tasks SET {assignments} WHERE id = ?",
                (*fields.values(), task_id),
            )
            conn.commit()
            if cur.rowcount == 0:
                self._send_json(404, {"error": "Task not found"})
                return
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, title, status, created_at FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
        self._send_json(200, dict(row))

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        prefix = "/tasks/"
        if not parsed.path.startswith(prefix):
            self._send_json(404, {"error": "Not found"})
            return
        task_id_text = parsed.path[len(prefix):]
        if not task_id_text.isdigit():
            self._send_json(404, {"error": "Task not found"})
            return
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (int(task_id_text),))
            conn.commit()
        if cur.rowcount == 0:
            self._send_json(404, {"error": "Task not found"})
            return
        self._send_json(200, {"deleted": True, "id": int(task_id_text)})


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8080), TaskHandler)
    print("Task Tracker listening on http://127.0.0.1:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
