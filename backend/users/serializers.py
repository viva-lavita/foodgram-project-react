from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.validators import UniqueValidator

from .models import Follow
from foodgram.serializers import RecipeSerializer


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
                  'first_name',
                  'last_name',
                  'is_subscribed')
        extra_kwargs = {
            'is_subscribed': {'read_only': True}
        }

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj, author=self.context['request'].user
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


class UserFollowSerializer(CustomUserSerializer):
    """
    Сериализатор для выдачи рецептов авторов,
    на которых подписан текущий пользователь.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = CustomUserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )
        read_only_fields = ('__all__',)

    def get_recipes_count(self, obj: User):
        """Функция динамического рассчета количества рецептов автора"""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """
        Функция динамической выдачи рецептов автора,
        количество ограничено лимитом из QUERY PARAMETERS
        """
        limit = self.context['request'].query_params.get('recipes_limit')
        queryset = obj.recipes.all()

        if limit:
            queryset = queryset[:int(limit)]

        return RecipeSerializer(queryset, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, attrs):
        if attrs['user'] == attrs['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        if Follow.objects.filter(user=attrs['user'],
                                 author=attrs['author']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        return attrs
