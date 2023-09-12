import base64  # Модуль с функциями кодирования и декодирования base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, Tag
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
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    measurement_unit = serializers.CharField(read_only=True)
    # amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""
    tags = TagSerializer(many=True,)
    author = CustomUserSerializer(read_only=True,)
    ingredients = RecipeIngredientSerializer(many=True,)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = RecipeIngredientSerializer(many=True,)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True,)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Не передано ни одного ингридиента'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингридиенты не должны повторяться'})
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def create_ingridients(self, ingredients_data, recipe):
        ingredients = []
        for ingredient in ingredients_data:
            amount = ingredient.get('amount')
            ingredients.append(RecipeIngredient(
                recipe=recipe,
                amount=amount,
                ingredient=get_object_or_404(
                    Ingredient, id=ingredient.get('id'))
                ))
        RecipeIngredient.objects.bulk_create(ingredients)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingridients(ingredients_data, recipe)
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    pass
