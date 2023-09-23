from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('', include('foodgram.urls')),
    path('', include('users.urls'))
]
