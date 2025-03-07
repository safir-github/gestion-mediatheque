
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from .models import Membre
from .forms import MembreForm, MediaForm, EmpruntForm
from .models import Media, Emprunt





def liste_membres(request):
    membres = Membre.objects.all()  # Récupère tous les membres
    context = {
        'membres': membres
    }
    return render(request, 'bibliotheque/liste_membres.html', context)




def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)  # Récupère le membre ou affiche une erreur 404

    if request.method == "POST":
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')  # Redirection vers la liste après modification
    else:
        form = MembreForm(instance=membre)  # Pré-remplir le formulaire avec les données existantes

    return render(request, 'bibliotheque/modifier_membre.html', {'form': form, 'membre': membre})




def ajouter_membre(request):
    if request.method == "POST":
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')  # Redirection après l'ajout
    else:
        form = MembreForm()

    return render(request, 'bibliotheque/ajouter_membre.html', {'form': form})



def liste_medias(request):
    # Test de message
    messages.success(request, "Le système de messages fonctionne correctement !")

    medias = Media.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        media_id = request.POST.get('media_id')

        media = get_object_or_404(Media, id=media_id)

        if action == "emprunter":
            membre_id = request.POST.get('membre_id')
            membre = get_object_or_404(Membre, id=membre_id)

            # Utilisation de la méthode emprunter_media pour gérer l'emprunt
            success, message = Emprunt.emprunter_media(membre, media)

            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

        elif action == "rendre":
            # Utilisation de la méthode rendre_media pour gérer le retour
            success, message = Emprunt.rendre_media(media)

            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    return render(request, 'bibliotheque/liste_medias.html', {'medias': medias, 'membres': Membre.objects.all()})




def emprunter_media(request):
    if request.method == "POST":
        media_id = request.POST.get("media_id")
        membre_id = request.POST.get("membre_id")

        # Vérifier que les ID existent
        if not media_id or not membre_id:
            messages.error(request, "Données manquantes.")
            return redirect('liste_medias')

        # Utilisation de la méthode emprunter_media dans Emprunt
        success, message = Emprunt.emprunter_media(membre_id, media_id)

        # Affichage du message selon le résultat de l'emprunt
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect('liste_medias')

    return redirect('liste_medias')






def rendre_media(request, media_id):
    # Utiliser l'id du média, pas l'objet complet
    success, message = Emprunt.rendre_media(media_id)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('liste_medias')



def verifier_emprunts_en_retard_view(request):
    Emprunt.verifier_emprunts_en_retard()  # Appel de la méthode dans le modèle

    messages.success(request, "Tous les emprunts en retard ont été vérifiés et les membres bloqués si nécessaire.")
    return redirect('liste_medias')



def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde du média
            messages.success(request, "Le média a été ajouté avec succès.")  # Message de confirmation
            return redirect('liste_medias')  # Redirection vers la liste des médias après l'ajout
        else:
            messages.error(request, "Il y a eu une erreur lors de l'ajout du média.")  # Message d'erreur
    else:
        form = MediaForm()  # Créer un formulaire vide pour la vue GET

    return render(request, 'bibliotheque/ajouter_media.html', {'form': form})







