from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from .views import FollowViewSet, UserFollowViewSet

app_name = 'users'


router = SimpleRouter()

router.register('subscriptions', UserFollowViewSet, basename='subscriptions')
router.register(r'api/users/(?P<user_id>\d+)/subscribe/',
                FollowViewSet,
                basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]