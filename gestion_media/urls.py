from django.contrib import admin
from django.urls import path, include  # Import de include
from membre.views import liste_medias  # Importer la vue liste_medias depuis membre



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', liste_medias, name='accueil'),  # La liste des médias devient la page d'accueil
    path('membre/', include('membre.urls')),  # Routes spécifiques à membre
    path('bibliotheque/', include('bibliotheque.urls')),  # Routes spécifiques à bibliotheque
]


