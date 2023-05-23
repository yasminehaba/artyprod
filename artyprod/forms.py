from multiprocessing import AuthenticationError
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Contact, Personnel
from artyprod.models import Equipe, Projet, ProjetRealisee, ServiceProjet


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'subject', 'message']

class LoginForm(AuthenticationError):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class PersonnelForm(ModelForm):
     class Meta : 
        model = Personnel
        fields = "__all__" #pour tous les champs de la table
class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom', 'membres']
        widgets = {
            'membres': forms.CheckboxSelectMultiple()
        }
class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceProjet
        fields = "__all__"
        widgets = {
            'projets': forms.CheckboxSelectMultiple()
        }
class ProjetForm(forms.ModelForm):


    class Meta:
        model = Projet
        fields = ['nom', 'services', 'FichierProjet','equipe']
class ProjetRealiseeForm(ModelForm):
     class Meta : 
        model = ProjetRealisee
        fields = "__all__" #pour tous les champs de la table
class DemandeProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'services', 'FichierProjet']


class ProjetAccepteForm(forms.ModelForm):
    projet_accepte = forms.BooleanField(required=False)

    class Meta:
        model = Projet
        fields = ['nom', 'services', 'FichierProjet', 'projet_accepte']