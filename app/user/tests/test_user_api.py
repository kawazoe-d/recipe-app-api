"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# APIサーバをテストするために用意されたDjangoの既存のClientクラスを拡張したモジュール
from rest_framework.test import APIClient
from rest_framework import status


# reverseは、普通の流れとは逆でnameからURLパスを呼び出す
# user appのname createを指定して呼び出す
CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user."""
    # get_user_model()で既定のユーザーモデルを取得し、マネージャーのcreate_userを実行
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        # テストクライアントのpostメソッドにエンドポイントとリクエストデータを渡す
        res = self.client.post(CREATE_USER_URL, payload)

        # ステータスコードの確認
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        # パスワードが正しく暗号化されているかの確認
        self.assertTrue(user.check_password(payload["password"]))
        # レスポンスにパスワードが含まれていないかの確認
        self.assertNotIn("password", res.data)

    def test_user_with_email_exist_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        # **による辞書の引数への展開
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if passworf less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # exists():結果が含まれているかどうかを真偽値で返す
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credenrtials."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        payload = {"email": user_details["email"], "password": user_details["password"]}
        res = self.client.post(TOKEN_URL, payload)

        # rokenが返ってきているかどうかの確認
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        # tokenが返って来ていないことの確認
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        # tokenが返って来ていないことの確認
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        # ユーザーを作成
        self.user = create_user(
            email="test@example.com", password="testpass123", name="Test Name"
        )
        # クライアントを作成
        self.client = APIClient()
        # リクエストを強制的に認証する
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve profile for logged in user."""
        res = self.client.get(ME_URL)

        # 認証が通っているかの確認
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_post_me_not_allowed(self):
        """
        Test POST is not allowed for the me endpoint.
        meエンドポイントではPOSTができないことのテスト
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {"name": "Updated name", "password": "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        # データベースからモデルの値を再読み込み
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
