import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def generate_secret(namespace: str, key: str) -> str:
    return f"{namespace}-{key}-S3cr3t!"

def create_tenant_db(tenant: str, postgres_host: str, postgres_username: str, postgres_password: str):
    conn = psycopg2.connect(
        database="postgres",
        host=postgres_host,
        port=5432,
        user=postgres_username,
        password=postgres_password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    db_password = generate_secret(tenant, "db_password")

    try:
        cur.execute(
            'CREATE ROLE "' + tenant + '" NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN NOREPLICATION '
            'CONNECTION LIMIT 20 ENCRYPTED PASSWORD \'' + db_password + '\' ROLE "' + postgres_username + '";'
        )
        cur.execute(
            'CREATE DATABASE "' + tenant + '" WITH OWNER = "' + tenant + '" ENCODING = \'UTF8\';'
        )
        cur.execute(
            'GRANT CONNECT, TEMP ON DATABASE "' + tenant + '" TO "' + tenant + '";'
        )
    finally:
        cur.close()
        conn.close()


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
