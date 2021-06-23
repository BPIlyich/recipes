from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from .managers import RecipeQuerySet


User = get_user_model()


class Measure(models.Model):
    """
    Модель единицы измерения (граммы, литры и т.д.)
    """
    name = models.CharField(_('name'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'measure'
        verbose_name = _('measure')
        verbose_name_plural = _('measures')


class Ingredient(models.Model):
    """
    Модель ингредиента (лимон, соль и т.д.)
    """
    name = models.CharField(_('name'), max_length=100, unique=True)
    food_energy = models.DecimalField(
        _('food energy'),
        help_text=_('in kcal/g'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    # Крепость ингредиента для рассчета крепости коктейля
    alcohol_by_volume = models.DecimalField(
        _('alcohol by volume'),
        help_text=_('in %'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'ingredient'
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')


class RecipeCategory(models.Model):
    """
    Модель категории рецепта (салат, суп и т.д.)
    """
    name = models.CharField(_('name'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'recipe_category'
        verbose_name = _('recipe category')
        verbose_name_plural = _('recipe categories')


class Recipe(models.Model):
    """
    Модель рецепта
    """
    objects = RecipeQuerySet.as_manager()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='recipes'
    )
    recipe_category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.CASCADE,
        verbose_name=_('recipe category'),
        related_name='recipes'
    )

    name = models.CharField(_('name'), max_length=100, unique=True)
    cook_time = models.TimeField(
        _('cook time'),
        null=True,
        blank=True,
        default=None,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    voter_turnout = models.PositiveSmallIntegerField(
        _('voter turnout'),
        null=True,
        blank=True,
        default=None,
    )
    full_score = models.PositiveIntegerField(
        _('full score'),
        null=True,
        blank=True,
        default=None,
    )
    rating = models.DecimalField(
        _('rating'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[
            MinValueValidator(Decimal('0')),
            MaxValueValidator(Decimal('10'))
        ]
    )

    # Поля food_energy и alcohol_by_volume заполняются по формулам из ингредиентов
    food_energy = models.DecimalField(
        _('food energy'),
        help_text=_('in kcal/g'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    # Крепость (для коктейлей)
    alcohol_by_volume = models.DecimalField(
        _('alcohol by volume'),
        help_text=_('in %'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.voter_turnout and self.full_score:
            self.rating = self.full_score / self.voter_turnout

    class Meta:
        ordering = ['rating', 'name']
        db_table = 'recipe'
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')


class RecipeIngredient(models.Model):
    """
    Модель ингредиента рецепта с количеством и мерой
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe'),
        related_name='recipe_ingredients'
    )
    measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        verbose_name=_('measure'),
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name=_('ingredient'),
        related_name='recipe_ingredients'
    )

    amount = models.DecimalField(
        _('amount'),
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}{self.measure}'

    class Meta:
        ordering = ['ingredient']
        db_table = 'recipe_ingredient'
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')


class UserRecipeScore(models.Model):
    """
    Модель рейтинга рецепта
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('users'),
        related_name='user_recipe_ratings'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe'),
        related_name='user_recipe_ratings'
    )

    score = models.PositiveSmallIntegerField(
        _('score'),
        help_text=_('from 1 to 10'),
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.recipe} - {self.score}'

    def save(self, *args, **kwargs):
        is_new = not self.pk
        old_score = self.score
        super().save(*args, **kwargs)
        if is_new:
            if self.recipe.voter_turnout:
                self.recipe.voter_turnout += 1
            else:
                self.recipe.voter_turnout = 1
            if self.recipe.full_score:
                self.recipe.full_score += self.score
            else:
                self.recipe.full_score = self.score
        else:
            self.recipe.full_score += self.score - old_score

    class Meta:
        ordering = ['score', 'recipe']
        unique_together = ('user', 'recipe')
        db_table = 'user_recipe_rating'
        verbose_name = _('user recipe score')
        verbose_name_plural = _('user recipe scores')
