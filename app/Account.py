class Account:
    express_transfer_fee = 1

    def __init__(self):
        self.balance = 0
        self.history = []

    def incoming_transfer(self, sum):
        if sum > 0:
            self.balance += sum
            self.history.insert(0, sum)


    def outgoing_transfer(self, sum):
        if self.can_make_outgoing_transfer(sum):
            self.balance -= sum
            self.history.insert(0, -sum)

    def express_outgoing_transfer(self, sum):
        if self.can_make_outgoing_transfer(sum):
            self.outgoing_transfer(sum)
            self.balance -= self.express_transfer_fee
            self.history.insert(0, -self.express_transfer_fee)

    def can_make_outgoing_transfer(self, sum):
        return sum > 0 and sum <= self.balance