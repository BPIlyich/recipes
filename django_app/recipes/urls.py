from rest_framework import routers

from .views import (
    MeasureViewSet,
    IngredientViewSet,
    RecipeCategoryViewSet,
    RecipeViewSet,
    RecipeIngredientViewSet,
    UserRecipeRatingViewSet
)

router = routers.DefaultRouter()

router.register(r'measure', MeasureViewSet)
router.register(r'ingredient', IngredientViewSet)
router.register(r'recipe_category', RecipeCategoryViewSet)
router.register(r'recipe', RecipeViewSet)
router.register(r'recipe_ingredient', RecipeIngredientViewSet)
router.register(r'user_recipe_rating', UserRecipeRatingViewSet)

urlpatterns = router.urls
