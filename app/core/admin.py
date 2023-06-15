"""
django admin customization.
"""

from django.contrib import admin

# UserAdminはModelAdminをUser管理用にカスタマイズしたクラス
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# gettextとgettext_lazyは、多言語対応するために使用されている関数
# gettext_lazy関数をアンダースコアで使えるようのは慣習的なもの
from django.utils.translation import gettext_lazy as _


from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""

    # 一覧画面のソート項目
    ordering = ["id"]
    # 一覧画面の表示フィールド
    list_display = ["email", "name"]
    # 変更画面の表示フィールド
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important data"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
