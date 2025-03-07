from django.contrib import admin
from .models import Media, Membre, Emprunt

admin.site.register(Membre)
admin.site.register(Media)
admin.site.register(Emprunt)

