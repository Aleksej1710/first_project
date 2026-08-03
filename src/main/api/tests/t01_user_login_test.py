import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester  # noqa: F811
from src.main.api.configs.config import Config

@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username=Config.fetch("ADMIN_USERNAME"), password=Config.fetch("ADMIN_PASSWORD"))

        response = LoginUserRequester(  # noqa: F821
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"


    def test_login_user(self):
        create_user_request = CreateUserRequest(username="UsrcwPvqT0q", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(  # noqa: F821
            request_spec=RequestSpecs.admin_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username="UsrcwPvqT0q", password="Pas!sw0rd")

        response = LoginUserRequester(  # noqa: F821
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"


