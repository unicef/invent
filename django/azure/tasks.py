from celery.utils.log import get_task_logger

from .adapters import AzureUserManagement
from scheduler.celery import app

logger = get_task_logger(__name__)

@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db(max_users=100):
    logger.info("Starting to fetch and update users from AAD")
    adapter = AzureUserManagement()
    # Call process_aad_users instead of get_aad_users
    adapter.process_aad_users(max_users)

    logger.info("Azure users fetched and updated in the database successfully.")
