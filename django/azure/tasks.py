from celery.utils.log import get_task_logger

from .adapters import AzureUserManagement
from scheduler.celery import app

logger = get_task_logger(__name__)


@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db(max_users=None):
    """
    Fetches users from Azure Active Directory (AAD) and updates the database with their information.

    This task fetches users from AAD in batches and processes them, updating the database
    with their information. The process repeats until a maximum number of users have been processed or
    there are no more users to fetch from AAD.

    Parameters
    ----------
    max_users : int, optional
        The maximum number of users to process. Defaults to None, that means every user available in the db.
    """
    # Log the beginning of the process
    logger.info("Starting to fetch and update users from AAD")
    # Create an instance of the AzureUserManagement class
    adapter = AzureUserManagement()
    # Call the process_aad_users method to fetch and process the users
    adapter.process_aad_users(max_users)
    # Log the successful completion of the process
    logger.info("Azure users fetched and updated in the database successfully.")
