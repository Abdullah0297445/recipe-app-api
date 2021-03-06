from rest_framework import serializers
from core import models


class TagSerializer(serializers.ModelSerializer):
    """Serialize the tag model"""

    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize the ingredient model"""

    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Ingredient.objects.all()
        )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = ['id', 'title', 'ingredients', 'tags', 'time', 'price',
                  'link']
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializes the detail view of the Recipe model"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serialize the image field on the recipe object"""
    class Meta:
        model = models.Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
