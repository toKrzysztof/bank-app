import unittest

from app.AccountRegistry import AccountRegistry
from unittest.mock import patch, MagicMock


class TestMongo(unittest.TestCase):
    @patch("app.AccountRegistry.AccountRegistry.collection")
    def test_load_accounts_from_database(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "firstName": "Jan",
                "lastName": "Kowalski",
                "pesel": "12345678901",
                "balance": 0,
                "history": [],
            }
        ]
        AccountRegistry.load()
        self.assertEqual(len(AccountRegistry.accounts), 1)
        self.assertEqual(AccountRegistry.accounts[0].firstName, "Jan")
        self.assertEqual(AccountRegistry.accounts[0].firstName, "Jan")
        self.assertEqual(AccountRegistry.accounts[0].firstName, "Jan")
        self.assertEqual(AccountRegistry.accounts[0].firstName, "Jan")
        self.assertEqual(AccountRegistry.accounts[0].firstName, "Jan")

    @patch("app.AccountRegistry.AccountRegistry.collection")
    def test_save_accounts_to_database(self, mock_collection):
        mock_account = MagicMock()
        mock_account.pesel = "12345678901"
        mock_account.firstName = "Jan"
        mock_account.lastName = "Kowalski"
        mock_account.balance = 0
        mock_account.history = []

        AccountRegistry.accounts.append(mock_account)
        AccountRegistry.save()

        expected_data = {
            "firstName": "Jan",
            "lastName": "Kowalski",
            "pesel": "12345678901",
            "balance": 0,
            "history": [],
        }

        mock_collection.insert_one.assert_called_with(expected_data)
