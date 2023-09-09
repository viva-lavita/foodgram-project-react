from django.urls import include, path
from rest_framework.routers import SimpleRouter


app_name = 'foodgram'


router = SimpleRouter()

# router.register('users/subscriptions',
#                 UserFollowViewSet,
#                 basename='subscriptions')
# router.register(r'users/(?P<pk>\d+)/subscribe',
#                 FollowViewSet,
#                 basename='subscribe')
# router.register(r'users/', FollowViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
]