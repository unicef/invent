# anonymize_db.py
from json import dumps, loads
import os
import logging
import random
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


def anonymize_db(source_db_name, db_user, db_password, db_host, db_port, target_db_name):
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    fake = Faker()

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

    try:
        # Copy schema from the original database to the new one
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
                # Define the tables and columns to anonymize
                tables_to_anonymize = {
                    'account_emailaddress': ['email'],
                    'auth_user': ['username', 'first_name', 'last_name', 'email'],
                    'core_newsitem': ['title', 'description', 'description_en', 'description_es', 'description_fr', 'description_pt', 'title_en', 'title_fr', 'title_es', 'title_pt'],
                    'project_hardwareplatform': ['name', 'name_en', 'name_es', 'name_fr', 'name_pt'],
                    'project_nontechplatform': ['name', 'name_en', 'name_es', 'name_fr', 'name_pt'],
                    'project_hardwareplatform': ['name', 'name_en', 'name_es', 'name_fr', 'name_pt'],
                    'project_technologyplatform': ['name', 'name_en', 'name_es', 'name_fr', 'name_pt'],
                    'project_project': ['name', 'data', 'draft'],
                    'project_projectportfoliostate': ['overall_reviewer_feedback'],
                    'project_projectversion': ['name', 'data'],
                    'project_reviewscore': ['psa_comment', 'rnci_comment', 'ratp_comment', 'ra_comment', 'ee_comment', 'nct_comment', 'nc_comment', 'ps_comment'],
                    'project_solution': ['name'],
                    'search_projectsearch': ['partner_names'],
                    'socialaccount_socialaccount': ['data'],
                    'user_userprofile': ['name', 'department', 'job_title']
                }
                # List of options that will be excluded from the anonymization script.
                non_anonymized_options = ['N/A', 'Unknown', 'Other']

                column_faker_map = {
                    'email': 'email',
                    'username': 'user_name',
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'title': 'sentence',
                    'description': 'paragraph',
                    'description_en': 'paragraph',
                    'description_es': 'paragraph',
                    'description_fr': 'paragraph',
                    'description_pt': 'paragraph',
                    'title_en': 'sentence',
                    'title_fr': 'sentence',
                    'title_es': 'sentence',
                    'title_pt': 'sentence',
                    'name': 'name',
                    'name_en': 'name',
                    'name_es': 'name',
                    'name_fr': 'name',
                    'name_pt': 'name',
                    'data': anonymize_json_project_data,
                    'draft': anonymize_json_project_data,
                    'overall_reviewer_feedback': 'paragraph',
                    'psa_comment': 'sentence',
                    'rnci_comment': 'sentence',
                    'ratp_comment': 'sentence',
                    'ra_comment': 'sentence',
                    'ee_comment': 'sentence',
                    'nct_comment': 'sentence',
                    'nc_comment': 'sentence',
                    'ps_comment': 'sentence',
                    'partner_names': 'name',
                    'department': 'bs',  # Generates random business nonsense
                    'job_title': 'job',
                }

                # Anonymize data
                # In the anonymization process, add a check before creating the fake value.
                for table, columns in tables_to_anonymize.items():
                    try:
                        # Fetch data from the original table
                        cursor.execute(f"SELECT * FROM {table};")
                        rows = cursor.fetchall()

                        # Fetch the existing emails from the account_emailaddress table
                        if table == 'account_emailaddress':
                            new_cursor.execute(
                                "SELECT email FROM account_emailaddress;")
                            existing_emails = {result[0]
                                               for result in new_cursor.fetchall()}

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
                                    # Check if the value is in the non_anonymized_options list
                                    if row[column_index] not in non_anonymized_options:
                                        faker_method = column_faker_map[column]
                                        if callable(faker_method):
                                            # If it's a function, call it with the JSON data as an argument
                                            new_row[column_index] = dumps(
                                                faker_method(loads(row[column_index])))
                                        elif column == 'email' and table == 'account_emailaddress':
                                            # Generate a unique email
                                            email = getattr(
                                                fake, faker_method)()
                                            while email in existing_emails:
                                                email = getattr(
                                                    fake, faker_method)()
                                            existing_emails.add(email)
                                            new_row[column_index] = email
                                        else:
                                            new_row[column_index] = getattr(
                                                fake, faker_method)()
                                    else:
                                        new_row[column_index] = row[column_index]
                            anonymized_rows.append(new_row)

                        # Insert anonymized data into the new table
                        values_placeholder = ','.join(['%s'] * len(row))
                        new_cursor.executemany(
                            f"INSERT INTO {table} VALUES ({values_placeholder});", anonymized_rows)

                        logging.info(f"Anonymized data in table {table}")

                    except psycopg2.Error as e:
                        logging.error(
                            f"Failed to anonymize data in table {table}. More info: {str(e)}")
                        raise

    except psycopg2.Error as e:
        logging.error(
            f"Failed to connect to the new database or execute a database operation. More info: {str(e)}")
        raise


def anonymize_json_project_data(json_data):
    fake = Faker()
    if 'name' in json_data:
        json_data['name'] = fake.name()
    if 'overview' in json_data:
        json_data['overview'] = fake.sentence()
    if 'total_budget' in json_data:
        json_data['total_budget'] = str(random.randint(0, 1000000))
    if 'contact_name' in json_data:
        json_data['contact_name'] = fake.name()
    if 'contact_email' in json_data:
        json_data['contact_email'] = fake.email()
    if 'links' in json_data:
        for link in json_data['links']:
            if 'link_url' in link:
                link['link_url'] = fake.url()
    if 'partners' in json_data:
        for partner in json_data['partners']:
            if 'partner_name' in partner:
                partner['partner_name'] = fake.name()
    if 'program_targets' in json_data:
        json_data['program_targets'] = fake.sentence()
    if 'current_achievements' in json_data:
        json_data['current_achievements'] = fake.sentence()
    if 'implementation_overview' in json_data:
        json_data['implementation_overview'] = fake.sentence()
    if 'program_targets_achieved' in json_data:
        json_data['program_targets_achieved'] = fake.sentence()

    return json_data


if __name__ == '__main__':
    # Database configuration
    SOURCE_DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_HOST = 'localhost'
    DB_PORT = 30011
    # Create a new database with a unique name
    TARGET_DB_NAME = 'postgres_anonymized'

    anonymize_db(SOURCE_DB_NAME, DB_USER, DB_PASSWORD,
                 DB_HOST, DB_PORT, TARGET_DB_NAME)
