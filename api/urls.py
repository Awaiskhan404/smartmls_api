from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
        path('',views.index,name="index"),
        path('upload',views.simple_upload,name="upload"),
        path('process',views.process_api,name="Processing"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
