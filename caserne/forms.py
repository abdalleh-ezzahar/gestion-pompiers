from django import forms
from django.contrib.auth.models import User
from .models import Vehicule, Intervention, Materiel


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['code_radio', 'marque', 'type_vehicule', 'immatriculation', 'kilometrage', 'statut']
        labels = {
            'marque': 'Marque',
            'type_vehicule': 'Type de véhicule',
        }
        widgets = {
            'code_radio': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-select'}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
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
    type_vehicule = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Vehicule.TYPE_VEHICULE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Vehicule.STATUS_CHOICES,
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


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Confirmer mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
