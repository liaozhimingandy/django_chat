from django.test import TestCase, Client

from oauth.common.token import verify_jwt_token
from oauth.models import App


# Create your tests here.
class OauthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.app_id, self.app_secret = "7f90da9d-b207-4921-babf-12bb256d2d45", "ttufUBx3f5VsxBpKj7F1pBQrGfaW6TJl"
        app = App(app_id=self.app_id, app_secret=self.app_secret)
        app.save()

    def test_authorize(self):
        """
        Test that we can authenticate with app_id and app_secret
        """
        result = self.client.get(f"/oauth/authorize/{self.app_id}/{self.app_secret}/client_credential/", follow=True)

        self.assertEqual(result.status_code, 200)

        app = App.objects.get(app_id=self.app_id, app_secret=self.app_secret, is_active=True)
        jwt_token = verify_jwt_token(result.data.get("access_token", ''), grant_type="access_token")

        self.assertEqual(app.salt, jwt_token["salt"])

    def test_refresh_token(self):
        """
        Test that we can refresh token with app_id and refresh_token
        """
        result = self.client.get(f"/oauth/authorize/{self.app_id}/{self.app_secret}/client_credential/", follow=True)

        self.assertEqual(result.status_code, 200)

        refresh_token = result.data.get("refresh_token", '')
        result2 = self.client.get(f"/oauth/refresh-token/{self.app_id}/refresh_token/",
                                 follow=True, headers={"authorization": f"Bearer {refresh_token}"})

        self.assertEqual(result2.status_code, 200)

    def test_test_oauth(self):
        """
        Test that we can test OAuth
        """
        result = self.client.get(f"/oauth/authorize/{self.app_id}/{self.app_secret}/client_credential/", follow=True)

        self.assertEqual(result.status_code, 200)

        access_token = result.data.get("access_token", '')

        result2 = self.client.get(f"/oauth/test-oauth/", headers={"authorization": f"Bearer {access_token}"})

        self.assertEqual(result2.status_code, 200)