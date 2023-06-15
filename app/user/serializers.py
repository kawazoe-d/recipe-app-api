"""
serializer for the user API View.
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # スーパークラスではパスワードの暗号化ができないため、オーバーライドする必要がある
    def create(self, validated_data):
        """
        Create and return a user with encrypt password.
        暗号化パスワードを持つユーザーを作成して返す
        """
        return get_user_model().objects.create_user(**validated_data)

    # スーパークラスではパスワードの暗号化ができないため、オーバーライドする必要がある
    def update(self, instance, validated_data):
        """
        Update and return user.
        更新し、userを返す
        """
        # validated_dataからpasswordを抜き出す。なければNone
        password = validated_data.pop("password", None)
        # スーパークラスのupsateを使い、userを更新
        user = super().update(instance, validated_data)

        # passwordに変更がある場合
        if password:
            # Userモデルのインスタンスにpasswordをsetするときにはset_passwordメソッドを使わなければならない
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user auth token.
    Modelとは紐づかないため通常のSerializerを使用する
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        validateは与えらえたattrsをそのまま返すだけなので、処理を加える
        """
        email = attrs.get("email")
        password = attrs.get("password")
        # authenticate:キーワード引数の組み合わせを個々の認証バックエンドに対して問い合わせ、
        # 認証バックエンドで認証情報が有効とされればUserオブジェクトを返す
        user = authenticate(
            # contextのrequestの中に現在のユーザー情報が入ってる
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
