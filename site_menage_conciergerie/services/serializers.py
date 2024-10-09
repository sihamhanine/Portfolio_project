# serializers.py
from rest_framework import serializers
from .models import Client, Service, Reservation, Devis, Contact

# Serializer pour le modèle Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'password', 'address']

# Serializer pour le modèle Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_description', 'price', 'image_path',
                  'subservice1_name', 'subservice1_description',
                  'subservice2_name', 'subservice2_description']

# Serializer pour le modèle Reservation
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'client', 'client_address', 'service', 'service_description',
                  'datetime_start', 'datetime_end', 'reservation_status']

# Serializer pour le modèle Devis
class DevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = ['id', 'client', 'service', 'service_description',
                  'estimated_price', 'devis_status', 'client_address']

# Serializer pour le modèle Contact
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'sender_name', 'sender_email', 'sender_phone', 'message']
