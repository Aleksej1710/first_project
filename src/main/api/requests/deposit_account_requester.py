from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.requester import Requester
from src.main.api.models.deposit_account_response import DepositAccountResponse
import requests
from src.main.api.models.error_response import ErrorResponse

class DepositAccountRequester(Requester):
    def post(self, deposit_account_request: DepositAccountRequest):
        url = f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=deposit_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return DepositAccountResponse(**response.json())


    def post_expecting_error(self, deposit_account_request: DepositAccountRequest) -> ErrorResponse:
        url = f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=deposit_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return ErrorResponse(**response.json())
