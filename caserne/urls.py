from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),

    path('vehicules/', views.vehicule_list, name='vehicule_list'),
    path('vehicules/create/', views.ajouter_vehicule, name='vehicule_create'),
    path('vehicules/<int:id>/', views.vehicule_detail, name='vehicule_detail'),
    path('vehicules/<int:id>/edit/', views.modifier_vehicule, name='vehicule_edit'),
    path('vehicules/<int:id>/delete/', views.supprimer_vehicule, name='vehicule_delete'),

    path('ajouter/', views.ajouter_vehicule, name='ajouter_vehicule'),
    path('modifier/<int:id>/', views.modifier_vehicule, name='modifier_vehicule'),
    path('supprimer/<int:id>/', views.supprimer_vehicule, name='supprimer_vehicule'),

    path('interventions/', views.intervention_list, name='intervention_list'),
    path('interventions/create/', views.ajouter_intervention, name='intervention_create'),
    path('interventions/<int:id>/', views.intervention_detail, name='intervention_detail'),

    path('materiels/', views.materiel_list, name='materiel_list'),
    path('materiels/create/', views.ajouter_materiel, name='materiel_create'),
    
    path('signup/', views.signup, name='signup'),
]