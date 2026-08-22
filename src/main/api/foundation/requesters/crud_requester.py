from typing import Optional
import requests
from requests import Response
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.configs.config import Config
import allure
import json

class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST to {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(
                json.dumps(body, indent=2, ensure_ascii=False),
                "Request body",
                allure.attachment_type.JSON
            )

            response = requests.post(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
                headers= self.request_spec,
                json= body
            )

            allure.attach(
                response.text,
                'Response body',
                allure.attachment_type.JSON
            )

            self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        with allure.step(
            f"DELETE to {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"
        ):
            response = requests.delete(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}",
                headers=self.request_spec,
            )

            allure.attach(
                response.text,
                'Response body',
                allure.attachment_type.JSON,
            )

            self.response_spec(response)
        return response