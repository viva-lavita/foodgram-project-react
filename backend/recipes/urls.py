from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet


app_name = 'recipes'


router = SimpleRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
]
