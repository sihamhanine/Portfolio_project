from .imports import *


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

def historique_service(request):
    # Exemple de choix de statut, à adapter selon votre modèle
    status_choices = [
        ('En attente', 'En attente'),
        ('Terminée', 'Terminée'),
        ('Annulée', 'Annulée'),
        ('Confirmée', 'Confirmée'),
    ]
    # Récupérer les réservations du client connecté
    client = request.user.client
    reservations = Reservation.objects.filter(client=client)

    # Récupérer les paramètres de filtre
    status = request.GET.get('status', '')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    # Filtrer par statut si un statut est fourni
    if status:
        reservations = reservations.filter(reservation_status=status)

    # Filtrer par date de début si fourni
    if date_start:
        reservations = reservations.filter(datetime_start__gte=date_start)
    # Filtrer par date de fin si fourni
    if date_end:
        reservations = reservations.filter(datetime_end__lte=date_end)

    # Trier les résultats par date de début, les plus récents en premier
    reservations = reservations.order_by('-datetime_start')

    context = {
        'status_choices': status_choices,
        'reservations': reservations,
        'status': status,
        'date_start': date_start,
        'date_end': date_end,
    }

    return render(request, 'front_end/historique.html', context)
@login_required
def dash_reservation(request):
    query = request.GET.get('search', '').strip()
    reservations = Reservation.objects.none()

    if request.user.is_authenticated:

        # Récupérer l'instance Client associée à l'utilisateur connecté
        client_instance = Client.objects.get(user=request.user)
        # Récupère toutes les réservations de l'utilisateur connecté
        reservations = Reservation.objects.filter(client=client_instance)
        print("Toutes les réservations de l'utilisateur:", reservations)

        if query:
            # Test 1 : Filtrer par nom de service
            service_filtered = reservations.filter(service__service_name__icontains=query)
            print("Filtré par nom de service:", service_filtered)

            # Test 2 : Filtrer par date
            try:
                # Tente de convertir la recherche en date
                date_search = parser.parse(query, fuzzy=True).date()
                print("Date recherchée:", date_search)  # Vérifie la date analysée
                date_filtered = reservations.filter(datetime_start__date=date_search)
                print("Filtré par date:", date_filtered)
            except ValueError:
                print("La recherche n'est pas une date valide.")  # Enregistre l'erreur
                date_filtered = Reservation.objects.none()

            # Combine les résultats des deux filtres
            reservations = service_filtered | date_filtered

    return render(request, 'dash_reservation.html', {'reservations': reservations, 'search': query})


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Vérifiez que l'utilisateur connecté est bien celui qui a effectué la réservation
    if reservation.client == request.user.client:
        if request.method == 'POST':
            reservation.reservation_status = 'Annulée'  # Correction ici
            reservation.delete()
            
            return redirect('dash_reservation')
    else:
        messages.error(request, "Vous n'avez pas l'autorisation d'annuler cette réservation.")
        return redirect('dash_reservation')



