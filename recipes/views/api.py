from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializers
  
@api_view()
def recipe_api_listt(request):
    recipes = Recipe.objects.get_published()[:10]
    serializers = RecipeSerializers(instance=recipes, many=True)
    return Response(serializers.data)

@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializers = RecipeSerializers(instance=recipe, many=False)
    return Response(serializers.data)