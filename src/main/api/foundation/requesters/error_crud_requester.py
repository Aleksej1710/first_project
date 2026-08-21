from typing import Optional
from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.models.error_response import ErrorResponse
import allure

class ErrorCrudRequester(HttpRequester):
    """Отправляет запрос, для которого ожидается отказ сервера.

    Работает так же, как ValidateCrudRequester, но разбирает тело ответа
    по модели ошибки, а не по модели успешного ответа эндпоинта.
    Ожидаемый статус задаётся через response_spec (например, request_bad).
    """

    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec,
        )

    def post(self, model: Optional[BaseModel] = None) -> ErrorResponse:
        with allure.step(
            f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validate Error Model"
        ):
            response = self.crud_requester.post(model)
            result = ErrorResponse.model_validate(response.json())
            allure.attach(
                f"Error Model response: {ErrorResponse.__name__}",
                "Model validation",
                allure.attachment_type.TEXT,
            )
            return result