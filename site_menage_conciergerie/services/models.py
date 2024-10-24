from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


# Modèle de base pour avoir un champ 'created_at' et 'id' dans tous les modèles
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True  # Indique que cette classe ne doit pas créer de table dans la base

# Modèle Client
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Lien avec le modèle User
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Modèle Service
class Service(BaseModel):
    service_name = models.CharField(max_length=50)
    service_description = models.TextField()
    price = models.FloatField()
    image_path = models.CharField(max_length=255, blank=True, null=True)

    # Sous-services pour mieux structurer les données
    subservice1_name = models.CharField(max_length=50, blank=True, null=True)
    subservice1_description = models.TextField(blank=True, null=True)
    subservice2_name = models.CharField(max_length=50, blank=True, null=True)
    subservice2_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.service_name

# Modèle Reservation
class Reservation(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_address = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_description = models.TextField()
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    reservation_status = models.CharField(max_length=25)

    def __str__(self):
        return f'Reservation for {self.client.user.name} on {self.datetime_start}'

# Modèle Devis
class Devis(BaseModel):
    client_name = models.CharField(max_length=100, default='Inconnu')  # Nom et Prénom du client
    client_email = models.EmailField(default='unknown@example.com')  # Email du client
    phone = models.CharField(max_length=15, blank=True, null=True)  # Numéro de téléphone
    service = models.CharField(max_length=100)  # Type de service demandé
    additional_details = models.TextField(blank=True, null=True)  # Détails supplémentaires
    desired_date = models.DateField(null=True, blank=True)  # Date souhaitée
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Budget estimé
    created_at = models.DateTimeField(null=True, blank=True)  # Date de création du devis


# Modèle Contact
class Contact(BaseModel):
    nom = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    objet = models.CharField(max_length=50, default='Inconnu')
    message = models.TextField()

    def __str__(self):
        return f'Message from {self.nom}'
