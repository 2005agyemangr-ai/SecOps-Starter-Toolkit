#!/usr/bin/env python3
"""Minimal JSON task tracker using Python standard library + SQLite."""

import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

DB_PATH = Path("tasks.db")


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
        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/tasks":
            self._send_json(404, {"error": "Not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
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
