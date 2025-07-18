from django.contrib import admin
from .models import Media, Membre, Emprunt, Livre, DVD, CD, JeuDePlateau

admin.site.register(Membre)
admin.site.register(Media)
admin.site.register(Livre)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(JeuDePlateau)
admin.site.register(Emprunt)

