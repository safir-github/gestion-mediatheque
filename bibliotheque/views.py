
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

            if media.disponible:
                Emprunt.objects.create(membre=membre, media=media)
                media.disponible = False
                media.save()

        elif action == "rendre":
            emprunt = Emprunt.objects.filter(media=media).first()
            if emprunt:
                media.disponible = True
                media.save()
                emprunt.date_retour = now()
                emprunt.save()
                emprunt.delete()

    return render(request, 'bibliotheque/liste_medias.html', {'medias': medias, 'membres': Membre.objects.all()})






def emprunter_media(request):
    if request.method == "POST":
        media_id = request.POST.get("media_id")
        membre_id = request.POST.get("membre_id")

        # Vérifier que les ID existent
        if not media_id or not membre_id:
            messages.error(request, "Données manquantes.")
            return redirect('liste_medias')

        media = get_object_or_404(Media, id=media_id, disponible=True)
        membre = get_object_or_404(Membre, id=membre_id)

        # ✅ Vérification 1 : Bloquer les jeux de plateau
        if "jeu" in media.type.lower():
            messages.error(request, "Les jeux de plateau ne peuvent pas être empruntés.")
            return redirect('liste_medias')

        # ✅ Vérification 2 : Limite de 3 emprunts par membre
        if Emprunt.objects.filter(membre=membre, date_retour__isnull=True).count() >= 3:
            messages.error(request, "Ce membre a déjà atteint la limite de 3 emprunts.")
            return redirect('liste_medias')

        # ✅ Vérification 3 : Emprunts en retard
        date_limite = timezone.now() - timedelta(days=7)
        emprunts_actifs = Emprunt.objects.filter(membre=membre, date_retour__isnull=True)
        if emprunts_actifs.filter(date_emprunt__lte=date_limite).exists():
            messages.error(request, "Ce membre a un emprunt en retard et ne peut pas emprunter.")
            return redirect('liste_medias')

        # ✅ Créer l'emprunt et mettre à jour le statut du média
        Emprunt.objects.create(membre=membre, media=media)
        media.disponible = False
        media.save()

        messages.success(request, f"{media.titre} a été emprunté avec succès.")
        return redirect('liste_medias')

    return redirect('liste_medias')



def rendre_media(request, media_id):
    media = get_object_or_404(Media, id=media_id, disponible=False)
    emprunt = Emprunt.objects.filter(media=media, date_retour__isnull=True).first()

    if emprunt:
        emprunt.date_retour = timezone.now()  # ✅ Marquer l’emprunt comme rendu
        emprunt.save()
        media.disponible = True  # ✅ Rendre le média disponible à nouveau
        media.save()
        messages.success(request, f"{media.titre} a été rendu avec succès.")

    return redirect('liste_medias')



def verifier_emprunts_en_retard():
    date_limite = timezone.now() - timedelta(days=7)
    emprunts_en_retard = Emprunt.objects.filter(date_retour__isnull=True, date_emprunt__lte=date_limite)

    for emprunt in emprunts_en_retard:
        emprunt.membre.bloque = True  # ✅ Bloquer le membre
        emprunt.membre.save()



def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')  # Redirige vers la liste des médias après l'ajout
    else:
        form = MediaForm()

    return render(request, 'bibliotheque/ajouter_media.html', {'form': form})









