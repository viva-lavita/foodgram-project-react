from datetime import datetime
import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    """Модель Тэга"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX',
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Класс ингридиента"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return self.name


def image_upload_path(instance, filename) -> str:
    """
    Функция, которая прописывает путь для изображений рецепта.
    Для структурирования, файлы сохраняются в папки текущего года и месяца.
    Подкаталоги будут созданы автоматически.
    """
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    return os.path.join('images', year, month, filename)


class Recipe(models.Model):
    """Модель рецепта"""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиенты',
        through='RecipeIngredient',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to=image_upload_path,
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=1,
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты'),
            MaxValueValidator(
                1440, 'Время приготовления не может быть больше 24 часов'),
        ],
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Recipe)
def delete_image_with_object(sender, instance, **kwargs) -> None:
    """
    Функция для удаления изображения, связанного с
    объектом модели Recipe.
    """
    instance.image.delete(False)


class RecipeIngredient(models.Model):
    """Модель связи ингридиента с рецептом, добалено поле amount."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингридиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[
            MinValueValidator(
                1, 'Количество ингридиента не может быть меньше 1'),
        ],
    )

    class Meta:
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецептов'


class FavoriteShoppingCart(models.Model):
    """Абстрактная модель избранного и корзины покупок"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_%(class)s'
            )
        ]


class Favorite(FavoriteShoppingCart):
    """Класс добавленных пользователем в избранное рецептов"""

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(FavoriteShoppingCart):
    """Класс добавленных пользователем в корзину рецептов."""

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'shopping_carts'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @staticmethod
    def ingredients_shopping_cart(user) -> list:
        return (RecipeIngredient.objects
                .filter(recipe__shopping_carts__user=user)
                .values('ingredient__name', 'ingredient__measurement_unit')
                .order_by('ingredient__name')
                .annotate(amount=models.Sum('amount')))
