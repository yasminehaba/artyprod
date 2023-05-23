from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
urlpatterns = [    

    path('login/', LoginView.as_view(), name='login'),
    path('register',register, name="register"),

    path('contact', views.contact, name='contact'),


    path('personnel/', views.personnel, name='personnel'),
    path('TtPersonnel/', views.TtPersonnel, name='TtPersonnel'),
    path('deletePersonnel/<int:pk>/', views.delete_personnel, name='delete_personnel'),
    path('Personnel/<int:prs_id>/', views.detail_personnel, name='detail_personnel'),
    path('editPersonnem/<int:pk>/', views.edit_personnel, name='edit_personnel'),


    path('Equipes', views.list_equipes, name='list_equipes'),
    path('createEquipe/', views.create_equipe, name='create_equipe'),
    path('<int:equipe_id>/detail_equipe', views.detail_equipe, name='detail_equipe'),
    path('<int:equipe_id>/edit_equipe/', views.edit_equipe, name='edit_equipe'),
    path('<int:equipe_id>/delete_equipe/', views.delete_equipe, name='delete_equipe'),


    path('Projets', views.TtProjet, name='TtProjet'),
    path('createProjet/', views.projet, name='projet'),
    path('artyprod/<int:projet_id>/detailProjet/', views.detail_projet, name='detail_projet'),
    path('<int:proj_id>/editProjet/', views.edit_projet, name='edit_projet'),
    path('<int:proj_id>/deleteProjet/', views.delete_projet, name='delete_projet'),

    path('ProjetsRealisses', views.TtProjetRealisee, name='TtProjetRealisee'),
    path('createProjetsRealisses/', views.projetrealisee, name='projetrealisee'),
    
    path('artyprod/<int:projr_id>/detailProjet/', views.detail_projetrealisee, name='detail_projetrealisee'),
    path('<int:prjr_id>/editProjetsRealisses/', views.edit_projetrealisee, name='edit_projetrealisee'),
    path('<int:prjr_id>/deleteProjetsRealisses/', views.delete_projetrealise, name='delete_projetrealise'),

    path('portfolio/', views.portfolio, name='portfolio'),
    path('realiser_projet/<int:projet_id>/', views.realiser_projet, name='realiser_projet'),

    path('demander_projet/', views.demander_projet, name='demander_projet'),
    path('page_succes/', views.page_succes, name='page_succes'),
    path('projets-en-cours/', views.projets_en_cours, name='projets_en_cours'),
    path('projet/<int:projet_id>/', views.detail_projet, name='detail_projet'),
    path('mes_projets/', views.mes_projets, name='mes_projets'),

    

    ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
