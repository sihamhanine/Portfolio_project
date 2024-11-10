from .imports import *  # Importe les modules nécessaires

class ReservationForm(forms.ModelForm):
    """
    Formulaire pour la création et la gestion des réservations.
    
    Cette classe hérite de ModelForm et permet de créer ou modifier une réservation.
    Elle inclut des champs comme le client, le service, l'adresse du client, et les dates de début et de fin de la réservation.
    
    Attributs:
        model (class): Le modèle utilisé pour ce formulaire (Reservation).
        fields (list): Les champs du modèle à inclure dans le formulaire.
        widgets (dict): Personnalisation des widgets pour les champs de date (utilisation d'un champ de type 'date').
    """
    class Meta:
        model = Reservation
        fields = ['client', 'client_address', 'service', 'service_description', 'datetime_start', 'datetime_end']
        widgets = {
            'datetime_start': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'datetime_end': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['datetime_start'].input_formats = ['%Y-%m-%d']
        self.fields['datetime_end'].input_formats = ['%Y-%m-%d']


class SignUpForm(UserCreationForm):
    """
    Formulaire pour l'inscription d'un utilisateur (création d'un compte).
    
    Ce formulaire permet de créer un utilisateur avec son email, son nom, son numéro de téléphone, 
    son adresse, et son mot de passe. Il valide aussi que l'email et le nom d'utilisateur sont uniques.
    
    Attributs:
        email (EmailField): Champ pour l'adresse e-mail de l'utilisateur.
        name (CharField): Champ pour le nom complet de l'utilisateur.
        phone (CharField): Champ pour le numéro de téléphone de l'utilisateur.
        address (CharField): Champ pour l'adresse de l'utilisateur.
        password1 (CharField): Champ pour le mot de passe de l'utilisateur.
        password2 (CharField): Champ pour confirmer le mot de passe.
    
    Méthodes:
        save: Crée l'utilisateur et son client associé dans la base de données.
        clean_email: Vérifie que l'adresse e-mail est unique dans la base de données.
        clean_username: Vérifie que le nom d'utilisateur est unique dans la base de données.
    """
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        label="Adresse e-mail",
        error_messages={
            'required': "L'adresse e-mail est obligatoire.",
            'invalid': "Veuillez entrer une adresse e-mail valide."
        }
    )
    name = forms.CharField(
        max_length=50, 
        label="Nom complet", 
        required=True,
        error_messages={
            'required': "Le nom complet est obligatoire."
        }
    )
    phone = forms.CharField(
        max_length=15, 
        label="Numéro de téléphone", 
        required=True,
        error_messages={
            'required': "Le numéro de téléphone est obligatoire."
        }
    )
    address = forms.CharField(
        max_length=255, 
        label="Adresse", 
        required=True,
        error_messages={
            'required': "L'adresse est obligatoire."
        }
    )
    password1 = forms.CharField(
        label="Mot de passe", 
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={
            'required': "Le mot de passe est obligatoire."
        }
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe", 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={
            'required': "Veuillez confirmer votre mot de passe.",
            'password_mismatch': "Les deux champs de mot de passe ne correspondent pas."
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Champs de l'utilisateur
        labels = {
        'username': 'Nom d’utilisateur',
        'email': 'Adresse e-mail',
        }
        error_messages = {
            'username': {
                'required': "Le nom d'utilisateur est obligatoire.",
                'unique': "Ce nom d'utilisateur est déjà pris."
            },
            'email': {
                'unique': "Cette adresse e-mail est déjà utilisée."
            }
        }

    def save(self, commit=True):
        """
        Sauvegarde l'utilisateur et crée un client associé.
        
        Crée un utilisateur à partir des données du formulaire, puis crée un objet Client associé à cet utilisateur.
        
        Args:
            commit (bool): Si True, l'objet Client sera enregistré dans la base de données.
        
        Returns:
            user (User): L'utilisateur créé.
        """
        user = super(SignUpForm, self).save(commit=commit)  # Crée l'utilisateur
        # Crée le Client associé
        client = Client(
            user=user,  # Associe le client au user créé
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address']
        )
        if commit:
            client.save()  # Sauvegarder le client
        return user  # Retourne l'utilisateur créé

    def clean_email(self):
        """
        Vérifie si l'email est déjà utilisé dans la base de données.
        
        Si l'email est déjà utilisé, une ValidationError est levée.
        
        Returns:
            email (str): L'adresse email nettoyée.
        
        Raises:
            ValidationError: Si l'email est déjà pris.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def clean_username(self):
        """
        Vérifie si le nom d'utilisateur est déjà pris.
        
        Si le nom d'utilisateur existe déjà dans la base de données, une ValidationError est levée.
        
        Returns:
            username (str): Le nom d'utilisateur nettoyé.
        
        Raises:
            ValidationError: Si le nom d'utilisateur est déjà pris.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour le profil d'un utilisateur.
    
    Ce formulaire permet à un utilisateur de mettre à jour son nom, son numéro de téléphone et son adresse.
    
    Attributs:
        model (class): Le modèle associé à ce formulaire (Client).
        fields (list): Les champs du modèle à inclure dans le formulaire.
        widgets (dict): Widgets personnalisés pour l'affichage des champs du formulaire.
    """
    class Meta:
        model = Client
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
        }