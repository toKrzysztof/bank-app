from app.PrivateAccount import PrivateAccount 
from pymongo import MongoClient

class AccountRegistry:
    client = MongoClient('localhost', 27017)
    db = client['mydatabase']
    collection = db['konta']
    accounts = []

    @classmethod
    def add_account(cls, account):
        if account.type == "private":
            cls.accounts.insert(0, account)

    @classmethod
    def search_account(cls, pesel):
        for account in cls.accounts:
            if account.pesel == pesel:
                return account

        return None

    @classmethod
    def get_number_of_accounts(cls):
        return len(cls.accounts)

    @classmethod
    def update_account(cls, pesel, new_data):
        account = cls.search_account(pesel)

        if not account:
            return None

        for key in new_data:
            fieldToUpdate = getattr(account, key)
            if fieldToUpdate:
                setattr(account, key, new_data[key])

        return account

    @classmethod
    def delete_account(cls, pesel):
        for i in range(len(cls.accounts)):
            if cls.accounts[i].pesel == pesel:
                return cls.accounts.pop(i)

        return None
    
    @classmethod
    def load(cls):
      cls.accounts = []
      for account_data in cls.collection.find():
          account = PrivateAccount(account_data["firstName"], account_data["lastName"], account_data["pesel"])
          account.balance = account_data["balance"]
          account.history = account_data["pesel"]
          cls.accounts.append(account)
      
      return cls.accounts

    @classmethod
    def save(cls):
      cls.collection.delete_many({})

      for account in cls.accounts:
          account_data = {
              "pesel": account.pesel,
              "firstName": account.firstName,
              "lastName": account.lastName,
              "balance": account.balance,
              "history": account.history
          }
          cls.collection.insert_one(account_data)

    @classmethod
    def DROP_TABLE(cls):
        cls.accounts = []
