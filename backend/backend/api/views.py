from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from recipes.models import (
    Recipe,
    Favorite,
    ShoppingCart,
    Follow,
    RecipeIngredient,
    User,
    Ingredient,
    Tag,
)
from recipes.serializers import (
    RecipeSerializer,
    RecipeCreateSerializer,
    UserSerializer,
    UserCreateSerializer,
    FollowSerializer,
    AvatarSerializer,
    SetPasswordSerializer,
    IngredientSerializer,
    TagSerializer,
)
from .filters import IngredientFilter
from recipes.utils import generate_short_code
from recipes.models import ShortLink

from users.pagination import UserPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()

        obj, created = ShortLink.objects.get_or_create(recipe=recipe)

        if created or not obj.code:
            obj.code = generate_short_code()
            obj.save()

        return Response({
            "short-link": request.build_absolute_uri(f"/s/{obj.code}")
        })

    @action(detail=True, methods=[
        'post', 'delete'
    ], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            obj, created = Favorite.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not created:
                return Response(
                    {'errors': 'Уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_201_CREATED)

        favorite = Favorite.objects.filter(user=user, recipe=recipe)

        if not favorite.exists():
            return Response(
                {'errors': 'Рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=[
        'post', 'delete'
    ], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            obj, created = ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not created:
                return Response(
                    {'Ошибка': 'Уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_201_CREATED)

        cart_item = ShoppingCart.objects.filter(user=user, recipe=recipe)

        if not cart_item.exists():
            return Response(
                {'errors': 'Рецепта нет в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in_carts__user=request.user)
            .values(
                'ingredients__name',
                'ingredients__measurement_unit'
            )
            .annotate(total=Sum('amount'))
            .order_by('ingredients__name')
        )

        lines = ['Список покупок:\n']

        for item in ingredients:
            lines.append(
                f"{item['ingredients__name']} — "
                f"{item['total']} "
                f"{item['ingredients__measurement_unit']}"
            )

        content = '\n'.join(lines)

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )

        return response

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.author != request.user:
            return Response(
                {'errors': 'Можно удалять только свои рецепты'},
                status=status.HTTP_403_FORBIDDEN
            )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = UserPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['put', 'patch', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me/avatar'
    )
    def avatar(self, request):
        user = request.user

        if request.method == 'DELETE':
            user.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = AvatarSerializer(
            user,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        author = self.get_object()
        user = request.user

        if request.method == 'POST':

            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            obj, created = Follow.objects.get_or_create(
                user=user,
                author=author
            )

            if not created:
                return Response(
                    {'errors': 'Уже подписан'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        follow = Follow.objects.filter(user=user, author=author)

        if not follow.exists():
            return Response(
                {'errors': 'Подписка не найдена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user

        authors = User.objects.filter(following__user=user)

        page = self.paginate_queryset(authors)

        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='set_password'
    )
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data[
            'current_password'
        ]):
            return Response(
                {'current_password': ['Неправильный пароль']},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
