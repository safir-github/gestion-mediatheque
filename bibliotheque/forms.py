from django import forms
from .models import Membre, Media, Emprunt, Livre, CD, DVD, JeuDePlateau

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'email', 'bloque']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'disponible']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['membre', 'media']


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre']  # adapte selon tes champs

class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['titre',]  # adapte selon tes champs

class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['titre']  # adapte selon tes champs

class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['titre']  # adapte selon tes champs