from django import forms
from .models import Reservation, Client
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client', 'client_address', 'service', 'service_description', 'datetime_start', 'datetime_end']
        widgets = {
            'datetime_start': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'datetime_end': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['datetime_start'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['datetime_end'].input_formats = ['%Y-%m-%dT%H:%M']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, label="Adresse e-mail")
    name = forms.CharField(max_length=50, label="Nom complet", required=True)
    phone = forms.CharField(max_length=15, label="Numéro de téléphone", required=True)
    address = forms.CharField(max_length=255, label="Adresse", required=True)
    password1 = forms.CharField(
        label="Mot de passe", 
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe", 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Champs de l'utilisateur
        labels = {
        'username': 'Nom d’utilisateur',
        'email': 'Adresse e-mail',
    }

    def save(self, commit=True):
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
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username