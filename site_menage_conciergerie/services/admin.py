from django.contrib import admin
from .models import Service, Reservation, Client, Contact, Devis

admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Devis)


