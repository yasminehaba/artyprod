from django.shortcuts import get_object_or_404, redirect, render
from agence import settings
from artyprod.forms import ContactForm, EquipeForm, LoginForm, PersonnelForm, ProjetForm, ProjetRealiseeForm

from artyprod.models import Equipe, Personnel, Projet, ProjetRealisee,Service,ServiceProjet
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
@login_required
def mes_projets(request):
    user = request.user
    projets = Projet.objects.filter(client=user)
    context = {
        'projets': projets
    }
    return render(request, 'mes_projets.html', context)
def detail_projet(request, projet_id):
    # Logique pour récupérer les détails du projet avec l'ID `projet_id`
    projet = Projet.objects.get(id=projet_id)
    
    return render(request, 'detail_projet.html', {'projet': projet})
def projets_en_cours(request):
    projets = Projet.objects.filter(utilisateur=request.user, etat_realisation='en_cours')
    return render(request, 'projets_en_cours.html', {'projets': projets})
# def demander_projet(request):
#     if request.method == 'POST':
#         form = ProjetForm(request.POST)
#         if form.is_valid():
#             projet = form.save(commit=False)
#             nom_projet = form.cleaned_data['nom']
#             services_projet = form.cleaned_data['services']
#             projet.save()
#             return render(request, 'page_succes.html', {'nom_projet': nom_projet, 'services_projet': services_projet})
#     else:
#         form = ProjetForm()
    
#     return render(request, 'demande_projet.html', {'form': form})
from .forms import DemandeProjetForm, ProjetForm
from .models import DemandeProjet, ProjetAccepte

@login_required
def accepter_projet(request, demande_id):
    if not request.user.is_superuser:
        return redirect('accueil')  # Redirige les utilisateurs non superutilisateurs vers une autre page
    
    demande = DemandeProjet.objects.get(id=demande_id)
    
    projet_accepte = ProjetAccepte.objects.create(
        demande_projet=demande,
        nom=demande.nom,
        services=demande.services,
        FichierProjet=demande.FichierProjet
    )
    
    demande.delete()
    
    return redirect('projets')  # Redirige vers la page des projets
@login_required
def liste_demandes_projet(request):
    if not request.user.is_superuser:
        return redirect('accueil')  # Redirige les utilisateurs non superutilisateurs vers une autre page
    
    demandes = DemandeProjet.objects.all()
    context = {'demandes': demandes}
    return render(request, 'liste_demandes_projet.html', context)
def demander_projet(request):
    if request.method == 'POST':
        form = DemandeProjetForm(request.POST, request.FILES)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.client = request.user
            projet.save()

            demande_projet = DemandeProjet.objects.create(
                client=request.user,
                nom=projet.nom,
                services=projet.services,
                FichierProjet=projet.FichierProjet
            )
            
            return render(request, 'page_succes.html')
    else:
        form = DemandeProjetForm()
    
    return render(request, 'demande_projet.html', {'form': form})
