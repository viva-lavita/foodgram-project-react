from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow
from foodgram.models import Recipe


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """
    Кастомный сериализатор для модели User,
    переопределяет поведение сериализатора Djoser.UserSerializer.
    Поля сделаны обязательными, добавлено динамическое поле is_subscribed,
    которое позволяет определить, подписан ли пользователь на автора.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')
        extra_kwargs = {
            'is_subscribed': {'read_only': True}
        }

    def get_is_subscribed(self, obj: User):
        return Follow.objects.filter(
            user=self.context.get('request').user, author=obj
            ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Кастомный сериализатор для модели User,
    переопределяет поведение сериализатора Djoser.UserCreateSerializer.
    Определены обязательные поля для регистрации,
    сделана валидация на уникальность email и username.
    """
    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'password',
                  'username',
                  'first_name',
                  'last_name')
        extra_kwargs = {
            'email': {'required': True,
                      'validators': [
                          UniqueValidator(queryset=User.objects.all())
                          ]},
            'username': {'required': True,
                         'validators': [
                          UniqueValidator(queryset=User.objects.all())
                         ]},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class ShortResipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор укороченной информации о рецепте
    для выдачи в списке подписок.
    """
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = ('__all__',)


class UserFollowSerializer(CustomUserSerializer):
    """
    Сериализатор, который возвращает пользователей,
    на которых подписан текущий пользователь.
    В выдачу добавляются рецепты с укороченной информацией.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )
        read_only_fields = ('__all__',)

    def get_recipes_count(self, obj: User):
        """Функция динамического расчета количества рецептов автора."""
        return obj.recipes.count()

    def get_recipes(self, obj: User) -> dict:
        """
        Функция динамической выдачи рецептов автора,
        количество ограничено лимитом из QUERY PARAMETERS
        """
        limit = self.context['request'].query_params.get('recipes_limit')
        queryset = obj.recipes.all()

        if limit:
            queryset = queryset[:int(limit)]

        serializer = ShortResipesSerializer(queryset, many=True)

        return serializer.data

    def validate(self, attrs: dict) -> dict:
        """Валидация для создания подписки."""
        request = self.context.get('request')
        author_id = request.parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = request.user
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        if Follow.objects.filter(user=user,
                                 author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        return attrs
