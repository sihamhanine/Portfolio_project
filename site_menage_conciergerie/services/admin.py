from django.contrib import admin
from .models import Service, Reservation, Client, Contact

admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(Client)
admin.site.register(Contact)

