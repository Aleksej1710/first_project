from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_account_request import CreditAccountRequest
from src.main.api.models.credit_account_response import CreditAccountResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.error_crud_requester import ErrorCrudRequester

class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.authentication_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse, amount: float):
        deposit_account_request = DepositAccountRequest(
            accountId=create_account_response.id,
            amount=amount,
        )
        response = ValidateCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse, amount: float):
        deposit_account_request = DepositAccountRequest(
            accountId=create_account_response.id,
            amount=amount,
        )
        response = ErrorCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(deposit_account_request)
        return response

    def transfer_account(self, create_user_request: CreateUserRequest, from_account_response: CreateAccountResponse, to_account_response: CreateAccountResponse, amount: float):
        transfer_account_request = TransferAccountRequest(
            fromAccountId=from_account_response.id,
            toAccountId=to_account_response.id,
            amount=amount,
        )
        response = ValidateCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(transfer_account_request)
        return response

    def transfer_account_invalid(self, create_user_request: CreateUserRequest, from_account_response: CreateAccountResponse, to_account_response: CreateAccountResponse, amount: float):
        transfer_account_request = TransferAccountRequest(
            fromAccountId=from_account_response.id,
            toAccountId=to_account_response.id,
            amount=amount,
        )
        response = ErrorCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(transfer_account_request)
        return response

    def credit_account(self, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse, amount: float, term_months: int):
        credit_account_request = CreditAccountRequest(
            accountId=create_account_response.id,
            amount=amount,
            termMonths=term_months,
        )
        response = ValidateCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.CREDIT_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post(credit_account_request)
        return response

    def credit_account_invalid(self, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse, amount: float, term_months: int):
        credit_account_request = CreditAccountRequest(
            accountId=create_account_response.id,
            amount=amount,
            termMonths=term_months,
        )
        response = ErrorCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.CREDIT_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(credit_account_request)
        return response

    def repay_credit_account(self, create_user_request: CreateUserRequest, credit_account_response: CreditAccountResponse, amount: float):
        repay_credit_request = RepayCreditRequest(
            creditId=credit_account_response.creditId,
            accountId=credit_account_response.id,
            amount=amount
        )
        response = ValidateCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.REPAY_CREDIT_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(repay_credit_request)
        return response

    def repay_credit_account_invalid(self, create_user_request: CreateUserRequest, credit_account_response: CreditAccountResponse, amount: float):
        repay_credit_request = RepayCreditRequest(
            creditId=credit_account_response.creditId,
            accountId=credit_account_response.id,
            amount=amount
        )
        response = ErrorCrudRequester(
            RequestSpecs.authentication_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            Endpoint.REPAY_CREDIT_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(repay_credit_request)
        return response

