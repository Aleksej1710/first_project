import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_with_account(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    return create_user_request, create_account_response

@pytest.fixture
def user_transfer_double_account(api_manager, create_user_request):
    deposit_amount = 5000
    from_account_response = api_manager.user_steps.create_account(create_user_request)
    to_account_response = api_manager.user_steps.create_account(create_user_request)
    api_manager.user_steps.deposit_account(create_user_request, from_account_response, deposit_amount)
    return create_user_request, from_account_response, to_account_response, deposit_amount

@pytest.fixture
def user_credit_account(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    create_account_response = api_manager.user_steps.create_account(user_request)
    return user_request, create_account_response

@pytest.fixture
def user_repay_credit(api_manager, user_credit_account):
    create_user_request, create_account_response = user_credit_account
    amount = 5000
    term_months = 12
    credit_account_response = api_manager.user_steps.credit_account(create_user_request, create_account_response, amount, term_months)
    return create_user_request, credit_account_response



    
