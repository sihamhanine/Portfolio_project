from django.contrib import admin
from django.urls import path, include
from services import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Page d'accueil
]
