from django.urls import include, path
from rest_framework import routers
# from djoser.urls

from .views import UserFollowViewSet


app_name = 'users'

router = routers.DefaultRouter()

router.register(r'users',
                UserFollowViewSet,
                basename='subscriptions')
# router.register(r'users/(?P<pk>\d+)/subscribe',
#                 FollowViewSet,
#                 basename='subscribe')
# router.register(r'users', FollowViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]