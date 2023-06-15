"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


# ModelViewSetはCRUD全てに対応した便利クラス
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive recipes for authenticated uer."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    # get_serializer_class(self):シリアライザーに使用するクラスを返す
    # 読み取りおよび書き込み操作に異なるシリアライザーを使用する、または異なるタイプのユーザーに異なるシリアライザーを提供するなど、
    # 動的な動作を提供するためにオーバーライドされる
    def get_serializer_class(self):
        """Return the serializer class for request."""
        # action:現在のアクションの名前 (例: list、create)
        # ViewSet actions
        # list(self, request)
        # create(self, request)
        # retrieve(self, request, pk=None)
        # update(self, request, pk=None)
        # partial_update(self, request, pk=None)
        # destroy(self, request, pk=None)
        if self.action == "lisl":
            return serializers.RecipeSerializer

        return self.serializer_class
