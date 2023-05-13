from celery.utils.log import get_task_logger

from core.utils import send_mail_wrapper
from scheduler.celery import app
from .adapters import MyAzureAccountAdapter

logger = get_task_logger(__name__)


@app.task(name="send_user_request_to_admins")
def send_user_request_to_admins(profile_id):
    """
    Sends user requests for donor and country user types to the admins.
    """
    from country.models import Country, Donor
    from .models import UserProfile

    admins = []
    admin_type = ""
    for_what = ""
    profile = UserProfile.objects.get(id=profile_id)

    if not any([profile.donor, profile.country]):
        return

    superusers = UserProfile.objects.filter(user__is_superuser=True)
    if profile.is_government_type():
        country = Country.objects.get(id=profile.country.id)
        admins = country.admins.all() | country.super_admins.all() | superusers
        admin_type = 'country'
        for_what = country.name
    elif profile.is_investor_type():
        donor = Donor.objects.get(id=profile.donor.id)
        admins = donor.admins.all() | donor.super_admins.all() | superusers
        admin_type = 'donor'
        for_what = donor.name

    for admin in admins:
        subject = "Request: {} has requested to be a {} for {}".format(str(profile),
                                                                       profile.get_account_type_display(),
                                                                       for_what)
        context = {
            "full_name": admin.name,
            "requester": str(profile),
            "requester_type": profile.get_account_type_display(),
            "admin_type": admin_type,
        }
        send_mail_wrapper(subject=subject,
                          email_type="admin_request",
                          to=admin.user.email,
                          language=admin.language,
                          context=context)


@app.task(name="fetch_users_from_aad_and_update_db")
def fetch_users_from_aad_and_update_db():
    adapter = MyAzureAccountAdapter()
    # Fetch the AAD users
    azure_users = adapter.get_aad_users()
    # Save the AAD users to the local database and get the updated user profiles
    updated_user_profiles = adapter.save_aad_users(azure_users)

    logger.info(f"Updated {len(updated_user_profiles)} user profiles")
    return f'Updated {len(updated_user_profiles)} user profiles. Azure users fetched and updated in the database successfully.'
