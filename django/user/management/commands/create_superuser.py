from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class Command(BaseCommand):
    """
    Custom Django management command to create a root superuser if it does not already exist.
    """
    help = 'Create a superuser if it does not already exist.'

    def handle(self, *args, **options):
        """
        Gets the User model and attempts to create a new superuser, of root does not exist. 
        """
        self.stdout.write('Creating superuser...')

        # Get the User model
        User = get_user_model()

        username = 'root'
        email = 'root@unicef.com'
        password = 'root'

        try:
            # Check if a User with the given username already exists
            if not User.objects.filter(username=username).exists():
                # If not, create the User
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
            else:
                # If a User already exists, print a message and skip creation
                self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        except IntegrityError:
            self.stderr.write(self.style.ERROR(f"Couldn't create user. Username {username} and/or email {email} are already taken."))

        self.stdout.write('Process finished.')
