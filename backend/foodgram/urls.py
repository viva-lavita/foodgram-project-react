from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, TagViewSet


app_name = 'foodgram'


router = SimpleRouter()

router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]
