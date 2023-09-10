from django.db import models
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


# class Favorite(models.Model):
#     """Класс избранного, ManyToMany(но скорее без переопределения)"""
#     pass


class Recipe(models.Model):
    """Модель рецепта"""
    tags = models.ManyToManyField(
        Tag,
        related_name='tags_in_recipe',
        verbose_name='Тэги',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients_in_recipe',
        verbose_name='Ингридиенты',
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
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты'),
            MaxValueValidator(
                1440, 'Время приготовления не может быть больше 24 часов')
        ],
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
