from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response
from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)

from .models import Recipe, Tag, Ingredient
from .serializers import (
    RecipeSerializer, TagSerializer, IngredientSerializer,
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
        if self.action in ['create', 'update']:
            return RecipeCreateSerializer
        return super().get_serializer_class()


class TagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Вьюсет ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
