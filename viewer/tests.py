from django.test import TestCase


class ExampleTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        # print("setUpTestData: Spustí se jednou na začátku testování a "
        #      "slouží k nastavení databáze")

    def setUp(self):
        pass
        # print("setUp: Spustí se před každým testem.")

    def test_false(self):
        # print("Testovací metoda: test_false")
        result = False
        self.assertFalse(result)

    def test_add(self):
        # print("Testovací metoda: test_add")
        result = 1 + 4
        self.assertEqual(result, 5)

