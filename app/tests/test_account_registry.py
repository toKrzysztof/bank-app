import unittest

from app.PrivateAccount import PrivateAccount
from app.AccountRegistry import AccountRegistry

class TestAccountRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.privateAccount = PrivateAccount("Jan", "Kowalski", "12345678901")
        AccountRegistry.add_account(cls.privateAccount)

    def test_1_add_account(self):
        privateAccount = PrivateAccount("98765432109", "Adam", "Nowak")
        AccountRegistry.add_account(privateAccount)
        self.assertEqual(len(AccountRegistry.accounts), 2, "Account count is incorrect!")

    def test_2_search_account_exists(self):
        account = AccountRegistry.search_account("12345678901")
        self.assertIsNotNone(account)
        self.assertEqual(account.pesel, "12345678901", "Wrong account was returned!")

    def test_3_search_account_doesnt_exist(self):
        account = AccountRegistry.search_account("12345678901123")
        self.assertIsNone(account)

    def test_4_get_number_of_accounts(self):
        self.assertEqual(AccountRegistry.get_number_of_accounts(), 2, "Accounts count is incorrect!")

    def test_5_update_account_that_exists(self):
        account = AccountRegistry.update_account("12345678901", { "firstName": "Marcin" })
        self.assertIsNotNone(account)
        self.assertEqual(account.firstName, "Marcin", "Account wasn't updated correctly!")

    def test_6_update_account_that_doesnt_exist(self):
        account = AccountRegistry.update_account("12345678901123", { "firstName": "Marcin" })
        self.assertIsNone(account)

    def test_7_delete_account_that_exists(self):
        account = AccountRegistry.delete_account("12345678901")
        self.assertEqual(account, self.privateAccount)
        self.assertEqual(AccountRegistry.get_number_of_accounts(), 1, "Accounts count is incorrect!")
        self.assertIsNotNone(account)

    def test_8_delete_account_that_doesnt_exists(self):
        account = AccountRegistry.delete_account("12345678901")
        self.assertIsNone(account)
        self.assertEqual(AccountRegistry.get_number_of_accounts(), 1, "Accounts count is incorrect!")

    def test_9_drop_accounts_table(self):
        AccountRegistry.DROP_TABLE()
        self.assertEqual(AccountRegistry.get_number_of_accounts(), 0, "Accounts count is incorrect!")

    @classmethod
    def tearDownClass(cls):
        AccountRegistry.accounts = []