from celery.utils.log import get_task_logger

from .adapters import AzureUserManagement
from scheduler.celery import app

logger = get_task_logger(__name__)


@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db():
    logger.info("Starting to fetch and update users from AAD")
    adapter = AzureUserManagement()
    # Fetch the AAD users
    azure_users = adapter.get_aad_users()
    # Save the AAD users to the local database and get the updated user profiles
    updated_user_profiles = adapter.save_aad_users(azure_users)

    logger.info(f"Updated {len(updated_user_profiles)} user profiles")
    return f'Updated {len(updated_user_profiles)} user profiles. Azure users fetched and updated in the database successfully.'
