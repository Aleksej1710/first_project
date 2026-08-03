from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.requests.requester import Requester
from src.main.api.models.error_response import ErrorResponse
import requests


class RepayCreditRequester(Requester):
    def post(self, repay_credit_request: RepayCreditRequest) -> RepayCreditResponse:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return RepayCreditResponse(**response.json())

    def post_expecting_error(self, repay_credit_request: RepayCreditRequest) -> ErrorResponse:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        return ErrorResponse(**response.json())
