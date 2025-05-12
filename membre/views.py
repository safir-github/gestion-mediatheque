from django.shortcuts import render, redirect
from bibliotheque.models import Media  # Import du modèle Media
from django.contrib.auth import authenticate, login
from django.contrib import messages


def liste_medias(request):
    medias = Media.objects.all()  # Récupérer tous les médias

    return render(request, 'membre/liste_medias.html', {'medias': medias})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Vérifier le groupe ou le type d'utilisateur
            if user.is_superuser:
                return redirect("/bibliotheque/medias")  # Redirige vers l'administration
            else:
                return redirect("/membre/")  # Redirige vers l'espace membre
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "membre/login.html")