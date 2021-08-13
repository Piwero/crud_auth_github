from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class LoginAccountsTests(TestCase):
    def setUp(self):
        self.response = self.client.get("/accounts/login/")

    def test_login_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_template(self):
        self.assertTemplateUsed(self.response, "account/login.html")

    def test_login_contains_html(self):
        self.assertContains(self.response, "Sign In")

    def test_login_no_contains_html(self):
        self.assertNotContains(self.response, "Sign up")


class SignupAccountsTests(TestCase):
    def setUp(self):
        self.response = self.client.get("/accounts/signup/")

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_template(self):
        self.assertTemplateUsed(self.response, "registration/signup.html")

    def test_signup_contains_html(self):
        self.assertContains(self.response, "Sign Up")

    def test_signup_no_contains_html(self):
        self.assertNotContains(self.response, "Homepage")

    def test_signup_model(self):
        new_user_test = CustomUser()
        new_user_test.username = "usernametest"
        new_user_test.email = "usertest@usermail.com"
        new_user_test.first_name = "first_name_test"
        new_user_test.last_name = "last_name_test"
        new_user_test.age = 20
        new_user_test.phone_number = "+072838834812"
        new_user_test.address = "Street test and city test"
        new_user_test.company = "company_name_test"
        new_user_test.job_position = "job_position_test"
        new_user_test.save()

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(
            get_user_model().objects.all()[0].username, new_user_test.username
        )
        self.assertEqual(get_user_model().objects.all()[0].email, new_user_test.email)
        self.assertEqual(
            get_user_model().objects.all()[0].first_name, new_user_test.first_name
        )
        self.assertEqual(
            get_user_model().objects.all()[0].last_name, new_user_test.last_name
        )
        self.assertEqual(get_user_model().objects.all()[0].age, new_user_test.age)
        self.assertEqual(
            get_user_model().objects.all()[0].phone_number, new_user_test.phone_number
        )
        self.assertEqual(
            get_user_model().objects.all()[0].address, new_user_test.address
        )
        self.assertEqual(
            get_user_model().objects.all()[0].company, new_user_test.company
        )
        self.assertEqual(
            get_user_model().objects.all()[0].job_position, new_user_test.job_position
        )

    def test_signup_valid_form(self):

        form_data = {
            "username": "piwero",
            "password1": "Thisisacontrasena!",
            "password2": "Thisisacontrasena!",
            "email": "piwerotest@test.com",
            "first_name": "Me",
            "last_name": "Test",
            "age": 23,
            "phone_number": "+010330424242",
            "address": "No9 in Testing Street",
            "company": "Test Company",
            "job_position": "Test Position",
        }

        form = CustomUserCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_signup_invalid_form(self):

        form_data = {
            "username": "piwero",
            "password1": "Thisisacontrasena!",
            "password2": "Thisiswrong!",
            "email": "piwerotest@test.com",
            "first_name": "Me",
            "last_name": "Test",
            "age": 23,
            "phone_number": "+010330424242",
            "address": "No9 in Testing Street",
            "company": "Test Company",
            "job_position": "Test Position",
        }

        form = CustomUserCreationForm(data=form_data)

        self.assertTrue(form.errors)


class EditProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="12test12", email="test@example.com"
        )
        self.user.save()
        self.client.force_login(self.user, None)

        self.response = self.client.get("/accounts/edit-profile")

    def test_edit_profile_status_code(self):

        self.assertEqual(self.response.status_code, 200)

    def test_edit_profile_template(self):
        self.assertTemplateUsed(self.response, "edit-profile.html")

    def test_edit_profile_contains_html(self):
        self.assertContains(self.response, "Edit Profile Page")

    def test_edit_profile_no_contains_html(self):
        self.assertNotContains(self.response, "Sign up")


class EditProfileFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12test12", email="test@example.com"
        )
        self.user.save()
        self.client.force_login(self.user, None)
        form_data = {
            "username": "piwerotest",
            "email": "piwerotest@test.com",
            "first_name": "Me",
            "last_name": "Test",
            "age": 23,
            "phone_number": "+010330424242",
            "address": "No9 in Testing Street",
            "company": "Test Company",
            "job_position": "Test Position",
        }
        self.response = self.client.post("/accounts/edit-profile", form_data)

    def test_edit_profile_form_status_code(self):

        self.assertEqual(self.response.status_code, 302)

    def test_edit_profile_modify_data(self):
        self.response = self.client.get("/")
        self.assertContains(self.response, "piwerotest")
        self.assertNotContains(self.response, "testuser")
