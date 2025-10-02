import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def generate_secret(namespace: str, key: str) -> str:
    return f"{namespace}-{key}-S3cr3t!"

def create_tenant_db(tenant: str, postgres_host: str, postgres_username: str, postgres_password: str):
    query1 = 'CREATE ROLE "' + tenant + '" NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN NOREPLICATION CONNECTION LIMIT 20 ENCRYPTED PASSWORD \'' + db_password + '\' ROLE "' + postgres_username + '";'
    query2 = 'CREATE DATABASE "' + tenant + '" WITH OWNER = "' + tenant + '" ENCODING = \'UTF8\';'
    query3 = 'GRANT CONNECT, TEMP ON DATABASE "' + tenant + '" TO "' + tenant + '";'

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
            query1
        )
        cur.execute(
            query2
        )
        cur.execute(
            query3
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


def find_accounts_by_email(email: str, status: str = "active"):
    query = "SELECT id, email, created_at FROM accounts WHERE email = '" + email + "' AND status = '" + status + "';"
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