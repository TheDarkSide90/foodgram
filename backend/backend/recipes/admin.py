from django.contrib import admin
from django.db.models import Count

from .models import Recipe, RecipeIngredient, Tag, Ingredient, User, ShortLink


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorites_count')
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(favorites_count=Count('favorited_by'))

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return obj.favorites_count


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'code')
    search_fields = ('code',)
    list_filter = ('recipe',)
