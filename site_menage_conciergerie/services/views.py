from django.shortcuts import render
from rest_framework import generics
from .models import Client, Service, Reservation, Devis, Contact
from .serializers import ClientSerializer, ServiceSerializer, ReservationSerializer, DevisSerializer, ContactSerializer

def accueil(request):
    return render(request, 'front_end/accueil.html')  # Affiche le template accueil.html

def nos_services(request):
    services = Service.objects.all()  # Récupérer tous les services depuis la base de données
    return render(request, 'front_end/NosServices.html', {'services': services})

def a_propos(request):
    return render(request, 'front_end/a-propos.html') # affiche le template a-propos.html

# Vues pour les Clients
class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# Vues pour les Services
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# Vues pour les Reservations
class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# Vues pour les Devis
class DevisList(generics.ListCreateAPIView):
    queryset = Devis.objects.all()
    serializer_class = DevisSerializer

class DevisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devis.objects.all()
    serializer_class = DevisSerializer

# Vues pour les Contacts
class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
