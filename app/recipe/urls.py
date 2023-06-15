"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# router.registerには 2 つの必須引数がある
# prefix: このルートのセットに使用するURLプレフィックス
# viewset: ビューセット クラス
router.register("recipes", views.RecipeViewSet)
# 上記では、次のURLパターンが生成される
# ^recipes/$ 名前:'recipes-list'
# ^recipes/{pk}/$ 名前:'recipes-detail'

# URLの名前空間
app_name = "recipe"

# ルーターインスタンスの属性.urlsは、単なるURLパターンの標準リスト
urlpatterns = [path("", include(router.urls))]
