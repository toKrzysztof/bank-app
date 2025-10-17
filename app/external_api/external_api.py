import requests
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

nipValidationApiUrl = os.getenv("BANK_APP_MF_URL")

def validate_nip_request(nip, today_date):
  response = requests.get(nipValidationApiUrl + nip + '?date=' + today_date)
  print(response, response.json())
  return response.json()