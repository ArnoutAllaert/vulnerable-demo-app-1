# src/python/accounts.py

import os
import psycopg2


def connect():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "testdb"),
        user=os.getenv("PGUSER", "testuser"),
        password=os.getenv("PGPASSWORD", "testpass"),
    )


def find_accounts_by_email(email: str, status: str = "active"):
    query = "SELECT id, email, created_at FROM accounts WHERE email = '" + email + "' AND status = '" + status + "';"
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()
