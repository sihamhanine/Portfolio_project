from django.contrib import admin
from .backend.models import Service, Reservation, Client, Contact, Devis

admin.site.register(Service)
admin.site.register(Reservation)
admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Devis)


