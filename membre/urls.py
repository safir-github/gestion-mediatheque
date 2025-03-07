from django.urls import path
from bibliotheque.views import liste_medias  # Import depuis bibliotheque

urlpatterns = [
    path('medias/', liste_medias, name='liste_medias_membre'),  # Réutilisation de la vue existante
]
