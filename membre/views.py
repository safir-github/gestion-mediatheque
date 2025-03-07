from django.shortcuts import render
from bibliotheque.models import Media  # Import du modèle Media


def liste_medias(request):
    medias = Media.objects.all()  # Récupérer tous les médias

    return render(request, 'membre/liste_medias.html', {'medias': medias})
