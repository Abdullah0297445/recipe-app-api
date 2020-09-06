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
