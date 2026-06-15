from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .constants import (
    MAX_LENGTH_NAME_RECIPE,
    MAX_LENGTH_NAME_TAG,
    MAX_LENGTH_NAME_INGREDIENT,
    MAX_LENGTH_NAME_MEASUREMENT,
    MAX_LENGTH_CODE,
)

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(max_length=MAX_LENGTH_NAME_RECIPE)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Картинка'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Время в минутах',
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Tag(models.Model):
    name = models.CharField(
        unique=True, max_length=MAX_LENGTH_NAME_TAG, verbose_name='Название'
    )
    slug = models.CharField(
        unique=True, max_length=MAX_LENGTH_NAME_TAG, verbose_name='slug'
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_INGREDIENT,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_NAME_MEASUREMENT,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='in_carts'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]


class ShortLink(models.Model):
    recipe = models.OneToOneField(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='short_link'
    )
    code = models.CharField(max_length=MAX_LENGTH_CODE, unique=True)

    def __str__(self):
        return self.code
