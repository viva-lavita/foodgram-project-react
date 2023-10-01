from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as g
from rest_framework.authtoken.models import TokenProxy

from .models import Follow
from recipes.models import ShoppingCart

User = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.unregister(User)


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    autocomplete_fields = ['recipe']


class SubscriptionInline(admin.StackedInline):
    model = Follow
    fk_name = 'user'
    autocomplete_fields = ['author']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('email', 'username')
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_total_subscriptions',
        'get_total_followers',
        'get_total_recipes',
        'is_staff',
    )
    inlines = [
        SubscriptionInline,
        ShoppingCartInline,
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (g("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            g("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (g("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        'user_permissions',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name',
                'last_name', 'password1', 'password2'
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Делает все поля обязательными при создании."""
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            for _, field in form.base_fields.items():
                field.required = True
        return form

    @admin.display(description='Подписки')
    def get_total_subscriptions(self, obj):
        return obj.follower.count()

    @admin.display(description='Подписчики')
    def get_total_followers(self, obj):
        return obj.following.count()

    @admin.display(description='Рецепты')
    def get_total_recipes(self, obj):
        return obj.recipes.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
        'get_total_subscriptions',
    )
    search_fields = ('user__username', 'author__username')
    list_filter = ('author__username',)
    ordering = ('-id',)

    @admin.display(description='Подписок всего')
    def get_total_subscriptions(self, obj):
        return obj.user.follower.count()
