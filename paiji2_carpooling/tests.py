from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from paiji2_carpooling.models import (
    Carpool,
    default_good_until,
)
# from paiji2_carpooling.views import (
#     CarpoolOwnerMixin,
#     CarpoolListView,
#     CarpoolCreateView,
#     CarpoolEditView,
#     CarpoolDeleteView,
# )
from paiji2_carpooling.templatetags.cov_tag import (
    get_cov,
)


User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            'alice',
            password='test',
        )
        self.chuck = User.objects.create_user(
            'chuck',
            password='test',
        )
        self.carpool = Carpool.objects.create(
            author=self.alice,
            annonce_type=Carpool.OFFER,
            notes='Test',
        )
        self.client = Client(enforce_csrf_checkts=True)


class PagesTestCase(BaseTestCase):
    def test_list(self):
        # Non unauthenticated user
        response = self.client.get(reverse('carpool-list'))
        self.assertEqual(response.status_code, 302)

        # Authenticated user
        self.client.login(username='alice', password='test')
        response = self.client.get(reverse('carpool-list'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        # Non authenticated user
        response = self.client.get(reverse('carpool-create'))
        self.assertEqual(response.status_code, 302)

        # Authenticated user
        self.client.login(username='alice', password='test')

        response = self.client.get(reverse('carpool-create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('carpool-create'), {
            'annonce_type': Carpool.OFFER,
            'good_until': default_good_until(),
            'notes': 'test',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Carpool.objects.count(), 2)

    def test_edit(self):
        url = reverse('carpool-edit', kwargs={
            'pk': self.carpool.pk,
        })
        # Non owner
        self.client.login(username='chuck', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        # Owner
        self.client.login(username='alice', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'annonce_type': Carpool.OFFER,
            'good_until': default_good_until(),
            'notes': 'test',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Carpool.objects.count(), 1)

    def test_delete(self):
        url = reverse('carpool-delete', kwargs={
            'pk': self.carpool.pk,
        })
        # Non owner
        self.client.login(username='chuck', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        # Owner
        self.client.login(username='alice', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Carpool.objects.count(), 0)


class TemplateTagsTestCase(BaseTestCase):
    def test_get_cov(self):
        context = {}
        context = get_cov(context)

        self.assertTrue('cov' in context)
        self.assertEqual(len(context.get('cov')), 1)


class ModelsTestCase(BaseTestCase):
    def setUp(self):
        super(ModelsTestCase, self).setUp()
        self.carpool_offer = Carpool.objects.create(
            author=self.alice,
            annonce_type=Carpool.OFFER,
            notes='test',
        )
        self.carpool_search = Carpool.objects.create(
            author=self.alice,
            annonce_type=Carpool.SEARCH,
            notes='test',
        )

    def test_carpool_unicode(self):
        carpool_search = unicode(self.carpool_search)

        self.assertEquals(type(carpool_search), unicode)
        self.assertTrue('searches' in carpool_search)

        carpool_offer = unicode(self.carpool_offer)

        self.assertEquals(type(carpool_offer), unicode)
        self.assertTrue('offers' in carpool_offer)


class ModularTestCase(BaseTestCase):
    def test_carpooling_modular(self):
        from modular_blocks import modules
        modules.autodiscover()
