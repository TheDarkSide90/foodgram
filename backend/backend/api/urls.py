from django.urls import include, path
from rest_framework import routers

from .views import (
    RecipeViewSet,
    UserViewSet,
    TagViewSet,
    IngredientViewSet,
)

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, 'ingredients')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
