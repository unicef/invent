# anonymize_db.py
import logging
import subprocess

import psycopg2
import psycopg2.extras
from psycopg2.extras import Json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import register_adapter, AsIs
import json
from tqdm import tqdm


# parameters
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "30011"
SOURCE_DB = "postgres"
TARGET_DB = "postgres_limited"
DUMP_FILE = "dump_anon.sql"


def adapt_dict(d):
    return AsIs(f"'{json.dumps(d)}'::jsonb")


register_adapter(dict, adapt_dict)


def limit_rows_db(source_db_name, db_user, db_password, db_host, db_port, target_db_name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    try:
        conn = psycopg2.connect(
            dbname=source_db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except psycopg2.Error as e:
        logging.error(
            f"Failed to connect to the source database. More info: {str(e)}")
        raise

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        # Terminate all connections to the new database
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{target_db_name}';
        """)
        logging.info("Terminated connections to the new database")

        # Drop the new database if it already exists
        cursor.execute(f"DROP DATABASE IF EXISTS {target_db_name};")
        logging.info("Dropped the new database if it already existed")

        # Create the new database
        cursor.execute(f"CREATE DATABASE {target_db_name};")
        logging.info("Created the new database")

    except psycopg2.Error as e:
        logging.error(
            f"Failed to execute a database operation. More info: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

    # Copy schema from the original database to the new one
    copy_schema_from_source_to_target(
        db_user, db_host, db_port, source_db_name, target_db_name)

    with psycopg2.connect(
        dbname=target_db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    ) as new_conn:
        with new_conn.cursor() as new_cursor, psycopg2.connect(
            dbname=source_db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        ).cursor() as cursor:
            # Fetch the list of tables in the database
            cursor.execute(
                """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'""")
            tables = cursor.fetchall()

            for table in tables:
                table = table[0]
                # Get first 100 rows from the table
                cursor.execute(f'SELECT * FROM "{table}" LIMIT 100;')
                rows = cursor.fetchall()
                if rows:
                    # Get the column names
                    column_names = [desc[0] for desc in cursor.description]
                    # Insert data into the new table
                    columns_placeholder = ', '.join(
                        [f'"{col}"' for col in column_names])
                    values_placeholder = ', '.join(['%s'] * len(rows[0]))

                    # Prepare the rows by converting dicts to JSON
                    prepared_rows = []
                    for row in rows:
                        new_row = []
                        for item in row:
                            if isinstance(item, dict):
                                try:
                                    # adapt dictionary as JSONB
                                    new_row.append(item)
                                except Exception as e:
                                    print(f"Failed to adapt item: {item}")
                                    raise e
                            elif isinstance(item, str):
                                new_row.append(item.replace("'", ""))
                            else:
                                new_row.append(item)
                        prepared_rows.append(new_row)

                    insert_command = f'''
                    INSERT INTO "{table}" ({columns_placeholder})
                    VALUES ({values_placeholder})
                    ON CONFLICT DO NOTHING;
                    '''
                    new_cursor.executemany(insert_command, prepared_rows)
                    logging.info(f"Copied 100 rows for table {table}.")


def copy_schema_from_source_to_target(db_user, db_host, db_port, source_db_name, target_db_name):
    try:
        subprocess.run(
            [
                "pg_dump",
                "--schema-only",
                "-U", db_user,
                "-h", db_host,
                "-p", str(db_port),
                "-f", "postgres_dump.sql",
                source_db_name,
            ],
            stdout=subprocess.DEVNULL,  # silence the stdout
            stderr=subprocess.DEVNULL,  # silence the stderr
            check=True,
        )
        logging.info("Dumped schema from the source database")

        subprocess.run(
            [
                "psql",
                "-U", db_user,
                "-h", db_host,
                "-p", str(db_port),
                "-d", target_db_name,
                "-f", "postgres_dump.sql",
            ],
            stdout=subprocess.DEVNULL,  # silence the stdout
            stderr=subprocess.DEVNULL,  # silence the stderr
            check=True,
        )
        logging.info("Loaded schema to the new database")

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to copy schema. More info: {str(e)}")
        raise


if __name__ == '__main__':
    # Database configuration
    SOURCE_DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    DB_PORT = 30011
    # Create a new database with a unique name
    TARGET_DB_NAME = 'postgres_limited'

    limit_rows_db(SOURCE_DB_NAME, DB_USER, DB_PASSWORD,
                  DB_HOST, DB_PORT, TARGET_DB_NAME)
