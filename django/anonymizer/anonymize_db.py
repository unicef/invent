import os
import logging
import subprocess

from faker import Faker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Database configuration
SOURCE_DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = 5432

# Create a new database with a unique name
TARGET_DB_NAME = 'postgres_anonymized'

fake = Faker()

try:
    conn = psycopg2.connect(
        dbname=SOURCE_DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
except psycopg2.Error as e:
    logging.error(f"Failed to connect to the source database. More info: {str(e)}")
    raise

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

try:
    # Terminate all connections to the new database
    cursor.execute(f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{TARGET_DB_NAME}';
    """)
    logging.info("Terminated connections to the new database")

    # Drop the new database if it already exists
    cursor.execute(f"DROP DATABASE IF EXISTS {TARGET_DB_NAME};")
    logging.info("Dropped the new database if it already existed")

    # Create the new database
    cursor.execute(f"CREATE DATABASE {TARGET_DB_NAME};")
    logging.info("Created the new database")

except psycopg2.Error as e:
    logging.error(f"Failed to execute a database operation. More info: {str(e)}")
    raise
finally:
    cursor.close()
    conn.close()

try:
    # Copy schema from the original database to the new one
    subprocess.run(
        [
            "pg_dump",
            "--schema-only",
            "-U", DB_USER,
            "-h", DB_HOST,
            "-p", str(DB_PORT),
            "-f", "postgres_dump.sql",
            SOURCE_DB_NAME,
        ],
        check=True,
    )
    logging.info("Dumped schema from the source database")

    subprocess.run(
        [
            "psql",
            "-U", DB_USER,
            "-h", DB_HOST,
            "-p", str(DB_PORT),
            "-d", TARGET_DB_NAME,
            "-f", "postgres_dump.sql",
        ],
        check=True,
    )
    logging.info("Loaded schema to the new database")

except subprocess.CalledProcessError as e:
    logging.error(f"Failed to copy schema. More info: {str(e)}")
    raise
# finally:
#     os.remove("postgres_dump.sql")

try:
    with psycopg2.connect(
        dbname=TARGET_DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as new_conn:
        with new_conn.cursor() as new_cursor, psycopg2.connect(
            dbname=SOURCE_DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ).cursor() as cursor:
            # Define the tables and columns to anonymize
            tables_to_anonymize = {
                'account_emailaddress': ['email'],
                'auth_user': ['username', 'first_name', 'last_name', 'email'],
                'core_newsitem': ['title', 'description', 'description_en', 'description_es', 'description_fr', 'description_pt']
            }

            column_faker_map = {
                'email': 'email',
                'username': 'user_name',
                'first_name': 'first_name',
                'last_name': 'last_name',
            }

            # Anonymize data
            for table, columns in tables_to_anonymize.items():
                try:
                    # Fetch data from the original table
                    cursor.execute(f"SELECT * FROM {table};")
                    rows = cursor.fetchall()

                    # Anonymize sensitive data
                    anonymized_rows = []
                    for row in rows:
                        new_row = list(row)
                        for column in columns:
                            column_index = None
                            for i, desc in enumerate(cursor.description):
                                if desc.name == column:
                                    column_index = i
                                    break
                            if column_index is not None:
                                faker_method = column_faker_map[column]
                                new_row[column_index] = getattr(fake, faker_method)()

                        anonymized_rows.append(new_row)

                    # Insert anonymized data into the new table
                    values_placeholder = ','.join(['%s'] * len(row))
                    new_cursor.executemany(f"INSERT INTO {table} VALUES ({values_placeholder});", anonymized_rows)

                    logging.info(f"Anonymized data in table {table}")

                except psycopg2.Error as e:
                    logging.error(f"Failed to anonymize data in table {table}. More info: {str(e)}")
                    raise

except psycopg2.Error as e:
    logging.error(f"Failed to connect to the new database or execute a database operation. More info: {str(e)}")
    raise
