# Student Task Tracker (Python stdlib HTTP + SQLite)

A zero-dependency JSON REST-style task tracker built with Python's `http.server` and `sqlite3`.

## Run
```bash
python3 app.py
# Test endpoints:
# curl -s http://127.0.0.1:8080/tasks | jq
# curl -s -X POST http://127.0.0.1:8080/tasks -H "Content-Type: application/json" -d '{"title":"Finish INF 215 lab"}'
```
