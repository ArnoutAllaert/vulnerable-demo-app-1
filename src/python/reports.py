# src/python/reports.py
import os
from google.cloud import bigquery


def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT"))


def purchases_by_country(country: str, min_total: str = "0"):
    query = (
        f"SELECT user_id, SUM(amount) AS total "
        f"FROM `myproj.analytics.purchases` "
        f"WHERE country = '{country}' AND amount >= {min_total} "
        f"GROUP BY user_id "
        f"ORDER BY total DESC"
    )
    client = get_client()
    return list(client.query(query).result())
