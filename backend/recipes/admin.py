from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

User = get_user_model()


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'get_image',
        'author',
        'get_tags',
        'get_favorites',
        'pub_date',
    )
    fields = (
        ('name', 'author', 'image'),
        ('cooking_time', 'text'),
        ('tags',),
    )
    search_fields = ('name', 'tags__name', 'author__username')
    list_filter = ('author__username', 'pub_date', 'tags__name')
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    inlines = (IngredientInline,)
    filter_horizontal = ('tags',)

    @admin.display(description='Популярность')
    def get_favorites(self, obj: Recipe):
        return obj.favorites.count()

    @admin.display(description='Тэги')
    def get_tags(self, obj: Recipe):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description='Изображение')
    def get_image(self, obj: Recipe):
        return mark_safe(
            f'<img src={obj.image.url} width="100" hieght="100"/>'
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user__username', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user__username', 'recipe__name')
