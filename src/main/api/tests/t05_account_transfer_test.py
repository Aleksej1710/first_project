from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.requests.transfer_account_requester import TransferAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.models.error_response import ErrorResponse

class TestTransferAccount:
    def test_transfer_account_valid(self):
        create_user_request = CreateUserRequest(
            username="UsrndCYy39n", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)


        """создание счета списания"""

        response_from = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrndCYy39n", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response_from.balance == 0

        deposit_account_request = DepositAccountRequest(accountId=response_from.id, amount=5000)

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrndCYy39n", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(deposit_account_request)

        """создание счета зачисления"""

        response_to = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrndCYy39n", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response_to.balance == 0

        transfer_account_request = TransferAccountRequest(
            fromAccountId=response_from.id, toAccountId=response_to.id, amount=3000
        )

        transfer_account_response = TransferAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrndCYy39n", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(transfer_account_request)

        assert  transfer_account_response.fromAccountIdBalance == deposit_account_response.balance - transfer_account_request.amount




    def test_transfer_account_invalid(self):
        create_user_request = CreateUserRequest(
            username="UsrlTplp4ba", password="Pas!sw0rd", role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        """создание счета списания"""

        response_from = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrlTplp4ba", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response_from.balance == 0

        deposit_account_request = DepositAccountRequest(accountId=response_from.id, amount=5000)

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrlTplp4ba", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(deposit_account_request)

        """создание счета зачисления"""

        response_to = CreateAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrlTplp4ba", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        assert response_to.balance == 0

        transfer_account_request = TransferAccountRequest.model_construct(
            fromAccountId=response_from.id, toAccountId=response_to.id, amount=None
        )

        error_response = TransferAccountRequester(
            request_spec=RequestSpecs.authentication_headers(username="UsrlTplp4ba", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad(),
        ).post_expecting_error(transfer_account_request)

        assert error_response.error == "Amount is required"
        