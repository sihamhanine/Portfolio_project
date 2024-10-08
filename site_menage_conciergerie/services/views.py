from django.shortcuts import render
from .models import Service

def accueil(request):
    return render(request, 'front_end/accueil.html')  # Affiche le template accueil.html

def nos_services(request):
    services = Service.objects.all()  # Récupérer tous les services depuis la base de données
    return render(request, 'front_end/NosServices.html', {'services': services})

