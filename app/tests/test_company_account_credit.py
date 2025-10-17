import unittest
from unittest.mock import patch

from app.CompanyAccount import CompanyAccount
from parameterized import parameterized


class TestCompanyAccountCredit(unittest.TestCase):
    company_data = {
        "company_name": "Super Firma",
        "nip": "8461627563",
    }

    @parameterized.expand([
        ([2000, -1775], 225, 100, True, 325),
        ([100], 100, 100, False, 100),
        ([2000, -1775], 225, 225, False, 225),
        ([225], 225, 100, False, 225)
    ])
    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_company_credit(self, history, balance, credit_sum, expected_output, expected_balance, mock_validate_nip):
        mock_validate_nip.return_value = True
        companyAccount = CompanyAccount(self.company_data["company_name"], self.company_data["nip"])
        companyAccount.history = history
        companyAccount.balance = balance
        creditGiven = companyAccount.get_credit(credit_sum)
        self.assertEqual(creditGiven, expected_output, "Credit output is incorrect!")
        self.assertEqual(companyAccount.balance, expected_balance, "Balance is incorrect!")
