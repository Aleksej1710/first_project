from src.main.api.models.credit_account_request import CreditAccountRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.credit_account_requester import CreditAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.error_response import ErrorResponse

class TestCreateCredit:
    def test_create_credit_valid(self):
        create_user_request = CreateUserRequest(
            username="UsriB7duRkw", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(request_spec=RequestSpecs.admin_headers(),
                            response_spec=ResponseSpecs.request_ok(),
                            ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(
                username="UsriB7duRkw", password="Pas!sw0rd"
            ),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        credit_account_request = CreditAccountRequest(accountId=create_account_response.id, amount=5000, termMonths=12)

        credit_account_response = CreditAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsriB7duRkw", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_account_request)

        assert credit_account_response.balance == create_account_response.balance + credit_account_request.amount
        assert credit_account_response.termMonths == credit_account_request.termMonths 
        
    def test_create_credit_invalid(self):
        create_user_request = CreateUserRequest(username="UsraHo8mK9a", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsraHo8mK9a", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        credit_account_request = CreditAccountRequest(accountId=create_account_response.id, amount=50000, termMonths=12)

        error_response = CreditAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsraHo8mK9a", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad(),
        ).post_expecting_error(credit_account_request)

        assert error_response.error == "Amount must be between 5000 and 15000"