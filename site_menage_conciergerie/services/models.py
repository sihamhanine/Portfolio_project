from django.db import models
from django.core.validators import MinLengthValidator


# Modèle de base pour avoir un champ 'created_at' et 'id' dans tous les modèles
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True  # Indique que cette classe ne doit pas créer de table dans la base

# Modèle Client
class Client(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(12)],
        blank=False,
        null=False)
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
        return f'Reservation for {self.client.name} on {self.datetime_start}'

# Modèle Devis
class Devis(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_description = models.TextField()
    estimated_price = models.FloatField()
    devis_status = models.CharField(max_length=25)
    client_address = models.CharField(max_length=100)

    def __str__(self):
        return f'Devis for {self.client.name} - {self.estimated_price}'

# Modèle Contact
class Contact(BaseModel):
    sender_name = models.CharField(max_length=50)
    sender_email = models.EmailField(max_length=255)
    sender_phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f'Message from {self.sender_name}'
