from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core import models

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """
    Base viewsets
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """
        Returns objects for authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Create new tag
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manages tags in database
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """
    Manages ingredients in database
    """
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    

class RecipeViewSet(viewsets.ModelViewSet):
    """
    Manages recipes in database
    """
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """
        Returns objects for authenticated user
        """
        return self.queryset.filter(user=self.request.user)
    
    