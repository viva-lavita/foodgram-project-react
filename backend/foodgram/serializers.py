import base64  # Модуль с функциями кодирования и декодирования base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag
from users.serializers import CustomUserSerializer


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Класс для сериализации изображений в base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэга"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента рецепта, с добавленным полем amount"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""
    tags = TagSerializer(many=True,)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = RecipeIngredientSerializer(
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Не передано ни одного ингридиента'})
        ingredient_list = []
        for ingredient_item in ingredients:
            if ingredient_item['id'] in ingredient_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингридиенты не должны повторяться'})
            ingredient_list.append(ingredient_item['id'])
        return ingredients

    def create_ingredients(self, ingredients_data, recipe):
        ingredients = []
        for ingredient in ingredients_data:
            ingredients.append(RecipeIngredient(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id'))
                )
        RecipeIngredient.objects.bulk_create(ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        try:
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            instance.name = validated_data.get('name')
            instance.text = validated_data.get('text')
            instance.cooking_time = validated_data.get('cooking_time')
            instance.image = validated_data.get('image')
        except KeyError:
            raise KeyError('Не переданы обязательные поля')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source='recipe.id')
    name = serializers.CharField(read_only=True, source='recipe.name')
    image = Base64ImageField(read_only=True, source='recipe.image')
    cooking_time = serializers.IntegerField(
        read_only=True,
        source='recipe.cooking_time'
    )

    class Meta:
        model = Favorite
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )

    def validate(self, attrs):
        recipe = self.initial_data.get('recipe')
        user = self.initial_data.get('user')
        if Favorite.objects.filter(recipe=recipe,
                                   user=user).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже обавлен в избранное.'
            )
        return attrs