@login_required
def reserver(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Récupérez l'objet Client associé à l'utilisateur connecté
            client = Client.objects.get(user=request.user)
            reservation.client = client  # Associe le client à la réservation
            reservation.reservation_status = 'En attente'  # Statut initial
            reservation.save()  # Enregistrez la réservation dans la base de données
            messages.success(request, "Votre réservation a été enregistrée avec succès.")
            return redirect('reserver')  # Redirige vers la même page après la soumission
    else:
        form = ReservationForm()

    return render(request, 'front_end/reserve.html', {'form': form})

# vue pour inscription d'un user
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

#vue pour l'espace personnel du client
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Recherche l'utilisateur par l'email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        # Authentification avec l'utilisateur trouvé
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('dashboard')  # Remplacez par le nom de la vue de l'espace personnel
        else:
            # Afficher un message d'erreur
            error_message = "Identifiants invalides."
            return render(request, 'front_end/login.html', {'error_message': error_message})
    
    return render(request, 'front_end/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    logout(request)
    cache.clear() 
    request.session.flush()
    messages.success(request, "Vous êtes déconnecté.")
    return render(request, 'front_end/accueil.html')

@login_required
def dashboard(request):
   # Récupérer l'instance Client associée à l'utilisateur actuel
    try:
        client_instance = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        client_instance = None  # Gérer le cas où le client n'existe pas

    services_a_venir = []
    derniers_services = []

    if client_instance:
        # Récupérer les réservations à venir
        services_a_venir = Reservation.objects.filter(
            client=client_instance,
            reservation_status='En attente'  # Assurez-vous que cela correspond exactement à ce qui est stocké
        )

        # Debug : Afficher les réservations à venir
        print(f"Services à venir pour {client_instance.user.username}: {services_a_venir}")

        # Récupérer l'historique des services (services passés)
        derniers_services = Reservation.objects.filter(
            client=client_instance,
            reservation_status='Terminée'  # Assurez-vous que cela correspond également
        )

        # Debug : Afficher les derniers services
        print(f"Derniers services pour {client_instance.user.username}: {derniers_services}")

    user_services = Service.objects.filter(client=client_instance)

    context = {
        'user': request.user,
        'services_a_venir': services_a_venir,
        'derniers_services': derniers_services,
        'user_services': user_services,
    }

    return render(request, 'front_end/dashboard.html', context)

@login_required
def exporter_historique(request):
    # Récupérer les réservations de l'utilisateur
    client_instance = Client.objects.get(user=request.user)
    reservations = Reservation.objects.filter(client=client_instance)

    # Créer une réponse HTTP avec le type de contenu approprié
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historique_reservations.csv"'

    # Créer un writer CSV
    writer = csv.writer(response)
    
    # Écrire l'en-tête
    writer.writerow(['Service', 'Date de début', 'Date de fin', 'Statut', 'Description', 'Adresse'])

    # Écrire les données des réservations
    for reservation in reservations:
        writer.writerow([
            reservation.service.service_name,
            reservation.datetime_start,
            reservation.datetime_end,
            reservation.get_reservation_status_display(),
            reservation.service_description,
            reservation.client_address
        ])

    return response

# vue pour mettre a jour profil user
@login_required
def mon_compte(request):
    # Récupérer l'objet client lié à l'utilisateur connecté
    client = request.user.client
    
    # Vérifier si le formulaire a été soumis
    if request.method == 'POST':
        # Créer une instance du formulaire avec les données soumises et l'objet client existant
        profile_form = ProfileUpdateForm(request.POST, instance=client)
        
        # Valider le formulaire
        if profile_form.is_valid():
            # Sauvegarder les données du formulaire
            profile_form.save()
            messages.success(request, 'Informations mises à jour avec succès.')
            return redirect('mon_compte')  # Rediriger vers la même page après la soumission

    else:
        # Si la requête n'est pas un POST, initialiser le formulaire avec les données actuelles du client
        profile_form = ProfileUpdateForm(instance=client)

    # Rendre le template avec le formulaire et l'objet client
    return render(request, 'front_end/profil.html', {
        'profile_form': profile_form,
        'client': client  # Passe l'objet client au template si nécessaire
    })

@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Vérification du mot de passe actuel
        if not request.user.check_password(old_password):
            messages.error(request, "Le mot de passe actuel est incorrect.")
            return redirect('mon_compte')

        # Vérification que les nouveaux mots de passe correspondent
        if new_password1 != new_password2:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
            return redirect('mon_compte')

        # Vérification des critères de sécurité du mot de passe (par exemple longueur minimale)
        if len(new_password1) < 8:
            messages.error(request, "Le nouveau mot de passe doit contenir au moins 8 caractères.")
            return redirect('mon_compte')

        # Si tout est correct, on change le mot de passe
        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Garde l'utilisateur connecté après la modification du mot de passe
        messages.success(request, "Votre mot de passe a été changé avec succès.")
        return redirect('mon_compte')

    return render(request, 'front_end/profil.html')

# vue pour la page contact
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
        full_message = f"Bonjour {nom},\n\nNous avons bien reçu votre message concernant \"{objet}\" et nous vous répondrons dans les plus brefs délais.\n\nCordialement,\nL'équipe de support."

        # Envoie l'email
        send_mail(
            subject=f"Confirmation de réception de votre message",
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
    queryset = Client.objects.select_related('user').all()
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

class CancelReservationAPIView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        reservation.status = 'annulée'  # Mettez à jour le statut ici
        reservation.save()  # Enregistrez les modifications

        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

