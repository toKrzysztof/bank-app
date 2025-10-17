import unittest

from app.PrivateAccount import PrivateAccount


class TestCreatePrivateBankAccount(unittest.TestCase):
    firstName = "Dariusz"
    lastName = "Januszewski"
    pesel = "12345678901"
    valid_promo_code = "PROM_XYZ"

    # section - account creation

    def test_creating_account(self):
        account = PrivateAccount(self.firstName, self.lastName, self.pesel)
        self.assertEqual(account.firstName, self.firstName, "First name was not saved!")
        self.assertEqual(account.lastName, self.lastName, "Last name was not saved!")
        self.assertEqual(account.balance, 0, "Balance is not 0!")
        self.assertEqual(account.pesel, self.pesel, "Pesel was not saved!")

    # end section - account creation

    # section - pesel validation

    def test_pesel_with_len_10(self):
        account = PrivateAccount(self.firstName, self.lastName, "1234567890")
        self.assertEqual(account.pesel, "Invalid pesel", "Pesel given is too short")

    def test_pesel_with_len_12(self):
        account = PrivateAccount(self.firstName, self.lastName, "1234567890111")
        self.assertEqual(account.pesel, "Invalid pesel", "Pesel given is too long")

    def test_pesel_empty(self):
        account = PrivateAccount(self.firstName, self.lastName, "")
        self.assertEqual(account.pesel, "Invalid pesel", "Pesel given is empty")

    # end section - pesel validation

    # section - promo_code validation

    def test_promo_wrong_prefix(self):
        account = PrivateAccount(self.firstName, self.lastName, self.pesel, "PR_123")
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_wrong_suffix(self):
        account = PrivateAccount(
            self.firstName, self.lastName, self.pesel, "PROM_12345"
        )
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_wrong_len(self):
        account = PrivateAccount(
            self.firstName, self.lastName, self.pesel, "PROMMOM_123"
        )
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_no_code(self):
        account = PrivateAccount(self.firstName, self.lastName, self.pesel, None)
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_correct(self):
        account = PrivateAccount(
            self.firstName, self.lastName, self.pesel, self.valid_promo_code
        )
        self.assertEqual(account.balance, 50, "Promotion was not accounted for")

    def test_promo_year_59(self):
        account = PrivateAccount(
            self.firstName, self.lastName, "59023456789", self.valid_promo_code
        )
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_year_61(self):
        account = PrivateAccount(
            self.firstName, self.lastName, "61023456789", self.valid_promo_code
        )
        self.assertEqual(account.balance, 50, "Promotion was not accounted for")

    def test_promo_year_2001_with_wrong_promo_code(self):
        account = PrivateAccount(self.firstName, self.lastName, "01283456789", "PR_2")
        self.assertEqual(account.balance, 0, "Balance is not 0")

    def test_promo_year_2001_with_correct_promo_code(self):
        account = PrivateAccount(
            self.firstName, self.lastName, "01283456789", self.valid_promo_code
        )
        self.assertEqual(account.balance, 50, "Promotion was not accounted for")

    def test_promo_year_60(self):
        account = PrivateAccount(
            self.firstName, self.lastName, "60083456789", self.valid_promo_code
        )
        self.assertEqual(account.balance, 0, "Balance is not 0")

    # end section - promo_code validation
