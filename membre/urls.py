from django.urls import path
from membre.views import liste_medias # Import depuis bibliotheque
from .views import login_view

urlpatterns = [
    path('medias/', liste_medias, name='home_for_member'),  # Réutilisation de la vue existante
    path("login/", login_view, name="login"),
]
