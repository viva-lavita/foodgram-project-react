from django.urls import include, path
from rest_framework import routers

from .views import UserFollowViewSet

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'users',
                UserFollowViewSet,
                basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
