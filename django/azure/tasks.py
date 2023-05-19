from celery.utils.log import get_task_logger

from .adapters import AzureUserManagement
from scheduler.celery import app

logger = get_task_logger(__name__)


@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db(max_users=100):
    """
    Fetches users from Azure Active Directory (AAD) and updates the database with their information.

    This task fetches users from AAD in batches and processes them, updating the database
    with their information. The process repeats until a maximum number of users have been processed or
    there are no more users to fetch from AAD.

    Parameters
    ----------
    max_users : int, optional
        The maximum number of users to process. Defaults to 100.
    """

    # Log the beginning of the process
    logger.info("Starting to fetch and update users from AAD")
    # Create an instance of the AzureUserManagement class
    adapter = AzureUserManagement()
    # Call the process_aad_users method to fetch and process the users
    adapter.process_aad_users(max_users)
    # Log the successful completion of the process
    logger.info("Azure users fetched and updated in the database successfully.")


@app.task(name="process_aad_user_changes")
def process_aad_user_changes(user_id):
    """
    Processes changes for a specific Azure Active Directory (AAD) user and updates the database.

    This task processes changes for a specific user fetched from AAD, and updates the database
    with their new information. It's typically triggered by a change notification for a user in AAD.

    Parameters
    ----------
    user_id : str
        The ID of the user to process changes for.
    """

    # Log the beginning of the process
    logger.info(f"Processing AAD user change notification for user {user_id}")
    # Create an instance of the AzureUserManagement class
    adapter = AzureUserManagement()
    # Process the changes for the specified user
    adapter.process_aad_user(user_id)
    # Log the successful completion of the process
    logger.info(
        f"User {user_id} data processed and updated in the database successfully.")
