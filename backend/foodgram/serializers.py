import base64  # Модуль с функциями кодирования и декодирования base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Recipe, Tag, Ingredient, Favorite, Follow
from users.serializers import CustomUserSerializer


User = get_user_model()


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
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = obj.ingredients_in_recipe.all()
        return IngredientSerializer(ingredients, many=True).data


class FavoriteSerializer(serializers.ModelSerializer):
    pass


#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit = request.GET.get('recipes_limit')
#         recipes = obj.recipes.all()
#         if limit:
#             recipes = recipes[: int(limit)]
#         serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
#         return serializer.data


# class RecipeShortSerializer(serializers.ModelSerializer):
#     """ Сериализатор полей избранных рецептов и покупок """

#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')


# class FollowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Follow
#         fields = ('user', 'author')
#         extra_kwargs = {
#             'user': {'read_only': True},
#             'author': {'read_only': True}
#         }

#     def validate(self, attrs):
#         request = self.context.get('request')
#         author_id = request.parser_context.get('kwargs').get('pk')
#         author = get_object_or_404(User, id=author_id)
#         user = request.user
#         if user == author:
#             raise serializers.ValidationError(
#                 'Нельзя подписаться на себя'
#             )
#         if Follow.objects.filter(user=user,
#                                  author=author).exists():
#             raise serializers.ValidationError(
#                 'Вы уже подписаны на этого автора'
#             )
#         return attrs

