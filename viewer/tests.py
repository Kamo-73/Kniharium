from django.test import TestCase


class ExampleTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_false(self):
        result = False
        self.assertFalse(result)

    def test_add(self):
        result = 1 + 4
        self.assertEqual(result, 5)
