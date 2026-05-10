from django.db import models


class Vehicule(models.Model):

    TYPE_VEHICULE_CHOICES = [
        ('FPT', 'Fourgon Pompe Tonne'),
        ('VSAV', 'Véhicule de Secours et d’Assistance aux Victimes'),
        ('EPA', 'Échelle Pivotante Automatique'),
    ]

    STATUS_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Intervention', 'En intervention'),
        ('Indisponible', 'Indisponible'),
    ]

    code_radio = models.CharField(max_length=50)
    marque = models.CharField(max_length=100)
    type_vehicule = models.CharField(max_length=100, choices=TYPE_VEHICULE_CHOICES)
    immatriculation = models.CharField(max_length=50)
    kilometrage = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.code_radio

    @property
    def badge_label(self):
        return self.statut

    @property
    def badge_class(self):
        return {
            'Disponible': 'badge-disponible',
            'Intervention': 'badge-en_intervention',
            'Indisponible': 'badge-indisponible',
        }.get(self.statut, 'badge-secondary')

    @property
    def km(self):
        return self.kilometrage


class Materiel(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    quantite = models.PositiveIntegerField(default=1)
    date_revision = models.DateField(null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='materiels')

    def __str__(self):
        return self.nom


class Intervention(models.Model):

    TYPE_CHOICES = [
        ('Incendie', 'Incendie'),
        ('Accident', 'Accident'),
        ('Secours', 'Secours à personne'),
    ]
    TYPE_SINISTRE_CHOICES = TYPE_CHOICES

    numero_rapport = models.CharField(max_length=100)
    type_sinistre = models.CharField(max_length=50, choices=TYPE_CHOICES)
    adresse = models.CharField(max_length=255)
    date_appel = models.DateTimeField()
    duree = models.IntegerField(help_text='Durée en minutes')
    notes = models.TextField(blank=True)

    vehicules = models.ManyToManyField(Vehicule)

    def __str__(self):
        return self.numero_rapport

    @property
    def badge_class(self):
        return {
            'Incendie': 'bg-danger',
            'Accident': 'bg-warning',
            'Secours': 'bg-success',
        }.get(self.type_sinistre, 'bg-secondary')
