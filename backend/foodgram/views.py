from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response, permissions
from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)

from .models import Favorite, Recipe, Tag, Ingredient
from .serializers import (
    FavoriteSerializer, RecipeSerializer, TagSerializer, IngredientSerializer,
    RecipeIngredientSerializer, RecipeCreateSerializer
)
from api.pagination import LimitPageNumberPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in permissions.SAFE_METHODS:
            return super().get_serializer_class()
        return RecipeCreateSerializer
    
    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        """Добавление/удаление рецепта из избранного."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(data={'user': user,
                                                  'recipe': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user,
                            recipe=recipe)
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(Favorite,
                                         user=user,
                                         recipe=recipe)
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
