from django.contrib import admin
from django.urls import path, include
from services import views
from django.conf import settings
from django.conf.urls.static import static
from services.views import (
    ClientList, ClientDetail,
    ServiceList, ServiceDetail,
    ReservationList, ReservationDetail,
    DevisList, DevisDetail,
    ContactList, ContactDetail,
    nos_services,
)


urlpatterns = [
    # Point de terminaison pour l'API
    path('api/clients/', ClientList.as_view(), name='client-list'),
    path('api/clients/<int:pk>/', ClientDetail.as_view(), name='client-detail'),

    path('api/services/', ServiceList.as_view(), name='service-list'),
    path('api/services/<int:pk>/', ServiceDetail.as_view(), name='service-detail'),

    path('api/reservations/', ReservationList.as_view(), name='reservation-list'),
    path('api/reservations/<int:pk>/', ReservationDetail.as_view(), name='reservation-detail'),

    path('api/devis/', DevisList.as_view(), name='devis-list'),
    path('api/devis/<int:pk>/', DevisDetail.as_view(), name='devis-detail'),

    path('api/contacts/', ContactList.as_view(), name='contact-list'),
    path('api/contacts/<int:pk>/', ContactDetail.as_view(), name='contact-detail'),

    #  Vues pour les pages HTML
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('nosservices/', views.nos_services, name='nos_services'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('notre-gestion/', views.notre_gestion, name='notre_gestion'),
    path('gestion-administrative/', views.gestion_administrative, name= 'gestion_administrative'),
    path('gestion-locative/', views.gestion_locative, name= 'gestion_locative'),
    path('packairbnb/', views.packairbnb, name= 'packairbnb'),
    path('demande-devis/', views.demander_devis, name= 'demander_devis'),
    path('reservation/', views.reservation, name= 'reservation'),
    path('reserve/', views.reserver, name= 'reserver'),
    path('login/', views.login_user, name= 'login_user'),
    path('inscription/', views.signup, name= 'signup'),
    path('contact/', views.contact, name= 'contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

