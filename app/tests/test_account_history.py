import unittest

from app.PrivateAccount import PrivateAccount
from app.CompanyAccount import CompanyAccount
from unittest.mock import patch

class TestHistory(unittest.TestCase):
    personal_data = {
        "name": "Adam",
        "surname": "Nowak",
        "pesel": "01282874666"
    }

    # company with invalid nip
    company_data = {
        "name": "Dziam dziam",
        "nip": "123456789"
    }

    def test_history_personal(self):
        account = PrivateAccount(self.personal_data["name"], self.personal_data["surname"], self.personal_data["pesel"])
        account.balance = 50
        account.outgoing_transfer(50)
        account.incoming_transfer(100)
        self.assertEqual(account.history, [100, -50], "History is incorrect!")

    def test_history_company(self):
        account = CompanyAccount(self.company_data["name"], self.company_data["nip"])
        account.balance = 100
        account.incoming_transfer(15)
        account.outgoing_transfer(90)
        account.incoming_transfer(3)
        self.assertEqual(account.history, [3, -90, 15], "History is incorrect!")

    def test_history_personal_express(self):
        account = PrivateAccount(self.personal_data["name"], self.personal_data["surname"],self.personal_data["pesel"])
        account.balance = 50
        account.express_outgoing_transfer(20)
        account.incoming_transfer(50)
        account.express_outgoing_transfer(10)
        self.assertEqual(account.history, [-1, -10, 50, -1, -20], "History is incorrect!")

    def test_history_company_express(self):
        Account = CompanyAccount(self.company_data["name"], self.company_data["nip"])
        Account.balance = 50
        Account.express_outgoing_transfer(20)
        Account.incoming_transfer(50)
        Account.express_outgoing_transfer(10)
        self.assertEqual(Account.history, [-5, -10, 50, -5, -20], "History is incorrect!")