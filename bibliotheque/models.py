
from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta



class Membre(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom




class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('DVD', 'DVD'),
        ('CD', 'CD'),
        ('JeuDePlateau', 'Jeu de Plateau'),
    ]

    titre = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} ({self.type})"

    def emprunter(self, membre):
        """ Méthode pour emprunter un média """
        if not self.disponible:
            return False, "Ce média est déjà emprunté."
        if "jeu" in self.type.lower():
            return False, "Les jeux de plateau ne peuvent pas être empruntés."

        Emprunt.objects.create(membre=membre, media=self)
        self.disponible = False
        self.save()
        return True, "Emprunt réussi."

    def rendre(self):
        """ Méthode pour rendre un média """
        emprunt = Emprunt.objects.filter(media=self).first()
        if not emprunt:
            return False, "Ce média n'est pas emprunté."

        self.disponible = True
        self.save()
        emprunt.date_retour = now()
        emprunt.save()
        emprunt.delete()
        return True, "Retour réussi."



class Emprunt(models.Model):
    membre = models.ForeignKey('Membre', on_delete=models.CASCADE)
    media = models.ForeignKey('Media', on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membre.nom} a emprunté {self.media.titre}"

    def marquer_comme_rendu(self):
        """ Marquer l'emprunt comme rendu """
        self.date_retour = now()
        self.rendu = True
        self.save()
        self.media.disponible = True  # Rendre le média disponible
        self.media.save()

    @staticmethod
    def emprunter_media(membre, media):
        print(f"DEBUG: membre reçu = {membre} ({type(membre)})")  # 🟢 Debug
        print(f"DEBUG: media reçu = {media} ({type(media)})")  # 🟢 Debug

        # ✅ Si membre est un ID (str ou int), récupérer l'objet Membre
        if isinstance(membre, str) or isinstance(membre, int):
            try:
                membre = Membre.objects.get(id=int(membre))
                print(f"DEBUG: Conversion réussie, membre = {membre}")  # 🟢 Debug
            except Membre.DoesNotExist:
                print("❌ ERREUR: Membre introuvable.")  # 🛑 Debug
                return False, "Ce membre n'existe pas."

        # ✅ Si media est un ID (str ou int), récupérer l'objet Media
        if isinstance(media, str) or isinstance(media, int):
            try:
                media = Media.objects.get(id=int(media))
                print(f"DEBUG: Conversion réussie, media = {media}")  # 🟢 Debug
            except Media.DoesNotExist:
                print("❌ ERREUR: Media introuvable.")  # 🛑 Debug
                return False, "Ce média n'existe pas."

        # ✅ Vérification 1 : Bloquer les jeux de plateau
        if "jeu" in media.type.lower():
            return False, "Les jeux de plateau ne peuvent pas être empruntés."

        # ✅ Vérification 2 : Limite de 3 emprunts par membre
        if Emprunt.objects.filter(membre=membre, date_retour__isnull=True).count() >= 3:
            return False, "Ce membre a déjà atteint la limite de 3 emprunts."

        # ✅ Vérification 3 : Emprunts en retard
        date_limite = timezone.now() - timedelta(days=7)
        emprunts_actifs = Emprunt.objects.filter(membre=membre, date_retour__isnull=True)
        if emprunts_actifs.filter(date_emprunt__lte=date_limite).exists():
            return False, "Ce membre a un emprunt en retard et ne peut pas emprunter."

        # ✅ Créer l'emprunt et mettre à jour le statut du média
        Emprunt.objects.create(membre=membre, media=media)
        media.disponible = False
        media.save()

        return True, f"{media.titre} a été emprunté avec succès."
    @staticmethod
    def rendre_media(media_id):
        print(f"DEBUG: media_id reçu = {media_id} ({type(media_id)})")

        # Vérifier que media_id est bien un entier
        if isinstance(media_id, Media):
            print("❌ ERREUR: media_id est un objet Media, conversion en ID...")
            media_id = media_id.id  # ✅ Extraire l'ID si c'est un objet Media

        if not isinstance(media_id, int) and not str(media_id).isdigit():
            print("❌ ERREUR: media_id n'est pas un entier valide.")  # 🛑 Debug
            return False, "ID du média invalide."

        media_id = int(media_id)  # Assurer que c'est bien un entier

        try:
            media = Media.objects.get(id=media_id, disponible=False)
            print(f"DEBUG: Media trouvé = {media}")  # 🟢 Debug
        except Media.DoesNotExist:
            print("DEBUG: Media introuvable ou déjà disponible.")  # 🟠 Debug
            return False, "Ce média n'existe pas ou est déjà disponible."

        emprunt = Emprunt.objects.filter(media_id=media_id, date_retour__isnull=True).first()

        if emprunt:
            print(f"DEBUG: Emprunt trouvé pour {media.titre}")  # 🟢 Debug
            emprunt.date_retour = timezone.now()
            emprunt.save()
            media.disponible = True
            media.save()
            return True, f"{media.titre} a été rendu avec succès."

        print("DEBUG: Aucun emprunt actif trouvé.")
        return False, "Aucun emprunt actif trouvé pour ce média."



    @classmethod
    def verifier_emprunts_en_retard(cls):
        # Définir la date limite (7 jours)
        date_limite = timezone.now() - timedelta(days=7)

        # Récupérer tous les emprunts en retard
        emprunts_en_retard = Emprunt.objects.filter(date_retour__isnull=True, date_emprunt__lte=date_limite)

        for emprunt in emprunts_en_retard:
            # Bloquer le membre
            emprunt.membre.bloque = True  # Marquer le membre comme bloqué
            emprunt.membre.save()