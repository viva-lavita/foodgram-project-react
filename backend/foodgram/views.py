from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from .filters import IngredientFilter, RecipeFilter, TagFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeSerializer,
    RecipeCreateSerializer, ShoppingCartSerializer, TagSerializer
)
from api.pagination import LimitPageNumberPagination
from api.permissions import AuthorOrStaffOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return super().get_serializer_class()
        return RecipeCreateSerializer

    def post_delete(self, request, pk, model, serializer_class):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = serializer_class(data={'user': user,
                                                'recipe': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user,
                            recipe=recipe)
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(model,
                                         user=user,
                                         recipe=recipe)
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавление/удаление рецепта из избранного."""
        return self.post_delete(
            request, pk, Favorite, FavoriteSerializer
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавление/удаление рецепта из корзины."""
        return self.post_delete(
            request, pk, ShoppingCart, ShoppingCartSerializer
        )

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        user = request.user
        ingredients = ShoppingCart.ingredients_shopping_cart(request.user)
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = 'Список покупок:\n'
        for ingredient in ingredients:
            shopping_list += (
                f'\n{ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) - '
                f'{ingredient["amount"]}')
        return HttpResponse(
            shopping_list,
            headers={
                'Content-Type': 'application/vnd.ms-excel',
                'Content-Disposition': f'attachment; filename={filename}',
            },
        )


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter


class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
