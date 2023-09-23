from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('email', 'username')
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
        """Делает все поля обязательными."""
        form = super().get_form(request, obj, **kwargs)
        for _, field in form.base_fields.items():
            field.required = True
        return form


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
