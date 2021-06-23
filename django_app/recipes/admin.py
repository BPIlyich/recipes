from django.contrib import admin
from .models import (
    Measure,
    Ingredient,
    RecipeCategory,
    Recipe,
    RecipeIngredient,
    UserRecipeScore
)


admin.site.register(Measure)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(UserRecipeScore)
