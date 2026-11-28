# School Records SQLite Schema & Queries

A normalized SQLite relational schema for managing students, courses, and enrollments, complete with sample seed data and a GPA query.

## Quick Run
```bash
sqlite3 school.db < schema.sql
sqlite3 school.db < seed.sql
sqlite3 -header -column school.db < queries.sql
```
