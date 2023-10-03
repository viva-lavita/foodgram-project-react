import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from .models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart',
    )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        )

    class Meta:
        model = Recipe
        fields = (
            'name', 'tags', 'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )


class TagFilter(FilterSet):

    class Meta:
        model = Tag
        fields = ('name', 'slug')
