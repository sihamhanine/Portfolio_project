# Imports de bibliothèques Python standards
import csv
from datetime import datetime


# Imports des packages Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.cache import never_cache, cache_control
from django.core.cache import cache
from django.forms.widgets import DateInput
from django import forms
from django.utils.dateparse import parse_datetime


# Imports de packages tiers
from rest_framework import generics
from dateutil import parser

# Imports de vos modules ou applications Django (fichiers internes)
from .models import Client, Service, Reservation, Devis, Contact
from .serializers import ClientSerializer, ServiceSerializer, ReservationSerializer, DevisSerializer, ContactSerializer
from .forms import ReservationForm, ProfileUpdateForm, SignUpForm






