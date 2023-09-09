from django.contrib import admin

from .models import Follow, Recipe


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = ('user', 'author')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    search_fields = ('name',)
