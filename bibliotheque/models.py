
from django.db import models


class Membre(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom




class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('DVD', 'DVD'),
        ('CD', 'CD'),
        ('JeuDePlateau', 'Jeu de Plateau'),
    ]

    titre = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} ({self.type})"




class Emprunt(models.Model):
    objects = None
    membre = models.ForeignKey('Membre', on_delete=models.CASCADE)
    media = models.ForeignKey('Media', on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membre.nom} a emprunté {self.media.titre}"
