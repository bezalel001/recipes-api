from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, ):
    """Baseviewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Creat a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return appropriate serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class

        # class TagViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
        #     """Manage tags in the database"""
        #     authentication_classes = (TokenAuthentication,)
        #     permission_classes = (IsAuthenticated,)
        #     queryset = Tag.objects.all()
        #     serializer_class = TagSerializer

        #     def get_queryset(self):
        #         """Return objects for the current authenticated user only"""
        #         return self.queryset.filter(user=self.request.user).order_by('-name')

        #     def perform_create(self, serializer):
        #         """Create a new tag"""
        #         serializer.save(user=self.request.user)

        # class IngredientViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
        #     """Manage ingredients in the database"""
        #     authentication_classes = (TokenAuthentication, )
        #     permission_classes = (IsAuthenticated,)
        #     queryset = Ingredient.objects.all()
        #     serializer_class = IngredientSerializer

        #     def get_queryset(self):
        #         """Return object for the current authenticated user."""
        #         return self.queryset.filter(user=self.request.user).order_by('-name')

        #     def perform_create(self, serializer):
        #         serializer.save(user=self.request.user)
