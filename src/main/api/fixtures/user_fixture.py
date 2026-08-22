import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.amount_range import DEPOSIT_AMOUNT_RANGE
from src.main.api.generators.amount_range import CREDIT_AMOUNT_RANGE
from src.main.api.fixtures.fixture_models import UserWithAccount, UserWithTwoAccounts, UserWithCredit


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def user_with_account(api_manager, create_user_request):
    create_account_response = api_manager.user_steps.create_account(create_user_request)
    return UserWithAccount(user=create_user_request, account=create_account_response)


@pytest.fixture
def transfer_accounts(api_manager, create_user_request):
    deposit_amount = DEPOSIT_AMOUNT_RANGE.random_value()
    from_account_response = api_manager.user_steps.create_account(create_user_request)
    to_account_response = api_manager.user_steps.create_account(create_user_request)
    api_manager.user_steps.deposit_account(create_user_request, from_account_response, deposit_amount)
    return UserWithTwoAccounts(
        user=create_user_request,
        from_account=from_account_response,
        to_account=to_account_response,
        deposit_amount=deposit_amount,
    )


@pytest.fixture
def user_credit_account(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    create_account_response = api_manager.user_steps.create_account(user_request)
    return UserWithAccount(user=user_request, account=create_account_response)


@pytest.fixture
def user_repay_credit(api_manager, user_credit_account):
    amount = CREDIT_AMOUNT_RANGE.random_value()
    term_months = 12
    credit_account_response = api_manager.user_steps.credit_account(
        user_credit_account.user, user_credit_account.account, amount, term_months
    )
    return UserWithCredit(user=user_credit_account.user, credit=credit_account_response)
