from django.shortcuts import render

def accueil(request):
    return render(request, 'front_end/accueil.html')  # Affiche le template accueil.html

