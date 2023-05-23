from datetime import date
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User





class DemandeProjet(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    services = models.CharField(max_length=100)
    FichierProjet = models.FileField(upload_to='FichierProjet/', blank=True, null=True)

    def __str__(self):
        return f"{self.client.username} - Demande de projet"


class ProjetAccepte(models.Model):
    demande_projet = models.OneToOneField(DemandeProjet, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    services = models.CharField(max_length=100)
    FichierProjet = models.FileField(upload_to='FichierProjet', blank=True, null=True)

    def __str__(self):
        return f"{self.demande_projet.client.username} - Projet accepté"

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email valide.")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    nom = models.CharField(max_length=100, default="")
    prenom = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Personnel(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    photo = models.ImageField(upload_to='photosProfil/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    date_affectation = models.DateField(null=True, default=date.today)
    profil_linkedin_ou_site_personnel = models.URLField(blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Equipe(models.Model):
    nom = models.CharField(max_length=255)
    membres = models.ManyToManyField(Personnel, related_name='equipes')


    def __str__(self):
        return self.nom

class Message(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.nom


class Projet(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_demandes',null=True)
    nom = models.CharField(max_length=255,default="")
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True)
    services = models.ForeignKey('Service', on_delete=models.CASCADE, null=True)
    TYPE_CHOICES=[  ('Charte graphique ','Charte graphique '),
                    ('Objet  3D ','Objet  3D '),
                    ('Scénarisation','Scénarisation')]
    equipe = models.ForeignKey('Equipe', on_delete=models.CASCADE, null=True)
    FichierProjet  = models.ImageField(upload_to='FichierProjet/', blank=True, null=True)
    realise = models.BooleanField(default=False)
    projet_accepte = models.OneToOneField('ProjetAccepte', on_delete=models.CASCADE, null=True, blank=True)
    @classmethod
    def get_projets_non_realises(cls):
        return cls.objects.filter(realise=False)

    def __str__(self):
        return self.nom
    
class Portfolio(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    FichierProjet  = models.ImageField(upload_to='FichierProjet/', blank=True, null=True)
    
class Service(models.Model):
    TYPE_CHOICES=[
    ('Charte graphique ','Charte graphique '),
                    ('Objet  3D ','Objet  3D '),
                    ('Scénarisation','Scénarisation'),
    ]

    name=models.CharField(max_length=50,default='Charte graphique ',choices=TYPE_CHOICES)



    def __str__(self):
        return self.name
    
    
class ProjetRealisee(models.Model):
    nom = models.CharField(max_length=255,default="")
    services = models.ForeignKey('Service', on_delete=models.CASCADE, null=True)
    TYPE_CHOICES=[  ('Charte graphique ','Charte graphique '),
                    ('Objet  3D ','Objet  3D '),
                    ('Scénarisation','Scénarisation')]
    
    FichierProjet  = models.ImageField(upload_to='FichierProjet/', blank=True, null=True)
    
    

    def __str__(self):
        return self.nom

class ServiceProjet(models.Model):
    TYPE_CHOICES=[
    ('Charte graphique ','Charte graphique '),
                    ('Objet  3D ','Objet  3D '),
                    ('Scénarisation','Scénarisation'),
    ]

    name=models.CharField(max_length=50,default='Charte graphique ',choices=TYPE_CHOICES)
    projet  = models.ManyToManyField(ProjetRealisee , related_name='projets')


    def __str__(self):
        return self.name