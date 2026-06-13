from django_filters.rest_framework import (
    FilterSet, CharFilter, BooleanFilter, NumberFilter)

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = CharFilter(method='filter_tags')
    is_favorited = BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_cart')
    author = NumberFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ()

    def filter_favorited(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(favorited_by__user=user)

        return queryset

    def filter_cart(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(in_carts__user=user)

        return queryset

    def filter_tags(self, queryset, name, value):
        tags = self.request.query_params.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return queryset
