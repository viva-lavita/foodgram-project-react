from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()

#router.register()


urlpatterns = [
    path('', include(router.urls)),
    path('', include('foodgram.urls')),
    path('', include('users.urls'))
]