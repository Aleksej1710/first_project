from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
import allure
from src.main.api.configs.config import Config

class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        with allure.step(
            f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validate Model"
        ):
            response = self.crud_requester.post(model)
            result = self.endpoint.value.response_model.model_validate(response.json())
            allure.attach(
                f"Validate Model response: {self.endpoint.value.response_model.__name__}",
                "Model validation",
                allure.attachment_type.TEXT,
            )
            return result

    def delete(self, user_id: int):
        """Из обучающего курса, в проекте не используется.

        Оставлено для сравнения. В рабочем виде метод не годится: разбирает
        ответ по `response_model` эндпоинта, а у `ADMIN_DELETE_USER` это поле
        равно None (см. `Endpoint`). Вызов `None.model_validate(...)` упадёт
        с AttributeError.

        Само тело ответа при этом валидное — сервер отдаёт
        {"message": "User deleted successfully"}, так что `response.json()`
        отрабатывает штатно. Проблема именно в отсутствующей модели.

        Уборка ходит напрямую через `CrudRequester.delete`
        (см. `AdminSteps.delete_user`).
        """
        response = self.crud_requester.delete(user_id)
        return self.endpoint.value.response_model.model_validate(response.json())
