"""
Tests for django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

# urls に設定された名前をパラメータとして渡すと、URLを返す
from django.urls import reverse

# ビューレベルでのユーザとのインタラクションをシミュレートすることができるテストクライアント
from django.test import Client


# データベースを使ったテストクラスではDjango標準のTestCaseを使用するのが良い
# データベースを使わないテストクラスではSimpleTestCaseを使用するのが推奨
class AdminSiteTest(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """
        Create user and client.
        setUpは各テストメソッドの最初に実行される
        """
        # django.test.TestCaseのself.clientはデフォルトで
        # django.test.Clientのインスタンスが格納されているため下記は必要ないのでは？
        # self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        # assertContains:レスポンスのコンテンツに特定の文字列が含まれていることを検証
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # reverseでURLを生戾する
        # args=[self.user.id]で、URLにuser.idを指定する
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
