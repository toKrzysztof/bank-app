import unittest

from app.PrivateAccount import PrivateAccount

class TestHistory(unittest.TestCase):
    personal_data = {
        "firstname": "Adam",
        "lastname": "Nowak",
        "pesel": "01282874666"
    }

    def test_credit_given_success(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.history = [100, 100, 100, -50, -50]
        account.balance = 200
        self.assertEqual(account.get_credit(100), True, "Credit was incorrectly noted as not given")

    def test_credit_given_success_account_balance(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        account.history = [100, 100, 100, -50, -50]
        account.balance = 200
        account.get_credit(100)
        self.assertEqual(account.balance, 300, "Account balance is incorrect!")
        
    def test_credit_given_fail(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        self.assertEqual(account.get_credit(250), False, "Credit was incorrectly noted as given")

    def test_credit_given_fail_account_balance(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        account.get_credit(100)
        self.assertEqual(account.balance, 0, "Account balance is incorrect!")

    def test_credit_given_fail_account_history(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        account.get_credit(100)
        self.assertEqual(account.history, [], "Account history is incorrect!")

    def test_credit_last_3_transactions_incoming_payment_insufficient_funds(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.history = [100, 100, 100, -50, -50]
        account.balance = 200
        account.get_credit(200)
        self.assertEqual(account.get_credit(200), False, "Credit was incorrectly noted as given!")        

    def test_credit_last_3_transactions_not_incoming_payment_sufficient_funds(self):
        account = PrivateAccount(
            self.personal_data["firstname"],
            self.personal_data["lastname"],
            self.personal_data["pesel"],
        )
        account.balance = 0
        account.incoming_transfer(150)
        account.get_credit(100)
        self.assertEqual(account.get_credit(100), False, "Credit was incorrectly noted as given!") 