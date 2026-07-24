from django.test import TestCase


# django-allauth >= 65 resolves the configured social app from the database when
# rendering {% provider_login_url %}, so the homepage needs DB access.
class HomepageTests(TestCase):
    def setUp(self):
        self.response = self.client.get("/")

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_html(self):
        self.assertContains(self.response, "Homepage")

    def test_homepage_no_contains_html(self):
        self.assertNotContains(self.response, "Sign up")
