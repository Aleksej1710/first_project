import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.generators.amount_range import DEPOSIT_AMOUNT_RANGE
from src.main.api.fixtures.fixture_models import UserWithAccount


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_with_account: UserWithAccount):

        account_from_db = Account.get_account_by_id(db_session, user_with_account.account.id)
        assert account_from_db.balance == 0, 'Новый счёт создан не с нулевым балансом'

        amount = DEPOSIT_AMOUNT_RANGE.random_value()
        api_manager.user_steps.deposit_account(user_with_account.user, user_with_account.account, amount)
        db_session.expire_all()

        assert account_from_db.balance == amount, 'Депозит не зачислен на счёт'

        transaction_from_db = Transaction.get_last_transaction_by_account_id(
            db_session, user_with_account.account.id
        )
        assert transaction_from_db is not None, 'Транзакция депозита не записана в БД'
        assert transaction_from_db.transaction_type == "deposit", 'Тип транзакции в БД не deposit'
        assert transaction_from_db.to_account_id == user_with_account.account.id, 'Депозит зачислен не на тот счёт'
        assert transaction_from_db.from_account_id is None, 'У депозита не должно быть счёта-источника'
        assert transaction_from_db.amount == amount, 'Сумма транзакции не совпадает с суммой депозита'

    def test_deposit_account_invalid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_with_account: UserWithAccount):

        account_from_db = Account.get_account_by_id(db_session, user_with_account.account.id)
        assert account_from_db.balance == 0, 'Новый счёт создан не с нулевым балансом'

        amount = 999
        response = api_manager.user_steps.deposit_account_invalid(
            user_with_account.user,
            user_with_account.account,
            amount
        )
        assert response.error == "Amount must be between 1000 and 9000", 'Сервис не отклонил недопустимую сумму'
        db_session.expire_all()

        assert account_from_db.balance == 0, 'Баланс изменился, хотя депозит отклонён'

        transaction_from_db = Transaction.get_last_transaction_by_account_id(db_session, user_with_account.account.id)
        assert transaction_from_db is None, 'Транзакция записана, хотя депозит отклонён'
