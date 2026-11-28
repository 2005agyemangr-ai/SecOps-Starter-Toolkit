import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

import app


class TaskApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        app.DB_PATH = Path(self.temp_dir.name) / "tasks.db"
        app.init_db()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), app.TaskHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp_dir.cleanup()

    def request(self, method: str, path: str, payload: dict | None = None):
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_create_get_patch_delete(self) -> None:
        status, created = self.request("POST", "/tasks", {"title": "Complete toolkit"})
        self.assertEqual(status, 201)

        status, fetched = self.request("GET", f"/tasks/{created['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(fetched["title"], "Complete toolkit")

        status, updated = self.request("PATCH", f"/tasks/{created['id']}", {"status": "completed"})
        self.assertEqual(status, 200)
        self.assertEqual(updated["status"], "completed")

        status, deleted = self.request("DELETE", f"/tasks/{created['id']}")
        self.assertEqual(status, 200)
        self.assertTrue(deleted["deleted"])


if __name__ == "__main__":
    unittest.main()
