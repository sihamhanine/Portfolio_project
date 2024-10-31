# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Client, Service, Reservation, Devis, Contact


#Serializer pour le modéle User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Ajoute d'autres champs si nécessaire
# Serializer pour le modèle Client
class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Sérialiseur pour le modèle User
    email = serializers.EmailField(source='user.email', read_only=True)  # Inclure l'email de l'utilisateur
    password = serializers.CharField(write_only=True)  # Mot de passe uniquement lors de l'écriture

    class Meta:
        model = Client
        fields = ['id', 'name', 'user', 'email', 'phone', 'password', 'address']

    def create(self, validated_data):
        # Sépare les données utilisateur du modèle Client
        user_data = validated_data.pop('user')
        user = User(**user_data)  # Crée un nouvel utilisateur
        user.set_password(validated_data.pop('password'))  # Définit le mot de passe
        user.save()  # Enregistre l'utilisateur

        client = Client.objects.create(user=user, **validated_data)  # Crée le client
        return client

# Serializer pour le modèle Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_description', 'date_service', 'price', 'image_path',
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
        fields = ['id', 'nom', 'email', 'objet', 'message']
