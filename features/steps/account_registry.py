from behave import *

from selenium.webdriver.common.keys import Keys
import requests
from unittest_assertions import AssertEqual


assert_equal = AssertEqual()
URL = "http://localhost:5000"


@when('I create an account using name: "{firstName}", last name: "{lastName}", pesel: "{pesel}"')
def create_account(context, firstName, lastName, pesel):
    json_body = {"firstName": f"{firstName}", "lastName": f"{lastName}", "pesel": f"{pesel}"}
    response = requests.post(URL + "/api/accounts", json=json_body)
    assert_equal(response.status_code, 201)


@step('Number of accounts in registry equals: "{count}"')
def check_number_of_accounts_in_registry(context, count):
    number_of_accounts = requests.get(URL + "/api/accounts/count")
    assert_equal(number_of_accounts.json()["message"], int(count))


@step('Account with pesel "{pesel}" exists in registry')
def check_if_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 200)

@step('Account with pesel "{pesel}" does not exists in registry')
def check_if_account_with_pesel_doesnt_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 404)

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    message = requests.delete(URL + f"/api/accounts/{pesel}")
    assert_equal(message.json(), {"message": "Account deleted succesfully!"})


@when("I save the account registry")
def save_accounts(context):
    resp = requests.post(URL + f"/api/accounts/save")
    assert_equal(resp.status_code, 201)


@when("I load the account registry")
def load_accounts(context):
    resp = requests.get(URL  + f"/api/accounts/load")
    assert_equal(resp.status_code, 200)


@when('I update last name in account with pesel "{pesel}" to "{last_name}"')
def update_last_name(context, pesel, last_name):
    response = requests.patch(URL + f"/api/accounts/{pesel}", json={"lastName": last_name})
    assert_equal(response.status_code, 200)


@then('The last name of account with pesel "{pesel}" is "{last_name}"')
def check_last_name(context, pesel, last_name):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.json()['lastName'], last_name)
