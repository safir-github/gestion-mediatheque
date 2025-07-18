from django.urls import path
from .views import liste_membres, modifier_membre, liste_medias, emprunter_media, ajouter_media, rendre_media, supprimer_membre # Import de la vue
from . import views




urlpatterns = [
    path('membres/', liste_membres, name='liste_membres'),
    path('membres/ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('membres/modifier/<int:membre_id>/', modifier_membre, name='modifier_membre'),
    path('medias/', liste_medias, name='liste_medias'),
    path('emprunter/', emprunter_media, name='emprunter_media'),
    path('ajouter-media/<str:type_media>/', ajouter_media, name='ajouter_media'),
    path('rendre/<int:media_id>/', rendre_media, name='rendre_media'),
    path('supprimer-media/<int:media_id>/', views.supprimer_media, name='supprimer_media'),
    path('membre/supprimer/<int:membre_id>/', supprimer_membre, name='supprimer_membre'),

]

