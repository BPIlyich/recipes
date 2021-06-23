from typing import List
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from users.permissions import IsAdminOrReadOnly, IsAdminOrOwnerOrReadOnly
from users.mixins import MultiSerializerViewSetMixin

from .models import (
    Measure,
    Ingredient,
    RecipeCategory,
    Recipe,
    RecipeIngredient,
    UserRecipeScore
)
from .serializers import (
    MeasureSerializer,
    IngredientSerializer,
    RecipeCategorySerializer,
    RecipeSerializer,
    RecipeIngredientSerializer,
    UserRecipeScoreSerializer
)


@extend_schema_view(
    create=extend_schema(description='Создание единицы измерения'),
    retrieve=extend_schema(description='Получение единицы измерения'),
    update=extend_schema(description='Полное обновление единицы измерения'),
    partial_update=extend_schema(
        description='Частичное обновление единицы измерения'),
    destroy=extend_schema(description='Удаление единицы измерения'),
    list=extend_schema(description='Получение списка единиц измерения'),
)
class MeasureViewSet(ModelViewSet):
    """
    CRUD для единиц измерения
    """
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema_view(
    create=extend_schema(description='Создание ингредиента'),
    retrieve=extend_schema(description='Получение ингредиента'),
    update=extend_schema(description='Полное обновление ингредиента'),
    partial_update=extend_schema(
        description='Частичное обновление ингредиента'),
    destroy=extend_schema(description='Удаление ингредиента'),
    list=extend_schema(description='Получение списка ингредиентов'),
)
class IngredientViewSet(ModelViewSet):
    """
    CRUD для ингредиентов
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema_view(
    create=extend_schema(description='Создание категории рецепта'),
    retrieve=extend_schema(description='Получение категории рецепта'),
    update=extend_schema(description='Полное обновление категории рецепта'),
    partial_update=extend_schema(
        description='Частичное обновление категории рецепта'),
    destroy=extend_schema(description='Удаление категории рецепта'),
    list=extend_schema(description='Получение списка категорий рецептов'),
)
class RecipeCategoryViewSet(ModelViewSet):
    """
    CRUD для категорий рецептов
    """
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema_view(
    create=extend_schema(description='Создание рецепта'),
    retrieve=extend_schema(description='Получение рецепта'),
    update=extend_schema(description='Полное обновление рецепта'),
    partial_update=extend_schema(
        description='Частичное обновление рецепта'),
    destroy=extend_schema(description='Удаление рецепта'),
    list=extend_schema(description='Получение списка рецептов'),
)
class RecipeViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """
    CRUD для рецептов
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    serializer_action_classes = {
        'missed_ingredients': RecipeIngredientSerializer,
    }
    permission_classes = (IsAdminOrOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # TODO: Разобраться с parameters для правильного отображения в Swagger
    @extend_schema(
        description='Возвращает все рецепты для приготовления которых достаточно заданных ингредиентов',
    )
    @action(detail=False, methods=['GET'], name='Get available recipes by ingredients')
    def available_by_ingredients(self, request, *args, **kwargs):
        ingredients_id_list = request.GET.getlist('ingredient')
        ingredients = Ingredient.objects.filter(pk__in=ingredients_id_list)
        queryset = self.queryset.get_available_by_ingredients(ingredients)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    # TODO: Разобраться с parameters для правильного отображения в Swagger
    @extend_schema(
        description='Возвращает ингредиенты недостающие для приготовления рецепта',
    )
    @action(detail=True, methods=['GET'], name='Get missed ingredients for recipe')
    def missed_ingredients(self, request, *args, **kwargs):
        recipe = self.get_object()
        ingredients_id_list = request.GET.getlist('ingredient')
        ingredients = Ingredient.objects.filter(pk__in=ingredients_id_list)
        missed_ingredients = recipe.recipe_ingredients.exclude(
            ingredient__in=ingredients)
        serializer = RecipeIngredientSerializer(missed_ingredients, many=True)

        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='cook_time',
                type=OpenApiTypes.TIME,
                location=OpenApiParameter.QUERY,
                description='Filter by cook time',
                examples=[
                    OpenApiExample(
                        'Example 1',
                        # summary='short optional summary',
                        # description='longer description',
                        value='00:10:00'
                    ),
                ],
            ),
        ],
        description='Возвращает рецепты приготовление которых занимает не более указанного времени',
    )
    @action(detail=False, methods=['GET'], name='Get recipes with cook_time less than or equal entered time')
    def cook_time(self, request, *args, **kwargs):
        cook_time = request.GET.get('cook_time')
        queryset = self.queryset.filter(cook_time__lte=cook_time)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


@extend_schema_view(
    create=extend_schema(
        description='Создание ингредиентов рецептов с количеством и мерой'),
    retrieve=extend_schema(
        description='Получение ингредиентов рецептов с количеством и мерой'),
    update=extend_schema(
        description='Полное обновление ингредиентов рецептов с количеством и мерой'),
    partial_update=extend_schema(
        description='Частичное обновление ингредиентов рецептов с количеством и мерой'),
    destroy=extend_schema(
        description='Удаление ингредиентов рецептов с количеством и мерой'),
    list=extend_schema(
        description='Получение списка ингредиентов рецепта с количеством и мерой'),
)
class RecipeIngredientViewSet(ModelViewSet):
    """
    CRUD для ингредиентов рецептов с количеством и мерой
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    permission_classes = (IsAdminOrOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema_view(
    create=extend_schema(
        description='Создание пользовательского рейтинга рецептов'),
    retrieve=extend_schema(
        description='Получение пользовательского рейтинга рецептов'),
    update=extend_schema(
        description='Полное обновление пользовательского рейтинга рецептов'),
    partial_update=extend_schema(
        description='Частичное обновление пользовательского рейтинга рецептов'),
    destroy=extend_schema(
        description='Удаление пользовательского рейтинга рецептов'),
    list=extend_schema(
        description='Получение списка пользовательских рейтингов рецептов'),
)
class UserRecipeRatingViewSet(ModelViewSet):
    """
    CRUD для рейтинга рецептов
    """
    queryset = UserRecipeScore.objects.all()
    serializer_class = UserRecipeScoreSerializer
    permission_classes = (IsAdminOrOwnerOrReadOnly,)
    owner_field_name = 'user'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
