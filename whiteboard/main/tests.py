from django.test import TestCase, Client

# Create your tests here.

class Test_Index(TestCase):
    
    def test_index(self):
        client = Client()
        response = client.get("")
        self.assertEqual(response.status_code, 200)
