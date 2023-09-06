from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Была добавлена вспомогательная функция static(), чтобы раздавать 
# медиафайлы с по мощью сервера разработки во время разработки 
# (то есть когда настроечный параметр DEBUG задан равным True).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
