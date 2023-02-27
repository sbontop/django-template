from django.test import TestCase

# Create your tests here.
from .models import MyModel


class MyModelTestCase(TestCase):
    def setUp(self):
        MyModel.objects.create(name="test")

    def test_mymodel(self):
        test = MyModel.objects.get(name="test")
        self.assertEqual(test.name, "test")
