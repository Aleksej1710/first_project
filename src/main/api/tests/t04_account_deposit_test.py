from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
class TestDepositAccount:
    def test_deposit_account_valid(self):
        create_user_request = CreateUserRequest(
            username="Usr1cLfl763", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="Usr1cLfl763", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response.balance == 0

        deposit_account_request = DepositAccountRequest(accountId=response.id, amount=5000)

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="Usr1cLfl763", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(deposit_account_request)

        assert deposit_account_response.balance == 5000
        assert deposit_account_response.id == response.id

    def test_deposit_account_invalid(self):
        create_user_request = CreateUserRequest(
            username="UsrAuMxGSvp", password="Pas!sw0rd", role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrAuMxGSvp", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response.balance == 0

        deposit_account_request = DepositAccountRequest(accountId=response.id, amount=999)

        error_response = DepositAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrAuMxGSvp", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad(),
        ).post_expecting_error(deposit_account_request)

        assert error_response.error == "Amount must be between 1000 and 9000"
