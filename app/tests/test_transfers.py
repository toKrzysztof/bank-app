import unittest
from unittest.mock import patch

from app.Account import Account
from app.PrivateAccount import PrivateAccount
from app.CompanyAccount import CompanyAccount


class MakePayment(unittest.TestCase):
    personal_data = {"firstname": "Jan", "lastname": "Kowalski", "pesel": "03281234567"}
    company_data = {
        "company_name": "Mega Firma",
        "nip": "8461627563",
    }

    # section - general

    def test_incoming_transfer(self):
        account = Account()
        account.incoming_transfer(50)
        self.assertEqual(account.balance, 50, "Balance is not 50!")

    def test_incoming_transfer_0(self):
        account = Account()
        account.incoming_transfer(0)
        self.assertEqual(account.balance, 0, "Balance is not 0!")

    def test_incoming_transfer_incorrect_amount(self):
        account = Account()
        account.incoming_transfer(-50)
        self.assertEqual(account.balance, 0, "Balance is not 0!")

    def test_outgoing_transfer(self):
        account = Account()
        account.balance = 100
        account.outgoing_transfer(50)
        self.assertEqual(account.balance, 50, "Balance is not 50!")

    def test_outgoing_transfer_0(self):
        account = Account()
        account.outgoing_transfer(0)
        self.assertEqual(account.balance, 0, "Balance is not 0!")

    def test_outgoing_transfer_not_enough_cash(self):
        account = Account()
        account.balance = 100
        account.outgoing_transfer(150)
        self.assertEqual(account.balance, 100, "Balance is not 100!")

    # end section - general

    # section - private and public account

    def test_incoming_transfer_PA(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.incoming_transfer(50)
        self.assertEqual(account.balance, 50, "Balance is not 50!")

    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_incoming_transfer_CA(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        account.incoming_transfer(50)
        self.assertEqual(account.balance, 50, "Balance is not 50!")

    # end section - private and public account

    # section - private account with promo_code

    def test_incoming_transfer_correct_promo_code(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
            "PROM_XYZ",
        )
        account.incoming_transfer(50)
        self.assertEqual(account.balance, 100, "Balance is not 100!")

    def test_outgoing_transfer_correct_promo_code(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
            "PROM_XYZ",
        )
        account.outgoing_transfer(50)
        self.assertEqual(account.balance, 0, "Balance is not 0!")

    # end section - promo_code

    # section - express transfers

    def test_express_outgoing_transfer_PK(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 100
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, 49, "Balance is not 49!")

    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_express_outgoing_transfer_CA(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        account.balance = 100
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, 45, "Balance is not 45!")

    def test_express_outgoing_transfer_negative_balance_PK(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 50
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, -1, "Balance is not -1!")

    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_express_outgoing_transfer_negative_balance_CA(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        account.balance = 50
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, -5, "Balance is not -5!")

    def test_express_outgoing_transfer_not_enough_cash_PK(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, 0, "Balance is not 0")

    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_express_outgoing_transfer_not_enough_cash_CA(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        account.balance = 0
        account.express_outgoing_transfer(50)
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_express_outgoing_transfer_0_PK(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.express_outgoing_transfer(0)
        self.assertEqual(account.balance, 0, "Balance is not 0")
        
    @patch("app.CompanyAccount.CompanyAccount.validate_nip")    
    def test_express_outgoing_transfer_0_CA(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        account.express_outgoing_transfer(0)
        self.assertEqual(account.balance, 0, "Balance is not 0")      

    # end section - express transfers
