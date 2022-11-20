from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from app import views
urlpatterns = [
    path('', views.index,name="home"),
    path('file',views.file_up,name='file'),
    
]
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)