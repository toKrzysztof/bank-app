import requests
import unittest
from app.AccountRegistry import AccountRegistry
from app.PrivateAccount import PrivateAccount


class PerformanceTest(unittest.TestCase):
    def setUp(self):
        self.account = {
            "firstName": "Jan",
            "lastName": "Kowalski",
            "pesel": "12345678901",
        }
        self.url = "http://localhost:5000/api/accounts"

    def tearDown(self):
        AccountRegistry.registry = []

    def test_100_accounts(self):
        for i in range(100):
            postAccountResponse = requests.post(self.url, json=self.account, timeout=2)
            self.assertEqual(postAccountResponse.status_code, 201)

            deleteAccountResponse = requests.delete(
                self.url + "/" + self.account["pesel"], timeout=2
            )
            self.assertEqual(deleteAccountResponse.status_code, 200)
