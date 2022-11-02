from dj_anonymizer.register_models import (
    AnonymBase,
    register_anonym,
    register_clean
)
from dj_anonymizer import anonym_field
from user.models import UserProfile
from django.contrib.auth.models import User
from datetime import datetime


class UserProfileAnonym(AnonymBase):

    # Anonymize name.
    name = anonym_field.string("John Doe {seq}")

    class Meta:
        # List of fields to exclude which will not be changed.
        exclude_fields = ['global_portfolio_owner', 'created', 'modified', 'language', 'account_type', 'filters']


class UserAnonym(AnonymBase):

        # Anonymize last name.
        last_name = anonym_field.string("Doe")

        # Anonymize first name.
        first_name = anonym_field.string("John")

        # Anonymize email.
        email = anonym_field.string(
            "johndoe{seq}@preply.com", seq_callback=datetime.now
        )

        # Anonymize username.
        username = anonym_field.string("john_doe{seq}")
        

        class Meta:

                # Anonymize all users except the first one.
                queryset = User.objects.exclude(id=1)
                
                # List of fields which will not be changed.
                exclude_fields = [
                    "groups", "user_permissions", "is_active",
                    "is_superuser", "last_login", "date_joined",
                    "is_staff", "password"
                ]


register_anonym([
    (UserProfile, UserProfileAnonym),
    (User, UserAnonym)
])