def page_succes(request):
    return render(request, 'page_succes.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Enregistrer les données du formulaire dans la base de données
            form_data = form.save(commit=False)
            form_data.save()

            # Envoyer un e-mail avec les données du formulaire
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            message_body = f"Email: {email}\nSubject: {subject}\nMessage: {message}"

            send_mail(
                'Contact Form Submission',
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                ['yesmine0203@gmail.com'], # l'adresse de l'email de destination
                fail_silently=False,
            )

            return redirect('home')  # ou une autre page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Connecté en tant que {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Identifiants invalides.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)
            messages.success(
                request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def TtPersonnel(request):
        personnels= Personnel.objects.all()
        context={'personnels':personnels}
        return render( request,'personnels/personnels.html',context )

def personnel(request):
       
    if request.method == "POST":
        form = PersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            personnels = Personnel.objects.all()
            return render(request, 'personnels/personnels.html', {'personnels': personnels})
    else:
        form = PersonnelForm()
    personnels = Personnel.objects.all()
    return render(request, 'personnels/create_prs.html', {'form': form, 'personnels': personnels})

def delete_personnel(request, pk):
    msg = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        msg.delete()
        return redirect('TtPersonnel')
    return render(request, 'personnels/delete_prs.html', {'msg': msg})

def detail_personnel(request, prs_id):
    personnel = get_object_or_404(Personnel, id=prs_id)
    context = {'personnel': personnel}
    return render(request, 'personnels/detail_prs.html', context)


def edit_personnel(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('TtPersonnel')
    else:
        form = PersonnelForm(instance=personnel)
    return render(request, 'personnels/edit_prs.html', {'form': form})
# *******************************************************************************
def create_equipe(request):
     if request.method == "POST" :
         form = EquipeForm(request.POST)
         if form.is_valid():
              form.save() 
              equipes=Equipe.objects.all()
              
              return render(request,'equipes/equipes.html',{'equipes':equipes})
     else : 
            form = EquipeForm() #créer formulaire vide 
            equipes=Equipe.objects.all()
            return render(request,'equipes/create_equipe.html',{'form':form,'equipes':equipes})


def detail_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    context = {'equipe': equipe}
    return render(request, 'equipes/detail_equipe.html', context)


def edit_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    if request.method == 'POST':
        form = EquipeForm(request.POST, instance=equipe)
        if form.is_valid():
            form.save()
            return redirect('list_equipes')
    else:
        form = EquipeForm(instance=equipe)
        return render(request, 'equipes/edit_equipe.html',{'form': form})


def delete_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    if request.method == 'POST':
        equipe.delete()
        return redirect('list_equipes')
    return render(request, 'equipes/delete_equipe.html', {'equipe': equipe})


def list_equipes(request):
    equipes = Equipe.objects.all()
    context = {'equipes': equipes}
    return render(request, 'equipes/equipes.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Projet, ProjetRealisee
# *************************************************************************
def TtProjet(request):
    if request.method == 'POST':
        
        projet_id = request.POST.get('projet_id')
        projet = Projet.objects.get(id=projet_id)
        projet.realise = True
        projet.save()
        return redirect('portfolio')  # Rediriger vers la page du portfolio une fois le projet réalisé

    projets = Projet.objects.all()
    context = {'projets': projets}
    return render(request, 'projets/projets.html', context)

def projet(request):
       if request.method == "POST" :
         form = ProjetForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              projets=Projet.objects.all()

              return render(request,'projets/projets.html',{'projets':projets})
       else : 
            form = ProjetForm() #créer formulaire vide 
            projets=Projet.objects.all()
            return render(request,'projets/create_projets.html',{'form':form,'projets':projets})

def delete_projet(request, proj_id):
    prj = get_object_or_404(Projet, id=proj_id)
    if request.method == 'POST':
        prj.delete()
        return redirect('TtProjet')
    return render(request, 'projets/delete_projets.html', {'prj': prj})

def detail_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {'projet': projet}
    return render(request, 'projets/detail_projets.html', context)


def edit_projet(request, proj_id):
    projet = get_object_or_404(Projet, id=proj_id)
    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('TtProjet')
    else:
        form = ProjetForm(instance=projet)
    return render(request, 'projets/edit_projets.html', {'form': form})





def projetrealisee(request):

    if request.method == "POST":
        form = ProjetRealiseeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            projetrealisees = ProjetRealisee.objects.all()
            return render(request, 'projetrealisees/projetrealisees.html', {'projetrealisees': projetrealisees})
    else:
        form = ProjetRealiseeForm()
    projetrealisees = ProjetRealisee.objects.all()
    return render(request, 'projetrealisees/create_projetrealisee.html', {'form': form, 'projetrealisees': projetrealisees})

def delete_projetrealise(request, prjr_id):
    prjr = get_object_or_404(ProjetRealisee, id=prjr_id)
    if request.method == 'POST':
        prjr.delete()
        return redirect('TtProjetRealisee')
    return render(request, 'personnels/delete_projetrealisee.html', {'prjr': prjr})

def detail_projetrealisee(request, prr_id):
    projetrealisee = get_object_or_404(ProjetRealisee, id=prr_id)
    context = {'projetrealisee': projetrealisee}
    return render(request, 'projetrealisee/detail_projetrealisee.html', context)


def edit_projetrealisee(request, prjr_id):
    projetrealisee = get_object_or_404(ProjetRealisee, id=prjr_id)
    if request.method == 'POST':
        form = ProjetRealiseeForm(request.POST, request.FILES, instance=projetrealisee)
        if form.is_valid():
            form.save()
            return redirect('TtProjetRealisee')
    else:
        form = ProjetRealiseeForm(instance=projetrealisee)
    return render(request, 'projetrealisees/edit_projetrealisee.html', {'form': form})
def TtProjetRealisee(request):
        projetrealisees= ProjetRealisee.objects.all()
        context={'projetrealisees':projetrealisees}
        return render( request,'projetrealisees/projetrealisees.html',context )


def projetrealisee(request):

    if request.method == "POST":
        form = ProjetRealiseeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            projetrealisees = ProjetRealisee.objects.all()
            return render(request, 'projetrealisees/projetrealisees.html', {'projetrealisees': projetrealisees})
    else:
        form = ProjetRealiseeForm()
    projetrealisees = ProjetRealisee.objects.all()
    return render(request, 'projetrealisees/create_projetrealisee.html', {'form': form, 'projetrealisees': projetrealisees})

def delete_projetrealise(request, prjr_id):
    prjr = get_object_or_404(ProjetRealisee, id=prjr_id)
    if request.method == 'POST':
        prjr.delete()
        return redirect('TtProjetRealisee')
    return render(request, 'personnels/delete_projetrealisee.html', {'prjr': prjr})

def detail_projetrealisee(request, prr_id):
    projetrealisee = get_object_or_404(ProjetRealisee, id=prr_id)
    context = {'projetrealisee': projetrealisee}
    return render(request, 'projetrealisees/detail_projetrealisee.html', context)


def edit_projetrealisee(request, prjr_id):
    projetrealisee = get_object_or_404(ProjetRealisee, id=prjr_id)
    if request.method == 'POST':
        form = ProjetRealiseeForm(request.POST, request.FILES, instance=projetrealisee)
        if form.is_valid():
            form.save()
            return redirect('TtProjetRealisee')
    else:
        form = ProjetRealiseeForm(instance=projetrealisee)
    return render(request, 'projetrealisees/edit_projetrealisee.html', {'form': form})


def portfolio(request):
    projetsrealises = Projet.objects.filter(realise=True)
    return render(request, 'portfolio.html', {'projetsrealises': projetsrealises})
def realiser_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    
    if projet.realise:
        # Le projet est déjà réalisé
        # Vous pouvez afficher un message d'erreur ou rediriger vers une autre page
        pass
    else:
        # Créer un nouveau projet réalisé à partir du projet existant
        ProjetRealisee.objects.create(
            nom=projet.nom,
            description=projet.description,
            photoPrj=projet.photoPrj,
            # Autres champs à copier depuis le projet d'origine
        )
        # Marquer le projet d'origine comme réalisé
        projet.realise = True
        projet.save()
        
    return redirect('portfolio')