from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Servicio

class AuthAndServicesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

    def test_inicio_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_servicios_requires_login(self):
        response = self.client.get('/servicios/')
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_user_data_isolation(self):
        # Create service for user1
        Servicio.objects.create(
            propietario=self.user1,
            titulo='Servicio User 1',
            descripcion='Desc 1',
            precio=100.00,
            categoria='Cat 1'
        )
        # Login as user2
        self.client.login(username='user2', password='password123')
        response = self.client.get('/servicios/')
        self.assertEqual(response.status_code, 200)
        # user2 should not see user1's service
        self.assertNotContains(response, 'Servicio User 1')

        # Login as user1
        self.client.logout()
        self.client.login(username='user1', password='password123')
        response = self.client.get('/servicios/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Servicio User 1')

    def test_servicios_search_and_pagination(self):
        self.client.login(username='user1', password='password123')
        # Create 6 services for user1 to test pagination (page size 5)
        for i in range(1, 7):
            Servicio.objects.create(
                propietario=self.user1,
                titulo=f'Servicio Alpha {i}',
                descripcion=f'Desc {i}',
                precio=50.00 * i,
                categoria='Cat'
            )
        Servicio.objects.create(
            propietario=self.user1,
            titulo='Beta Test',
            descripcion='Desc Beta',
            precio=99.00,
            categoria='Cat'
        )

        # Test search query 'Alpha'
        response = self.client.get('/servicios/?q=Alpha')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Servicio Alpha 6')
        self.assertNotContains(response, 'Beta Test')

        # Test pagination page 1
        response = self.client.get('/servicios/?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Página 1 de 2')
