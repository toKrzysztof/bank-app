import unittest
from unittest.mock import patch
from parameterized import parameterized

from app.PrivateAccount import PrivateAccount
from app.CompanyAccount import CompanyAccount
from app.mail.SMTPConnection import SMTPConnection

class TestHistory(unittest.TestCase):
    connection = SMTPConnection

    receiver_email = "example@gmail.com"

    personal_data = {
        "name": "Adam",
        "surname": "Nowak",
        "pesel": "01282874666"
    }

    company_data = {
        "name": "Dziam dziam",
        "nip": "1234567891"
    }

    mock_validate_nip_response = {
        'result': {
            'subject': {
                'nip': '8461627563',
            },
        }
    }

    @parameterized.expand([
        True,
        False
    ])
    @patch("app.mail.SMTPConnection.SMTPConnection.send")
    def test_1_send_private_account_history(self, mock_send_expected_response, mock_send):
        mock_send.return_value = mock_send_expected_response

        account = PrivateAccount(self.personal_data["name"], self.personal_data["surname"], self.personal_data["pesel"])
        account.incoming_transfer(100)
        
        response = account.send_history_through_mail(self.receiver_email, self.connection)

        # Check if send was called with the expected arguments
        mock_send.assert_called_once_with("history", f"Your account history: {account.history}", self.receiver_email)

        self.assertEqual(response, mock_send_expected_response, "Email was not sent!")

    @parameterized.expand([
        True,
        False
    ])
    @patch("app.external_api.external_api.requests.get")
    @patch("app.mail.SMTPConnection.SMTPConnection.send")
    def test_2_send_company_history(self, mock_send_expected_response, mock_send, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = self.mock_validate_nip_response

        mock_send.return_value = mock_send_expected_response

        account = CompanyAccount(self.company_data["name"], self.company_data["nip"])
        account.incoming_transfer(15)

        response = account.send_history_through_mail(self.receiver_email, self.connection)

        mock_send.assert_called_once_with("history", f"Your company's account history: {account.history}", self.receiver_email)

        self.assertEqual(response, mock_send_expected_response, "Email was not sent!")