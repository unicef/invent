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
    try:
        # Log the beginning of the process
        logger.info("Starting to fetch and update users from AAD")
        # Create an instance of the AzureUserManagement class
        adapter = AzureUserManagement()

        # Fetch specific users before updating. TODO: Remove when ready
        users_before_update = adapter.fetch_specific_users()

        # Call the process_aad_users method to fetch and process the users
        adapter.process_aad_users(max_users)

        # Fetch specific users after updating. TODO: Remove when ready
        users_after_update = adapter.fetch_specific_users()

        # Log the successful completion of the process
        logger.info(
            "Azure users fetched and updated in the database successfully.")

        # Find differences. TODO: Remove when ready
        for user_id, user_info_before in users_before_update.items():
            try:
                user_info_after = users_after_update.get(user_id)
                if user_info_after:
                    if user_info_before != user_info_after:
                        logger.info(f"User {user_id} was updated. Details: ")
                        logger.info(f"Before: {user_info_before}")
                        logger.info(f"After: {user_info_after}")
            except Exception as e:
                logger.error(f"Error processing user {user_id}: {str(e)}")

    except Exception as e:
        logger.error(f"Error in fetch_users_from_aad_and_update_db: {str(e)}")
