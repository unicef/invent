from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user.models import UserProfile, Organisation
from country.models import Country


class Command(BaseCommand):
    help = """
    Generates test user with profile if needed
    user will be: pulitest, pulitest@pulilab.com, puli_1928 pw
    """

    def handle(self, *args, **options):
        self.stdout.write("-- Checking if test user exists")
        try:
            user = User.objects.get(email="pulitest@pulilab.com")
            self.stdout.write('-- No need to create test user')
        except User.DoesNotExist:
            self.stdout.write('-- Creating test user: pulitest@pulilab.com')
            user = User.objects.create_user('pulitest', 'pulitest@pulilab.com', 'puli_1928')

        self.stdout.write('-- Creating profile for user if needed')

        userprofile, _ = UserProfile.objects.get_or_create(user=user, defaults={'name': "Puli Test User"})
        userprofile.organisation = Organisation.objects.get(name="UNICEF")
        userprofile.country = Country.objects.all()[0]
        userprofile.global_portfolio_owner = True
        userprofile.save()

        self.stdout.write('-- Test user ready for use!')
