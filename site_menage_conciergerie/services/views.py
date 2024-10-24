from django.shortcuts import render, redirect
from rest_framework import generics
from .models import Client, Service, Reservation, Devis, Contact
from .serializers import ClientSerializer, ServiceSerializer, ReservationSerializer, DevisSerializer, ContactSerializer
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm


def accueil(request):
    return render(request, 'front_end/accueil.html')  # Affiche le template accueil.html

def nos_services(request):
    services = Service.objects.all()  # Récupérer tous les services depuis la base de données
    return render(request, 'front_end/NosServices.html', {'services': services})

def a_propos(request):
    return render(request, 'front_end/a-propos.html') # affiche le template a-propos.html

def notre_gestion(request):
    return render(request, 'front_end/notre-gestion.html') # affiche le template notre-gestion.html

def gestion_administrative(request):
    return render(request, 'front_end/gestion-administrative.html') # affiche le template gestion_administrative

def gestion_locative(request):
    return render(request, 'front_end/gestion-locative.html') # affiche le template gestion_locative

def packairbnb(request):
    return render(request, 'front_end/packairbnb.html') # affiche le template packairbnb

def reservation(request):
    return render(request, 'front_end/reservation.html') # affiche le template reservation

@login_required
def reserver(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user  # Associe le client connecté
            reservation.save()
            messages.success(request, "Votre réservation a été enregistrée avec succès.")
            return redirect('reserver')  # Redirige vers la même page après la soumission
    else:
        form = ReservationForm()
    
    return render(request, 'front_end/reserve.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('reserver')  # Rediriger vers la réservation après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'front_end/login.html', {'form': form})
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Crée l'utilisateur et le client
            messages.success(request, "Inscription réussie ! Bienvenue.")
            return redirect('reserver')  # Redirection vers la page de réservation
        else:
            print(form.errors)  # Affiche les erreurs du formulaire pour le débogage
            messages.error(request, "Veuillez corriger les erreurs ci-dessus.")
    else:
        form = SignUpForm()

    return render(request, 'front_end/inscription.html', {'form': form})




def contact(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        # Créer un nouvel objet Contact
        contact = Contact(
            nom=nom,
            email=email,  
            objet=objet,
            message=message
        )
        contact.save()
       # Utilise une adresse e-mail vérifiée comme expéditeur
        from_email = 'siham.elani17@gmail.com'  # Adresse e-mail vérifiée
        
        # Ajoute l'email du client dans le corps du message
        full_message = f"Message de : {nom}\nEmail : {email}\n\n{message}"

        # Envoie l'email
        send_mail(
            subject=f"{objet} de {nom}",
            message=full_message,
            from_email=from_email,  # Adresse e-mail vérifiée
            recipient_list=[email],  # Ton adresse e-mail
            fail_silently=False,
        )

        # Message de succès ou redirection après soumission
        messages.success(request, 'Votre message a été envoyé avec succès !')
        return redirect('contact')  # Rediriger vers la page de contact après soumission

    return render(request, 'front_end/contact.html') # affiche le template contact

def demander_devis(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        additional_details = request.POST.get('additional_details')
        desired_date = request.POST.get('desired_date')
        estimated_budget = request.POST.get('estimated_budget')

        # Créer un nouvel objet Devis
        devis = Devis(
            client_name=client_name,  # Utilisez client_name ici
            client_email=client_email,  # Utilisez client_email ici
            phone=phone,
            service=service,
            additional_details=additional_details,
            desired_date=desired_date,
            estimated_budget=estimated_budget
        )
        devis.save()

        # Envoyer l'email de confirmation
        send_mail(
            'Demande de Devis',
            f'Merci pour votre soumission ! Nous reviendrons vers vous bientôt.\nNom: {client_name}\nEmail: {client_email}\nTéléphone: {phone}\nService: {service}\nDétails: {additional_details}\nDate souhaitée: {desired_date}\nBudget estimé: {estimated_budget}',
            'siham.elani17@gmail.com',
            [client_email],
            fail_silently=False
        )

        return redirect('accueil')  # Redirection après l'envoi de l'email

    # Rendu du formulaire pour d'autres méthodes (GET par exemple)
    return render(request, 'front_end/demande-devis.html')




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
