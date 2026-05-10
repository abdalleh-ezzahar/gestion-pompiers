from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Vehicule, Intervention, Materiel
from .forms import (
    VehiculeForm,
    InterventionForm,
    MaterielForm,
    VehiculeFilterForm,
    InterventionFilterForm,
    SignUpForm,
)


def landing(request):
   
    return render(request, 'landing.html')


def signup(request):
   
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    
    logout(request)
    return redirect('landing')


def dashboard(request):
    vehicules = Vehicule.objects.all()
    total_vehicules = vehicules.count()
    dispo = vehicules.filter(statut='Disponible').count()
    en_inter = vehicules.filter(statut='Intervention').count()
    maintenance = vehicules.filter(statut='Indisponible').count()
    dernieres_interventions = Intervention.objects.order_by('-date_appel')[:5]

    context = {
        'total_vehicules': total_vehicules,
        'dispo': dispo,
        'en_inter': en_inter,
        'maintenance': maintenance,
        'dernieres_interventions': dernieres_interventions,
    }
    return render(request, 'dashboard.html', context)


def home(request):
    return redirect('dashboard')


def vehicule_list(request):
    form = VehiculeFilterForm(request.GET or None)
    vehicules = Vehicule.objects.all()

    if form.is_valid():
        type_vehicule = form.cleaned_data.get('type_vehicule')
        if type_vehicule:
            vehicules = vehicules.filter(type_vehicule=type_vehicule)
        statut = form.cleaned_data.get('statut')
        if statut:
            vehicules = vehicules.filter(statut=statut)

    return render(request, 'vehicule_list.html', {'vehicules': vehicules, 'form': form})


def vehicule_detail(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)
    materiels = vehicule.materiels.all()
    interventions = Intervention.objects.filter(vehicules=vehicule).order_by('-date_appel')

    return render(request, 'vehicule_detail.html', {
        'vehicule': vehicule,
        'materiels': materiels,
        'interventions': interventions,
    })


def ajouter_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehiculeForm()

    return render(request, 'ajouter_vehicule.html', {'form': form})


def modifier_vehicule(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)

    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VehiculeForm(instance=vehicule)

    return render(request, 'modifier_vehicule.html', {'form': form})


def supprimer_vehicule(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)
    vehicule.delete()
    return redirect('dashboard')


def intervention_list(request):
    form = InterventionFilterForm(request.GET or None)
    interventions = Intervention.objects.prefetch_related('vehicules').all()

    if form.is_valid():
        if form.cleaned_data.get('type_sinistre'):
            interventions = interventions.filter(type_sinistre=form.cleaned_data['type_sinistre'])
        if form.cleaned_data.get('date_debut'):
            interventions = interventions.filter(date_appel__date__gte=form.cleaned_data['date_debut'])
        if form.cleaned_data.get('date_fin'):
            interventions = interventions.filter(date_appel__date__lte=form.cleaned_data['date_fin'])

    return render(request, 'intervention_list.html', {
        'interventions': interventions,
        'form': form,
    })


def intervention_detail(request, id):
    intervention = get_object_or_404(Intervention, id=id)
    return render(request, 'intervention_detail.html', {'intervention': intervention})


def ajouter_intervention(request):
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('intervention_list')
    else:
        form = InterventionForm()

    return render(request, 'intervention_form.html', {'form': form, 'title': 'Nouvelle intervention'})


def materiel_list(request):
    materiels = Materiel.objects.select_related('vehicule').all()
    return render(request, 'materiel_list.html', {'materiels': materiels})


def ajouter_materiel(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materiel_list')
    else:
        form = MaterielForm()

    return render(request, 'materiel_form.html', {'form': form, 'title': 'Ajouter du matériel'})
