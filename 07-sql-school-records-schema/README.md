# School Records SQLite Schema & Queries

A normalized SQLite relational schema for managing students, courses, enrollments, and attendance records, complete with sample seed data and analytical SQL queries.

## Quick Run
```bash
sqlite3 school.db < schema.sql
sqlite3 school.db < seed.sql
sqlite3 -header -column school.db < queries.sql
```
