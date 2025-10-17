from flask import Flask, request, jsonify
from app.AccountRegistry import AccountRegistry
from app.PrivateAccount import PrivateAccount

app = Flask(__name__)


@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request with data: {data}")
    if AccountRegistry.search_account(data["pesel"]):
        return jsonify({"error": "Account already exists!"}), 409
    
    account = PrivateAccount(
        data["firstName"], data["lastName"], data["pesel"])
    AccountRegistry.add_account(account)
    return jsonify({"message": "Account created!"}), 201


@app.route("/api/accounts/count", methods=['GET'])
def get_number_of_accounts():
    number_of_accounts = AccountRegistry.get_number_of_accounts()
    return jsonify({"message": number_of_accounts}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def search_account_by_pesel(pesel):
    account = AccountRegistry.search_account(pesel)
    if account:
        return jsonify({"firstName": account.firstName, "lastName": account.lastName, "pesel": account.pesel, "balance": account.balance}), 200
    return jsonify({"error": "Account not found!"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    # body params
    new_data = request.get_json()
    try:
        account = AccountRegistry.update_account(pesel, new_data)
        if account:  
            return jsonify({"message": "Account succesfully updated!"}), 200
        return jsonify({"error": "Account not found!"}), 404
    
    except (NameError, AttributeError) as e:
        print(e)
        return jsonify({"error": "Bad request!"}), 400

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    if (AccountRegistry.delete_account(pesel)):
        return jsonify({"message": "Account deleted succesfully!"}), 200
    return jsonify({"error": "Account not found!"}), 404

@app.route("/api/accounts/DROP_TABLE", methods=['DELETE'])
def delete_database_data():
    try:    
      AccountRegistry.DROP_TABLE()
      return jsonify({"message": "Accounts table was successfully cleared!"}), 200
    except:
      return jsonify({"message": "Error clearing accounts table!"}), 400
    
@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_transfer(pesel):
  account = AccountRegistry.search_account(pesel)
  if account == None:
    return jsonify({"error": "Account not found!"}), 404
  
  data = request.get_json()
  sum = data["sum"]
  type = data["type"]

  if type == "incoming":
    account.incoming_transfer(sum)
    return jsonify({"message": "Order accepted for processing"}), 200
  
  elif type == "outgoing":
    account.outgoing_transfer(sum)
    return jsonify({"message": "Order accepted for processing"}), 200
  
  else:
    return jsonify({"error": "Bad request!"}), 400

@app.route("/api/accounts/save", methods=['POST'])
def save_accounts():
  AccountRegistry.save()
  return jsonify({"message": "Accounts saved succesfully!"}), 201
  
@app.route("/api/accounts/load", methods=['GET'])
def load_accounts():
  accounts = AccountRegistry.load()
  return jsonify({"message": len(accounts)}), 200

     