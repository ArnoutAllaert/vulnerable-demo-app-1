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
    query = (
        f"SELECT id, email, created_at "
        f"FROM accounts "
        f"WHERE email = '{email}' AND status = '{status}';"
    )
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()


if __name__ == "__main__":
    user_email = input("Email to lookup: ")
    rows = find_accounts_by_email(user_email)
    for r in rows:
        print(r)
