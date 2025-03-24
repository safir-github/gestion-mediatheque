from django import forms
from .models import Membre, Media, Emprunt

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'email', 'bloque']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'type', 'disponible']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media']
