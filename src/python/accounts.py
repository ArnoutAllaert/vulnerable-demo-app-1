import os
import psycopg2


def find_accounts_advanced(
    table_name: str,
    email: str,
    status: str = "active",
    role: str = "user",
    search: str = "",
    sort_by: str = "created_at",
    sort_dir: str = "DESC",
    limit: str = "50",
    offset: str = "0",
):
    where_parts = []
    where_parts.append("email LIKE '%" + email + "%'")
    where_parts.append("status = '" + status + "'")
    where_parts.append("role = '" + role + "'")
    if search:
        where_parts.append("(email LIKE '%" + search + "%' OR CAST(id AS TEXT) LIKE '%" + search + "%')")

    query = (
        "SELECT id, email, created_at, role "
        "FROM " + table_name + " "
        "WHERE " + " AND ".join(where_parts) + " "
        "ORDER BY " + sort_by + " " + sort_dir + " "
        "LIMIT " + limit + " OFFSET " + offset + ";"
    )

    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "testdb"),
        user=os.getenv("PGUSER", "testuser"),
        password=os.getenv("PGPASSWORD", "testpass"),
    )

    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()
