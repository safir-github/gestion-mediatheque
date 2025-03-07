from django.urls import path
from .views import liste_membres, modifier_membre, liste_medias, emprunter_media, ajouter_media # Import de la vue
from . import views




urlpatterns = [
    path('membres/', liste_membres, name='liste_membres'),
    path('membres/ajouter/', views.ajouter_membre, name='ajouter_membre'),

    path('membres/modifier/<int:membre_id>/', modifier_membre, name='modifier_membre'),
    path('medias/', liste_medias, name='liste_medias'),
    path('emprunter/', emprunter_media, name='emprunter_media'),
    path('ajouter-media/', ajouter_media, name='ajouter_media'),






]

