from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import MembreForm, MediaForm, LivreForm, CDForm, DVDForm, JeuDePlateauForm
from .models import Media, Emprunt, Membre, Livre, CD, DVD
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
from django.http import HttpResponseBadRequest







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
    messages.success(request, "Le système de messages fonctionne correctement !")
    medias = Media.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        media_id = request.POST.get('media_id')

        if not media_id:
            return HttpResponseBadRequest("media_id manquant")

        media = get_object_or_404(Media, id=media_id)

        if action == "emprunter":
            membre_id = request.POST.get('membre_id')

            if not membre_id:
                return HttpResponseBadRequest("membre_id manquant")

            membre = get_object_or_404(Membre, id=membre_id)
            success, message = Emprunt.emprunter_media(membre, media)

            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

        elif action == "rendre":
            success, message = Emprunt.rendre_media(media.id)

            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

        else:
            return HttpResponseBadRequest("Action non reconnue")

    elif request.method != 'GET':
        return HttpResponseBadRequest("Méthode non autorisée")

    return render(request, 'bibliotheque/liste_medias.html', {
        'medias': medias,
        'membres': Membre.objects.all()
    })


def emprunter_media(request):
    print("📥 POST reçu dans la vue emprunter_media")

    if request.method == "POST":
        media_id = request.POST.get("media_id")
        membre_id = request.POST.get("membre_id")

        print(f"🎯 media_id = {media_id}, membre_id = {membre_id}")

        # Vérification des IDs
        if not media_id or not membre_id:
            messages.error(request, "Données manquantes.")
            return redirect('liste_medias')

        # Nouvelle étape : retrouver l'instance de média à partir de l'ID, en vérifiant dans les sous-classes
        media = None
        for Model in [Livre, CD, DVD]:  # ajoute ici toutes tes classes concrètes
            try:
                media = Model.objects.get(id=media_id)
                print(f"📚 Média trouvé : {media} (type {Model.__name__})")
                break
            except Model.DoesNotExist:
                continue

        if media is None:
            messages.error(request, "Le média demandé n'existe pas.")
            return redirect('liste_medias')

        # Appel de la méthode d’emprunt, que l'on adaptera ensuite si besoin
        success, message = Emprunt.emprunter_media(membre_id, media.id)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect('liste_medias')

    return redirect('liste_medias')





def rendre_media(request, media_id):
    print(f"📤 Requête pour rendre le média ID = {media_id}")

    # Étape 1 : Retrouver le média depuis l'ID dans les sous-classes
    media = None
    for Model in [Livre, CD, DVD]:
        try:
            media = Model.objects.get(id=media_id)
            print(f"📦 Média à rendre trouvé : {media} (type {Model.__name__})")
            break
        except Model.DoesNotExist:
            continue

    if media is None:
        messages.error(request, "Le média à rendre est introuvable.")
        return redirect('liste_medias')

    # Étape 2 : Appeler la méthode de rendu avec l'ID du média
    success, message = Emprunt.rendre_media(media.id)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('liste_medias')




def verifier_emprunts_en_retard_view(request):
    Emprunt.verifier_emprunts_en_retard()  # Appel de la méthode dans le modèle

    messages.success(request, "Tous les emprunts en retard ont été vérifiés et les membres bloqués si nécessaire.")
    return redirect('liste_medias')



def ajouter_media(request, type_media):
    form_classes = {
        'livre': LivreForm,
        'cd': CDForm,
        'dvd': DVDForm,
        'jeu': JeuDePlateauForm
    }

    FormClass = form_classes.get(type_media.lower())

    if not FormClass:
        messages.error(request, "Type de média invalide.")
        return redirect('liste_medias')

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{type_media.capitalize()} ajouté avec succès.")
            return redirect('liste_medias')
        else:
            messages.error(request, f"Erreur lors de l'ajout du {type_media}.")
    else:
        form = FormClass()

    return render(request, 'bibliotheque/ajouter_media.html', {'form': form, 'type': type_media})






def supprimer_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    media.delete()
    return redirect('liste_medias')


def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    membre.delete()
    messages.success(request, "Le membre a été supprimé avec succès.")
    return redirect('liste_membres')




def superuser_required(view_func):
    decorated = user_passes_test(lambda u: u.is_superuser)(view_func)
    decorated = login_required(decorated)
    return decorated



