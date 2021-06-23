from django.db.models import Count, Q, QuerySet


class RecipeQuerySet(QuerySet):
    """
    QuerySet для модели рецептов
    """

    def with_unlikeness(self, ingredients):
        """
        Возвращает рецепты в которых присутствует хотя бы 1 ингредиент из ingredients.
        Каждому рецепту проставляется unlikeness (>= 0) - число недостающих
        ингредиентов для рецепта.
        """
        return self.annotate(
            unlikeness=Count(
                'recipe_ingredients__pk',
                filter=~Q(recipe_ingredients__ingredient__in=ingredients)
            )
        ).filter(
            recipe_ingredients__ingredient__in=ingredients
        ).order_by('unlikeness')

    def get_available_by_ingredients(self, ingredients):
        """
        Возвращает все рецепты для приготовления которых достаточно
        заданных ингредиентов
        """
        return self.with_unlikeness(ingredients).filter(unlikeness=0)
