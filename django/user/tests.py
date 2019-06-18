from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from django.core import mail
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from allauth.account.models import EmailConfirmation

from country.models import Country, Donor
from .models import Organisation, UserProfile


class UserTests(APITestCase):

    def setUp(self):
        # Create a test user.
        url = reverse("rest_register")
        data = {
            "email": "test_user1@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, response.json())
        self.test_user_key = response.json().get("key")
        self.test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(self.test_user_key), format="json")

        # Validate the account.
        key = EmailConfirmation.objects.get(email_address__email="test_user1@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, response.json())

        # Create a test user, don't validate the account.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, response.json())

        self.donor = Donor.objects.create(name='Donor 1', code='dnr1')

    def test_register_user(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user3@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())

    def test_register_user_unique_email(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user1@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"][0], "A user is already registered with this e-mail address.")

    def test_register_user_invalid_email(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user@gmail",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"][0], "Enter a valid email address.")

    def test_register_without_email(self):
        url = reverse("rest_register")
        data = {
            "email": "",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"][0], 'This field may not be blank.')

        data = {
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["email"][0], 'This field is required.')

    def test_verify_email(self):
        key = EmailConfirmation.objects.get(email_address__email="test_user2@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()["detail"], "ok")

    def test_login_user(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user1@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertIn("user_profile_id", response.json())

    def test_login_user_wrong_credentials(self):
        url = reverse("api_token_auth")
        data = {
            "username": "aaaaaa@gmail.com",
            "password": "123456hetNYOLCs"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json()["non_field_errors"][0], "Unable to log in with provided credentials.")

    def test_register_user_creates_user_profile(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user3@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        self.assertIn("user", response.json())
        self.assertIn("user_profile_id", response.json())
        self.assertIn("account_type", response.json())
        self.assertEqual(response.json().get("account_type"), UserProfile.IMPLEMENTER)

    def test_register_user_creates_user_profile_with_account_type(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user3@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC",
            "account_type": "G"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        self.assertIn("user", response.json())
        self.assertIn("user_profile_id", response.json())
        self.assertIn("account_type", response.json())
        self.assertEqual(response.json().get("account_type"), UserProfile.GOVERNMENT)

    def test_forgot_password_send_email(self):
        url = reverse("rest_password_reset")
        data = {
            "email": "test_user1@gmail.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['detail'], 'Password reset e-mail has been sent.')
        self.assertIn("Your Digital Health Atlas password has been reset", mail.outbox[2].subject)


class UserProfileTests(APITestCase):

    def setUp(self):
        # Create a test user without profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user1@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)

        # Validate the account.
        key = EmailConfirmation.objects.get(email_address__email="test_user1@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)

        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)

        # Validate the account.
        key = EmailConfirmation.objects.get(email_address__email="test_user2@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)

        # Log in.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.user_profile_id = response.json().get('user_profile_id')
        self.client = APIClient(HTTP_AUTHORIZATION="Token {}".format(response.json().get("token")), format="json")

        # Update profile.
        self.org = Organisation.objects.create(name="org1")
        self.country = Country.objects.all()[0]
        self.donor = Donor.objects.create(name="Donor1", code="donor1")
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": self.country.id,
            "donor": self.donor.id,
            "account_type": UserProfile.GOVERNMENT}
        response = self.client.put(url, data)

    def test_donor_is_not_reqired(self):
        url = reverse("rest_register")
        data = {
            "email": "test_user33@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)

        key = EmailConfirmation.objects.get(email_address__email="test_user33@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)

        url = reverse("api_token_auth")
        data = {
            "username": "test_user33@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        user_profile_id = response.json().get('user_profile_id')
        client = APIClient(HTTP_AUTHORIZATION="Token {}".format(response.json().get("token")), format="json")

        org = Organisation.objects.create(name="org33")
        country = Country.objects.all()[0]
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        data = {
            "name": "Test Name",
            "organisation": org.id,
            "country": country.id,
            "account_type": UserProfile.GOVERNMENT}
        response = client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['donor'], None)

    def test_obtain_user_profile_returns_id(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('user_profile_id'),
                         UserProfile.objects.get(user__email="test_user2@gmail.com").id)

    def test_retrieve_existent_user_profile_on_login(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertIn("user_profile_id", response.json())
        self.assertTrue(response.json().get("user_profile_id"))

    def test_retrieve_existent_user_profile(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        user_profile_id = response.json().get('user_profile_id')
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        client = APIClient(HTTP_AUTHORIZATION="Token {}".format(response.json().get("token")), format="json")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.country.users.add(user_profile_id)
        self.assertEqual(response.json().get('id'), user_profile_id)
        self.assertEqual(response.json().get('email'), "test_user2@gmail.com")
        self.assertEqual(response.json().get('donor'), self.donor.id)
        self.assertEqual(response.json().get('account_type'), UserProfile.GOVERNMENT)
        self.assertEqual(response.json().get('account_type_approved'), False)
        self.assertIn('language', response.json())

    def test_retrieve_existent_user_profile_approved(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        user_profile_id = response.json().get('user_profile_id')
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        client = APIClient(HTTP_AUTHORIZATION="Token {}".format(response.json().get("token")), format="json")

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.DONOR)
        self.donor.users.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.DONOR_ADMIN)
        self.donor.admins.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.SUPER_DONOR_ADMIN)
        self.donor.super_admins.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.GOVERNMENT)
        self.country.users.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.COUNTRY_ADMIN)
        self.country.admins.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.SUPER_COUNTRY_ADMIN)
        self.country.super_admins.remove(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.IMPLEMENTER)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), False)

        UserProfile.objects.filter(id=user_profile_id).update(account_type=UserProfile.SUPER_COUNTRY_ADMIN)
        self.country.super_admins.add(user_profile_id)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('account_type_approved'), True)

    def test_update_user_profile(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        data = response.json()
        updated_country = Country.objects.all()[2].id
        data.update(country=updated_country)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.json().get("country"), updated_country)

    def test_user_profile_update_with_empty_values(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        data['country'] = None
        data['organisation'] = None
        data['name'] = ''

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'name': ['This field may not be blank.'],
                          'country': ['This field may not be null.'],
                          'organisation': ['This field may not be null.']})

    def test_create_org(self):
        url = reverse("organisation-list")
        data = {
            "name": "org2"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_org(self):
        url = reverse("organisation-list")
        data = {
            "name": "org2"
        }
        response = self.client.post(url, data)
        url = reverse("organisation-detail", kwargs={"pk": response.json().get("id")})
        response = self.client.get(url)
        self.assertEqual(response.json().get("name"), "org2")

    def test_organisation_autocomplete(self):
        url = reverse("organisation-list")
        data = {
            "name": "other"
        }
        response = self.client.post(url, data)
        url = reverse("organisation-list")
        data = {
            "name": "org2"
        }
        response = self.client.post(url, data)
        url = reverse("organisation-list")
        response = self.client.get(url, {"name": "org"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_user_profile_api_should_return_organisation(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("organisation" in response.json())

    def test_user_profile_has_account_type_information(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("account_type" in response.json())

    def test_user_profile_create_sets_account_type(self):
        url = reverse("api_token_auth")
        data = {
            "username": "test_user1@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        user_profile_id = response.json().get('user_profile_id')
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        client = APIClient(HTTP_AUTHORIZATION="Token {}".format(response.json().get("token")), format="json")
        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": Country.objects.get(id=3).id,
            "account_type": UserProfile.DONOR,
            "donor": self.donor.id
        }
        response = client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_type'], UserProfile.DONOR)

    def test_user_profile_update_changes_account_type(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_type'], UserProfile.GOVERNMENT)

        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": Country.objects.get(id=3).id,
            "account_type": UserProfile.DONOR,
            "donor": self.donor.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_type'], UserProfile.DONOR)

    def test_user_profile_donor_is_missing(self):
        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_type'], UserProfile.GOVERNMENT)

        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": Country.objects.get(id=3).id,
            "account_type": UserProfile.DONOR
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'donor': ['Donor is required']})

        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": Country.objects.get(id=3).id,
            "account_type": UserProfile.DONOR,
            "donor": self.donor.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_type'], UserProfile.DONOR)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_admin_requests_are_triggering_celery_task(self):
        c = Country.objects.create(code='XXY', name='COUNTRY_TEST')
        c.admins.add(self.user_profile_id)

        d = Donor.objects.create(name='DONOR_TEST')
        d.super_admins.add(self.user_profile_id)

        u1 = User.objects.create(username="username1", email="user1@user.org")
        UserProfile.objects.create(name="USER1", user=u1, account_type=UserProfile.IMPLEMENTER, country=c)

        u2 = User.objects.create(username="username2", email="user2@user.org")
        UserProfile.objects.create(name="USER2", user=u2, account_type=UserProfile.GOVERNMENT)

        u3 = User.objects.create(username="username3", email="user3@user.org")
        upf3 = UserProfile.objects.create(name="USER3", user=u3, account_type=UserProfile.GOVERNMENT, country=c)

        self.assertEqual(mail.outbox[-1].subject, 'Request: {} has requested to be a {} for {}'.format(
            str(upf3), upf3.get_account_type_display(), c.name))

        u4 = User.objects.create(username="username4", email="user4@user.org")
        upf4 = UserProfile.objects.create(name="USER4", user=u4, account_type=UserProfile.SUPER_DONOR_ADMIN, donor=d)

        self.assertEqual(mail.outbox[-1].subject, 'Request: {} has requested to be a {} for {}'.format(
            str(upf4), upf4.get_account_type_display(), d.name))

        super_user = User.objects.filter(is_superuser=True).first()
        UserProfile.objects.create(user=super_user)

        upf3.account_type = UserProfile.COUNTRY_ADMIN
        upf3.save()

        self.assertEqual(mail.outbox[-1].subject, 'Request: {} has requested to be a {} for {}'.format(
            str(upf3), upf3.get_account_type_display(), c.name))

        # last two emails should be the same, but one going to the superuser
        self.assertEqual(mail.outbox[-1].subject, mail.outbox[-2].subject)
        self.assertNotEqual(mail.outbox[-1].recipients(), mail.outbox[-2].recipients())
        recipients = mail.outbox[-2].recipients()[0] + mail.outbox[-1].recipients()[0]
        self.assertTrue(UserProfile.objects.get(id=self.user_profile_id).user.email in recipients)
        self.assertTrue(super_user.email in recipients)
