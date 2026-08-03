from src.main.api.requests.repay_credit_requester import RepayCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_account_request import CreditAccountRequest
from src.main.api.requests.credit_account_requester import CreditAccountRequester
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.error_response import ErrorResponse

class TestRepayCredit:
    def test_repay_credit_valid(self):
        create_user_request = CreateUserRequest(username="Usrz6AP8UH7", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="Usrz6AP8UH7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        credit_account_request = CreditAccountRequest(accountId=create_account_response.id, amount=5000, termMonths=12)

        credit_account_response = CreditAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="Usrz6AP8UH7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_account_request)

        repay_credit_request = RepayCreditRequest(creditId=credit_account_response.creditId, accountId=credit_account_response.id, amount=5000)

        repay_credit_response = RepayCreditRequester(
            request_spec=RequestSpecs.authentication_headers(username="Usrz6AP8UH7", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(repay_credit_request)

        assert repay_credit_response.amountDeposited == credit_account_response.amount


    def test_repay_credit_invalid(self):
        create_user_request = CreateUserRequest(
            username="UsryDE505KQ", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsryDE505KQ", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        credit_account_request = CreditAccountRequest(
            accountId=create_account_response.id, amount=5000, termMonths=12
        )

        credit_account_response = CreditAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsryDE505KQ", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_account_request)

        repay_credit_request = RepayCreditRequest(
            creditId=credit_account_response.creditId, accountId=credit_account_response.id, amount=0,
        )

        error_response = RepayCreditRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsryDE505KQ", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad(),
        ).post_expecting_error(repay_credit_request)

        assert error_response.error == "Amount must be greater than 0"