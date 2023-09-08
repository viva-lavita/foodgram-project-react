import base64  # Модуль с функциями кодирования и декодирования base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, Tag, Ingredient, Favorite
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    pass


class IngredientSerializer(serializers.ModelSerializer):
    pass


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=True)
    author = CustomUserSerializer(read_only=True, required=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return IngredientSerializer(ingredients, many=True).data


class FavoriteSerializer(serializers.ModelSerializer):
    pass
