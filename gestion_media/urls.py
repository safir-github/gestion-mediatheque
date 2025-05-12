from django.contrib import admin
from django.urls import path, include  # Import de include
from membre.views import liste_medias  # Importer la vue liste_medias depuis membre
from membre.views import login_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('membre/', include('membre.urls')),
    path('bibliotheque/', include('bibliotheque.urls')),
    path("", login_view, name="accueil"),

]


