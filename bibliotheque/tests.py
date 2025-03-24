from django.test import TestCase
from .models import Membre, Media, Emprunt
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages


class MembreTests(TestCase):

    def test_creer_membre(self):
        # Création d'un membre
        membre = Membre.objects.create(nom="Jean Dupont", email="jean@exemple.com", bloque=False)

        # Vérifier que le membre a bien été ajouté
        self.assertEqual(Membre.objects.count(), 1)
        self.assertEqual(membre.nom, "Jean Dupont")
        self.assertEqual(membre.email, "jean@exemple.com")
        self.assertFalse(membre.bloque)  # Vérifier que le membre n'est pas bloqué



class MembreListTests(TestCase):

    def test_afficher_liste_membres(self):
        # Créer quelques membres
        Membre.objects.create(nom="Alice", email="alice@exemple.com")
        Membre.objects.create(nom="Bob", email="bob@exemple.com")

        # Faire une requête à la vue
        response = self.client.get(reverse('liste_membres'))

        # Vérifier que la requête a réussi (code 200)
        self.assertEqual(response.status_code, 200)

        # Vérifier que les noms des membres sont bien affichés
        self.assertContains(response, "Alice")
        self.assertContains(response, "Bob")



class MembreUpdateTests(TestCase):

    def test_modifier_membre(self):
        # Créer un membre
        membre = Membre.objects.create(nom="Charlie", email="charlie@exemple.com")

        # Modifier ses informations
        response = self.client.post(reverse('modifier_membre', args=[membre.id]), {
            'nom': 'Charlie Modifié',
            'email': 'charlie@exemple.com',
            'bloque': False
        })

        # Vérifier la redirection après modification
        self.assertEqual(response.status_code, 302)

        # Vérifier que les données sont bien mises à jour
        membre.refresh_from_db()
        self.assertEqual(membre.nom, "Charlie Modifié")



class ListeMediasTests(TestCase):

    def test_afficher_liste_medias(self):
        # Créer des médias
        Media.objects.create(titre="Livre A", type="Livre", disponible=True)
        Media.objects.create(titre="DVD B", type="DVD", disponible=False)

        # Accéder à la liste des médias
        response = self.client.get(reverse('liste_medias'))

        # Vérifier que la page s'affiche correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que les médias sont bien présents dans le contexte
        self.assertContains(response, "Livre A")
        self.assertContains(response, "DVD B")




class EmpruntTests(TestCase):
    def setUp(self):
        """Initialisation des données de test."""
        self.membre = Membre.objects.create(nom="Ali", email="ali@example.com", bloque=False)
        self.media = Media.objects.create(titre="Livre X", type="Livre", disponible=True)

    def test_creer_emprunt_media_disponible(self):
        """Vérifie qu'un média disponible peut être emprunté."""
        response = self.client.post(reverse('emprunter_media'), {
            'membre_id': self.membre.id,
            'media_id': self.media.id
        })

        self.assertEqual(response.status_code, 302)  # Vérifie la redirection
        self.media.refresh_from_db()
        self.assertFalse(self.media.disponible)  # Vérifie que le média n'est plus disponible

    def test_rendre_emprunt(self):
        """Vérifie que l'emprunt d'un média peut être rendu avec succès."""
        # Créer un membre avec un email unique
        membre = Membre.objects.create(nom="Ali", email="ali_test@example.com", bloque=False)

        # Créer un média emprunté
        self.media.disponible = False
        self.media.save()

        # Créer un emprunt pour ce média (média non disponible)
        emprunt = Emprunt.objects.create(membre=membre, media=self.media, date_emprunt=timezone.now(), date_retour=None)

        # Effectuer la requête POST pour rendre l'emprunt
        response = self.client.post(reverse('rendre_media', kwargs={'media_id': self.media.id}))

        # Vérifier que la réponse est une redirection (code 302)
        self.assertEqual(response.status_code, 302)

        # Suivre la redirection
        response = self.client.get(response.url)

        # Vérifier que le message de succès est bien affiché
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Livre X a été rendu avec succès.", messages)

        # Vérifier que l'emprunt a bien été mis à jour avec une date de retour
        emprunt.refresh_from_db()  # Recharge l'emprunt pour vérifier les changements
        self.assertIsNotNone(emprunt.date_retour)

        # Vérifier que le média est maintenant disponible
        self.media.refresh_from_db()  # Recharge le média pour vérifier son statut
        self.assertTrue(self.media.disponible)




class MediaTests(TestCase):
    def test_ajouter_media(self):
        # Créer un membre pour l'emprunt
        membre = Membre.objects.create(nom='Ali', email='ali@example.com', bloque=False)

        # Créer un média à ajouter
        media_data = {
            'titre': 'Livre X',
            'type': 'Livre',
            'disponible': True
        }

        # Effectuer la requête POST
        response = self.client.post(reverse('ajouter_media'), media_data)

        # Vérifier que la redirection a eu lieu vers la liste des médias
        self.assertEqual(response.status_code, 302)  # Attendre une redirection (code 302)

        # Vérifier que le média a bien été ajouté
        self.assertEqual(Media.objects.count(), 1)
        self.assertEqual(Media.objects.first().titre, 'Livre X')



