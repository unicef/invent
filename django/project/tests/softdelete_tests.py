from rest_framework.test import APITestCase

from project.models import DigitalStrategy


class TestSoftDelete(APITestCase):
    def test_on_instance_delete(self):
        ds1 = DigitalStrategy.objects.create(name='ds1', group='Client')
        self.assertEqual(ds1.is_active, True)

        ds1.delete()
        self.assertEqual(ds1.is_active, False)

    def test_queryset_delete(self):
        total_count = DigitalStrategy.objects.all().count()
        self.assertEqual(total_count, 117)

        active_count = DigitalStrategy.objects.filter(is_active=True).count()
        self.assertEqual(active_count, 117)

        is_active_false_count = DigitalStrategy.all_objects.filter(is_active=False).count()
        self.assertEqual(is_active_false_count, 0)

        DigitalStrategy.objects.all().delete()

        active_count = DigitalStrategy.objects.filter(is_active=True).count()
        self.assertEqual(active_count, 0)

        active_count = DigitalStrategy.objects.all().count()
        self.assertEqual(active_count, 0)

        is_active_false_count = DigitalStrategy.all_objects.filter(is_active=False).count()
        self.assertEqual(is_active_false_count, 117)
