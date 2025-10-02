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

if __name__ == "__main__":
    tenant = input("Tenant/namespace: ")
    host = os.getenv("PGHOST", "localhost")
    user = os.getenv("PGUSER", "postgres")
    pwd = os.getenv("PGPASSWORD", "postgres")
    create_tenant_db(tenant, host, user, pwd)
    print("Done.")
