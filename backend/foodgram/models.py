from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Модель Тэга"""
    pass


class Ingredient(models.Model):
    """Класс ингридиента"""
    pass


class Favorite(models.Model):
    """Класс избранного, ManyToMany(но скорее без переопределения)"""
    pass


class Recipe(models.Model):
    """Модель рецепта"""
    tags = models.ManyToManyField(
        Tag, related_name='tags_in_recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients_in_recipe',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка, закодированная в Base64',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=1,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
