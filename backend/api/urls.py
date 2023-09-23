from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('', include('recipes.urls')),
    path('', include('users.urls'))
]
