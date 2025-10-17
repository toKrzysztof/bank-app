import requests
import unittest


class TestTransfers(unittest.TestCase):
    pesel = "12345678901"
    url = "http://localhost:5000/api/accounts"

    @classmethod
    def setUpClass(cls):
        requests.post(
            cls.url,
            json={"firstName": "Jan", "lastName": "Kowalski", "pesel": cls.pesel},
        )

    @classmethod
    def tearDownClass(cls):
        requests.delete(
            cls.url + "/" + cls.pesel,
        )

    def test_1_incoming_transfer_account_exists(self):
        response = requests.post(
            self.url + "/" + self.pesel + "/transfer",
            json={"sum": 600, "type": "incoming"},
        )
        account = requests.get(self.url + "/" + self.pesel).json()
        balance = account["balance"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(balance, 600)

    def test_2_incoming_transfer_account_doesnt_exists(self):
        response = requests.post(
            self.url + "/098765432109" + "/transfer",
            json={"sum": 500, "type": "incoming"},
        )
        self.assertEqual(response.status_code, 404)

    def test_3_outgoing_transfer_sufficient_funds(self):
        response = requests.post(
            self.url + "/" + self.pesel + "/transfer",
            json={"sum": 500, "type": "outgoing"},
        )
        account = requests.get(self.url + "/" + self.pesel).json()
        balance = account["balance"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(balance, 100)

    def test_4_outgoing_transfer_insufficient_funds(self):
        response = requests.post(
            self.url + "/" + self.pesel + "/transfer",
            json={"sum": 500, "type": "outgoing"},
        )
        account = requests.get(self.url + "/" + self.pesel).json()
        balance = account["balance"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(balance, 100)
