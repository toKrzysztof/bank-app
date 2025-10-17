import requests
import unittest


class TestAccountCrud(unittest.TestCase):
    url = "http://localhost:5000/api/accounts"

    def test_1_create_account_doesnt_yet_exist(self):
        response = requests.post(
            self.url,
            json={"firstName": "Jan", "lastName": "Kowalski", "pesel": "12345678901"},
        )
        self.assertEqual(
            response.status_code, 201, "Failed to create account"
        )

    def test_2_create_account_already_exists(self):
        response = requests.post(
            self.url,
            json={"firstName": "Jan", "lastName": "Kowalski", "pesel": "12345678901"},
        )
        self.assertEqual(
            response.status_code,
            409,
            "Account with given pesel already exists",
        )

    def test_3_get_account_by_pesel(self):
        response = requests.get(self.url + "/12345678901")
        self.assertEqual(
            response.status_code, 200, "Failed to retrieve account by pesel"
        )
        self.assertEqual(
            response.json(),
            {
                "firstName": "Jan",
                "lastName": "Kowalski",
                "pesel": "12345678901",
                "balance": 0,
            },
            "Failed to match account details by pesel",
        )

    def test_4_check_for_404(self):
        response = requests.get(self.url + "/12345678901098")
        self.assertEqual(
            response.status_code, 404, "Failed to handle 404 for non-existent account"
        )

    def test_5_patch(self):
        response = requests.patch(
            self.url + "/12345678901",
            json={"firstName": "Jan", "lastName": "Niewalski"},
        )
        self.assertEqual(
            response.status_code, 200, "Failed to update account details using patch"
        )

    def test_6_delete(self):
        response = requests.delete(self.url + "/12345678901")
        self.assertEqual(response.status_code, 200, "Failed to delete account")

    # for development purposes - remove later
    def test_7_DROP_TABLE(self):
        response = requests.delete(self.url + "/DROP_TABLE")
        self.assertEqual(response.status_code, 200, "Failed to drop table")

    @classmethod
    def tearDownClass(cls):
        requests.delete(cls.url + "/DROP_TABLE")
