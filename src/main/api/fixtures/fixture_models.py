from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_account_response import CreditAccountResponse


class UserWithAccount(BaseModel):
    user: CreateUserRequest
    account: CreateAccountResponse


class UserWithTwoAccounts(BaseModel):
    user: CreateUserRequest
    from_account: CreateAccountResponse
    to_account: CreateAccountResponse
    deposit_amount: float


class UserWithCredit(BaseModel):
    user: CreateUserRequest
    credit: CreditAccountResponse