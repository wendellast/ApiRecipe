from collections import defaultdict
from rest_framework import serializers
from .models import Category
from django.contrib.auth.models import User
from tag.models import Tag

from rest_framework import serializers
from tag.models import Tag

from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation', 'preparation_time',
            'tag_objects', 'tag_links',
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    preparation_time = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True, source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe}'
    
    def validate(self, attrs):
        super_validate = super().validate(attrs)
        cd = attrs

        _my_errors  = defaultdict(list)

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            _my_errors['title'].append('Cannot be equal to description')
            _my_errors['description'].append('Cannot be equal to title')

        if _my_errors:
            raise serializers.ValidationError(_my_errors)

        return super_validate
    
    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError("Must have at least 5 characters")
        
        return title




