from django.azure.client import get_azure_ad_users
from django.contrib.auth import get_user_model


def new_users():
    # Call the get_azure_ad_users function and create new users in the Django app's database
    azure_ad_users = get_azure_ad_users()
    user_model = get_user_model()
    for azure_ad_user in azure_ad_users["value"]:
        try:
            user_model.objects.get(username=azure_ad_user["userPrincipalName"])
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(
                username=azure_ad_user["userPrincipalName"],
                email=azure_ad_user["mail"],
                first_name=azure_ad_user["givenName"],
                last_name=azure_ad_user["surname"],
            )
            print("this is a new user: ", azure_ad_user)

            # user.save()
        break