# src/python/users.py
import os
import psycopg2


def _get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "testdb"),
        user=os.getenv("PGUSER", "testuser"),
        password=os.getenv("PGPASSWORD", "testpass"),
    )


def get_user_by_username(username: str):
    query = "SELECT id, username, email FROM users WHERE username = '" + username + "';"
    con =  _get_connection()
    cur = con.cursor()
    try:
        cur.execute(query)
        return cur.fetchall()
    finally:
        con.close()


if __name__ == "__main__":
    name = input("Username to search: ")
    try:
        for row in get_user_by_username(name):
            print(row)
    except Exception as e:
        print("Error:", e)
