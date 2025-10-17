import unittest

from app.CompanyAccount import CompanyAccount
from unittest.mock import patch


class TestCreateCompanyAccount(unittest.TestCase):
    company_data = {
        "company_name": "Super Firma",
        "nip": "8461627563",
    }

    mock_validate_nip_response = {
        'result': {
            'subject': {
                'nip': '8461627563',
            },
        }
    }

    # section - account creation
    
    @patch("app.external_api.external_api.requests.get")
    def test_1_creating_account(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = self.mock_validate_nip_response
        
        account = CompanyAccount(
            self.company_data["company_name"], self.company_data["nip"]
        )
        
        self.assertEqual(
            account.company_name,
            self.company_data["company_name"],
            "Company name was not saved!",
        )
        self.assertEqual(
            account.nip,
            self.company_data["nip"],
            "Nip was not saved!",
        )


    # end section - account creation

    # section - nip validation

    def test_2_nip_with_len_9(self):
        account = CompanyAccount(self.company_data["company_name"], "11111111111")
        self.assertEqual(account.nip, "Invalid nip", "Nip given is too short")

    def test_3_nip_with_len_11(self):
        account = CompanyAccount(self.company_data["company_name"], "111111111")
        self.assertEqual(account.nip, "Invalid nip", "Nip given is too long")

    def test_4_nip_empty(self):
        account = CompanyAccount(self.company_data["company_name"], "")
        self.assertEqual(account.nip, "Invalid nip", "Nip given is empty")

    @patch("app.CompanyAccount.CompanyAccount.validate_nip")
    def test_5_nip_doesnt_exists(self, mock_validate_nip):
        mock_validate_nip.return_value = False
        with self.assertRaises(Exception) as context:
            account = CompanyAccount(self.company_data["company_name"], self.company_data["nip"])
        self.assertTrue("Taki nip nie istnieje krętaczu! 🤨" in str(context.exception))

    # end section - nip validation
