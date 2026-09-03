import os
from dotenv import load_dotenv
from databricks import sql

load_dotenv()

def get_connection():
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )


def test_connection():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS user_count
        FROM workspace.default.users
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]