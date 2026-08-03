from src.main.api.models.error_response import ErrorResponse
import requests
from src.main.api.models.credit_account_response import CreditAccountResponse
from src.main.api.requests.requester import Requester
from src.main.api.models.credit_account_request import CreditAccountRequest

class CreditAccountRequester(Requester):
    def post(self, credit_account_request: CreditAccountRequest):
        url=f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return CreditAccountResponse(**response.json())

    def post_expecting_error(self, credit_account_request: CreditAccountRequest) -> ErrorResponse:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return ErrorResponse(**response.json())
