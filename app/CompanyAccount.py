from app.Account import Account
from datetime import datetime
from app.external_api.external_api import validate_nip_request
from dotenv import load_dotenv

load_dotenv()


class CompanyAccount(Account):
    express_transfer_fee = 5
    type = "company"

    def __init__(self, company_name: str, nip: str):
        super().__init__()
        self.company_name = company_name

        if len(nip) != 10:
            self.nip = "Invalid nip"
        else:
            if not self.validate_nip(nip):
                raise Exception("Taki nip nie istnieje krętaczu! 🤨")
            
            self.nip = nip


    def get_credit(self, sum) -> bool:
        if self.balance < sum * 2 or -1775 not in self.history:
            return False
        
        self.balance += sum
        return True
    
    def validate_nip(self, nip) -> bool:
        today_date = datetime.today().strftime('%Y-%m-%d')
        responseSubject = validate_nip_request(nip, today_date)["result"]["subject"]
        return True if responseSubject else False

    def send_history_through_mail(self, receiver_mail, SMPTConnection):
        response = SMPTConnection.send("history", f"Your company's account history: {self.history}", receiver_mail)

        return response