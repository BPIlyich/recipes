from rest_framework.serializers import ModelSerializer

from .models import (
    Measure,
    Ingredient,
    RecipeCategory,
    Recipe,
    RecipeIngredient,
    UserRecipeScore
)


class MeasureSerializer(ModelSerializer):
    """
    Сериализатор мер
    """

    class Meta:
        model = Measure
        fields = ('id', 'name')


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'food_energy', 'alcohol_by_volume')


class RecipeCategorySerializer(ModelSerializer):
    """
    Сериализатор категорий рецептов
    """

    class Meta:
        model = RecipeCategory
        fields = ('id', 'name')


class RecipeIngredientSerializer(ModelSerializer):
    """
    Сериализатор ингредиентов рецепта
    """

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe', 'measure', 'ingredient', 'amount')


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор рецептов
    """
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'recipe_category', 'name', 'cook_time', 'author',
                  'created_at', 'updated_at', 'voter_turnout', 'rating',
                  'food_energy', 'alcohol_by_volume', 'recipe_ingredients')
        read_only_fields = ('author', 'created_at', 'updated_at',
                            'voter_turnout', 'rating', 'food_energy',
                            'alcohol_by_volume')


class UserRecipeScoreSerializer(ModelSerializer):
    """
    Сериализатор рейтингов рецептов
    """

    class Meta:
        model = UserRecipeScore
        fields = ('id', 'recipe', 'score', 'user', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')
