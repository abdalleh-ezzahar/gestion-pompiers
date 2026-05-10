from django import forms
from .models import Vehicule, Materiel, Intervention, TypeEngin


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['code_radio', 'type_engin', 'immatriculation', 'statut', 'km']
        widgets = {
            'code_radio': forms.TextInput(attrs={'class': 'form-control'}),
            'type_engin': forms.Select(attrs={'class': 'form-select'}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'Type Vehicule': forms.Select(attrs={'class': 'form-select'}),
        }


class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = ['nom', 'description', 'quantite', 'date_revision', 'vehicule']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vehicule': forms.Select(attrs={'class': 'form-select'}),
        }


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['numero_rapport', 'type_sinistre', 'adresse', 'date_appel', 'duree', 'vehicules', 'notes']
        widgets = {
            'numero_rapport': forms.TextInput(attrs={'class': 'form-control'}),
            'type_sinistre': forms.Select(attrs={'class': 'form-select'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'date_appel': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duree': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicules': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VehiculeFilterForm(forms.Form):
    type_engin = forms.ModelChoiceField(
        queryset=TypeEngin.objects.all(),
        required=False,
        empty_label="Tous les types",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Vehicule.STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class InterventionFilterForm(forms.Form):
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Du"
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Au"
    )
    type_sinistre = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Intervention.TYPE_SINISTRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Type"
    )