import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

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
    name = serializers.CharField(read_only=True,
                                 source='ingredient.name')
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
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user,
                                           recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user,
                                               recipe=obj).exists()
        return False


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
            'id', 'tags', 'author', 'ingredients', 'name',
            'image', 'text', 'cooking_time',
        )
        read_only_fields = ('author',)
        extra_kwargs = {
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
            'image': {'required': True},
            'ingredients': {'required': True},
            'tags': {'required': True},
        }

    def validate_ingredients(self, ingredients) -> list:
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Не передано ни одного ингридиента'
            })
        ingredient_list = []
        for ingredient_item in ingredients:
            if ingredient_item['id'] in ingredient_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингридиенты не должны повторяться'
                })
            ingredient_list.append(ingredient_item['id'])
        return ingredients

    def validate_tags(self, tags) -> list:
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Не переданы тэги'
            })
        tag_list = []
        for tag_item in tags:
            if tag_item in tag_list:
                raise serializers.ValidationError({
                    'tags': 'Тэги не должны повторяться'
                })
            tag_list.append(tag_item)
        return tags

    def create_ingredients(self, ingredients_data, recipe) -> None:
        ingredients = []
        for ingredient in ingredients_data:
            ingredients.append(RecipeIngredient(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            ))
        RecipeIngredient.objects.bulk_create(ingredients)

    def create(self, validated_data) -> Recipe:
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data) -> Recipe:
        try:
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            instance.name = validated_data.get('name')
            instance.text = validated_data.get('text')
            instance.cooking_time = validated_data.get('cooking_time')
            instance.image = validated_data.get('image')
        except KeyError:
            raise serializers.ValidationError('Не переданы обязательные поля')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        return instance

    def to_representation(self, instance) -> dict:
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор добавления/удаления рецепта из избранного."""
    id = serializers.IntegerField(read_only=True,
                                  source='recipe.id')
    name = serializers.CharField(read_only=True,
                                 source='recipe.name')
    image = Base64ImageField(read_only=True,
                             source='recipe.image')
    cooking_time = serializers.IntegerField(
        read_only=True,
        source='recipe.cooking_time'
    )

    class Meta:
        model = Favorite
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )

    def validate_recipe(self, recipe) -> dict:
        if Recipe.objects.filter(id=recipe.id).exists():
            return recipe
        raise serializers.ValidationError('Рецепт не найден')

    def validate(self, attrs) -> dict:
        recipe = self.initial_data.get('recipe')
        user = self.initial_data.get('user')
        if Favorite.objects.filter(recipe=recipe,
                                   user=user).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже добавлен.'
            )
        return attrs


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор добавления/удаления рецепта из списка покупок."""
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart

    def validate(self, attrs) -> dict:
        recipe = self.initial_data.get('recipe')
        user = self.initial_data.get('user')
        if ShoppingCart.objects.filter(recipe=recipe,
                                       user=user).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже добавлен.'
            )
        return attrs
