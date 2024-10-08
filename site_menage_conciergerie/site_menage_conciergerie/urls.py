from django.contrib import admin
from django.urls import path, include
from services import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('nosservices/', views.nos_services, name='nos_services'),
]

