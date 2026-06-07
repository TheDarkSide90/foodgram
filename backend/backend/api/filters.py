from django_filters import rest_framework as filters
from django.db.models import Case, When, Value, IntegerField

from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def filter_name(self, queryset, name, value):
        return queryset.annotate(
            priority=Case(
                When(name__istartswith=value, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).filter(
            name__icontains=value
        ).order_by('priority', 'name')
