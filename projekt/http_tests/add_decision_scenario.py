import unittest
from rest_framework.test import APITestCase


class MyTestCase(APITestCase):
    def test_add_decision_scenario(self):
        response = self.client.post('   `/decision_scenario', {'title': 'new idea'}, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
