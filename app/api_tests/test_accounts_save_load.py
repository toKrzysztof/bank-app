from pymongo import MongoClient
import requests
import unittest


class TestTransfers(unittest.TestCase):
    pesel = "12345678901"
    url = "http://localhost:5000/api/accounts"

    client = MongoClient("localhost", 27017)
    db = client["mydatabase"]
    collection = db["konta"]

    def setUp(self):  
        requests.post(
            self.url,
            json={"firstName": "Jan", "lastName": "Kowalski", "pesel": self.pesel},
        )
    
    def tearDown(self):
        requests.delete(
            self.url + "/" + self.pesel,
        )
        self.collection.delete_many({})

    def test_1_load_accounts(self):
        response = requests.get(self.url + "/load")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], 0)

    def test_2_save_accounts(self):
        saveResponse = requests.post(self.url + "/save")
        loadResponse = requests.get(self.url + "/load")
        self.assertEqual(saveResponse.status_code, 201)
        self.assertEqual(loadResponse.status_code, 200)
        self.assertEqual(loadResponse.json()["message"], 1)

