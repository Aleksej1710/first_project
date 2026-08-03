import requests
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.requests.requester import Requester
from src.main.api.models.error_response import ErrorResponse

class TransferAccountRequester(Requester):
    def post(self, transfer_account_request: TransferAccountRequest):
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return TransferAccountResponse(**response.json())

    def post_expecting_error(self, transfer_account_request: TransferAccountRequest) -> ErrorResponse:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return ErrorResponse(**response.json())