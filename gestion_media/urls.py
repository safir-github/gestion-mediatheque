from django.contrib import admin
from django.urls import path, include  # Import de include

from bibliotheque import views
from membre.views import liste_medias  # Importer la vue liste_medias depuis membre
from membre.views import login_view
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('membre/', include('membre.urls')),
    path('bibliotheque/', include('bibliotheque.urls')),
    path("", login_view, name="accueil"),
    path("login-biblio/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login_biblio"),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=False)),

]


