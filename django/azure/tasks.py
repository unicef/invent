from __future__ import absolute_import, unicode_literals
from scheduler.celery import app
from celery.utils.log import get_task_logger

from .views import AzureOAuth2Adapter
from user.adapters import MyAzureAccountAdapter

logger = get_task_logger(__name__)


@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db():
    logger.info('Starting Azure users fetch and update task')
    azure_adapter = AzureOAuth2Adapter()
    account_adapter = MyAzureAccountAdapter()

    azure_users = azure_adapter.get_all_users()
    account_adapter.save_users_from_azure(azure_users)

    logger.info('Azure users fetched and updated in the database successfully.')
    return 'Azure users fetched and updated in the database successfully.'
