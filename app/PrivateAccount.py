from app.Account import Account
from app.mail.SMTPConnection import SMTPConnection

class PrivateAccount(Account):
    type = "private"
    
    def __init__(
        self, firstName: str, lastName: str, pesel: str, promo_code: str | None = None
    ):
        super().__init__()
        self.firstName = firstName
        self.lastName = lastName
        pass

        if len(pesel) != 11:
            self.pesel = "Invalid pesel"
        else:
            self.pesel = pesel

        if self.is_promo_code_correct(promo_code) and self.can_customer_get_promo(
            pesel
        ):
            self.balance = 50
        else:
            self.balance = 0

    def send_history_through_mail(self, receiver_mail, SMPTConnection):
        response = SMPTConnection.send("history", f"Your account history: {self.history}", receiver_mail)

        return response

    def can_customer_get_promo(self, pesel) -> bool:
        if (
            self.was_born_in_20th_century(pesel)
            and int(self.get_year_of_birth_shorthand(pesel)) <= 60
        ):
            return False

        return True
    
    def get_credit(self, sum) -> bool:
        if self.calculate_sum_of_last_n_transactions(5) == None:
            return False

        if self.calculate_sum_of_last_n_transactions(5) > sum and self.are_last_n_transactions_incoming(3):
            self.balance += sum
            return True
        
        return False
    
    # section - utility methods

    def is_promo_code_correct(self, promo_code) -> bool:
        if promo_code is None:
            return False

        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True

        return False

    def was_born_in_20th_century(self, pesel) -> bool:
        milleniumNumber = pesel[2]
        return milleniumNumber == "0"

    def get_year_of_birth_shorthand(self, pesel) -> str:
        return pesel[0:2]
    
    def are_last_n_transactions_incoming(self, n) -> bool:
        incoming_transactions_counter = 0
        for payment in self.history:
            if payment > 0:
                incoming_transactions_counter += 1
        
        return incoming_transactions_counter == n
    
    def calculate_sum_of_last_n_transactions(self, n) -> int | None:
        if n > len(self.history):
            return None
        
        sum = 0

        for i in range (n):
            sum += self.history[i]

        return sum
    
    # end section - utility methods