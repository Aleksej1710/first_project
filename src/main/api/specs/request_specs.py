from src.main.api.foundation.endpoint import Endpoint
import requests
from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse

class RequestSpecs:

    @staticmethod
    def base_headers():
        return {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    @staticmethod
    def authentication_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url = f"{Config.fetch('backendUrl')}{Endpoint.LOGIN_USER.value.url}",
            json=request.model_dump(),
            headers = RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")

    @staticmethod
    def admin_headers():
        """Логин администратором. Креды берутся из окружения, в коде их нет."""
        return RequestSpecs.authentication_headers(
            username=Config.fetch("ADMIN_USERNAME"),
            password=Config.fetch("ADMIN_PASSWORD"),
        )

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()
