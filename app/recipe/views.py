from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
)
from recipe import serializers
from rest_framework import (
    viewsets,
    mixins,
)

"""views are functions to process incoming requets using logic contained in them and return response, in order to do that we 
first have to fetch data or process it from database and then serialise ot """
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    """Specifies the authentication classes to be used for authenticating 
    requests. Here, it's set to TokenAuthentication for token-based authentication."""
    authentication_classes = [TokenAuthentication]

    """Specifies the permission classes to be used for controlling access to views. """
    permission_classes = [IsAuthenticated]

    "Purpose: To retrieve recipes associated with the authenticated user."
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        """ self: Refers to the current instance of the class (RecipeViewSet).

            self.queryset: Refers to the default queryset defined for the RecipeViewSet,
            which contains all recipes.       
            
            .filter(user=self.request.user): Filters the queryset to include only 
            recipes belonging to the authenticated user (self.request.user).

                 """
        return self.queryset.filter(user=self.request.user).order_by('-id')
    

    """Purspose: This method determines which serializer class to use for serializing 
    data based on the action being performed 
    (e.g., listing, retrieving, updating, or creating recipes).
    """
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class
    
    "Purpose: To customize the creation process of a new recipe."
    def perform_create(self, serializer):
        """Create a new recipe.
        Explanation:
        self: Refers to the current instance of the class (RecipeViewSet).
        serializer: Represents the serializer instance used for serializing the data.
        serializer.save(user=self.request.user): Saves the new recipe to the database, associating it with the authenticated user (self.request.user).
        Intuition: This method ensures that the user field of 
        the recipe is set to the authenticated user before saving it to the database, 
        """
        serializer.save(user=self.request.user)

class TagViewSet(mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')