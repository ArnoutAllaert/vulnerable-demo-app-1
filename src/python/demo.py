# src/python/demo.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_queue_mode_db(k8s_namespace, postgres_host, postgres_username, postgres_password):
    conn = psycopg2.connect(
        database="postgres",
        host=postgres_host,
        port=5432,
        user=postgres_username,
        password=postgres_password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    db_password = generate_queuemode_secret(k8s_namespace, "db_password")

    try:
        cur.execute(
            'CREATE ROLE "' + k8s_namespace + '" NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN NOREPLICATION '
            "CONNECTION LIMIT 20 ENCRYPTED PASSWORD '" + db_password + "' ROLE \"" + postgres_username + '";'
        )
        cur.execute(
            'CREATE DATABASE "' + k8s_namespace + '" WITH OWNER = "' + k8s_namespace + '" ENCODING = \'UTF8\';'
        )
    finally:
        cur.close()
        conn.close()
