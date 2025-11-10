# PostgreSQL CRUD 

## Overview
This repo demonstrates a PostgreSQL-backed application performing CRUD (Create, Read, Update, Delete) on a `students` table. The Python app uses `psycopg2` to connect and run operations.

## Prerequisites
- PostgreSQL 13+ installed and running
- Python 3.10+
- (Optional) pgAdmin for visual verification

## Setup

### 1 Create database and table
1. **Create a database** (e.g., `school_db`) in psql or pgAdmin.
2. **Run the schema script**:
   ```bash
   psql -h localhost -U your_user -d school_db -f db/schema.sql
