from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()

#router_v1.register()


urlpatterns = [
    path('', include(router.urls)),
]