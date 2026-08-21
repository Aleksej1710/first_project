import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_transfer_double_account:
            tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse, float]):
        user, from_account, to_account, deposit_amount = user_transfer_double_account

        to_account_from_db = Account.get_account_by_id(db_session, to_account.id)
        assert to_account_from_db is not None, 'Счёт получателя не найден в БД'
        assert to_account_from_db.balance == 0, 'Счёт получателя создан не с нулевым балансом'

        from_account_from_db = Account.get_account_by_id(db_session, from_account.id)
        assert from_account_from_db is not None, 'Счёт отправителя не найден в БД'
        assert from_account_from_db.balance == deposit_amount, 'Фикстура не положила деньги отправителю'

        transfer_amount = 3000

        api_manager.user_steps.transfer_account(user, from_account, to_account, transfer_amount)
        db_session.expire_all()

        assert to_account_from_db.balance == transfer_amount, 'Деньги не зачислены получателю'

        transaction_from_db = Transaction.get_last_transaction_by_account_id(db_session, from_account.id)

        assert transaction_from_db is not None, 'Транзакция перевода не записана в БД'
        assert transaction_from_db.transaction_type == "transfer", 'Тип транзакции в БД не transfer'
        assert transaction_from_db.from_account_id == from_account.id, 'В транзакции неверный счёт-источник'
        assert transaction_from_db.to_account_id == to_account.id, 'В транзакции неверный счёт-получатель'
        assert transaction_from_db.amount == transfer_amount, 'Сумма транзакции не совпадает с переводом'
        assert from_account_from_db.balance == deposit_amount - transfer_amount, 'Деньги не списаны с отправителя'

    def test_transfer_account_invalid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_transfer_double_account:
            tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse, float]):
        user, from_account, to_account, deposit_amount = user_transfer_double_account

        from_account_from_db = Account.get_account_by_id(db_session, from_account.id)
        assert from_account_from_db is not None, 'Счёт отправителя не найден в БД'
        assert from_account_from_db.balance == deposit_amount, 'Фикстура не положила деньги отправителю'

        to_account_from_db = Account.get_account_by_id(db_session, to_account.id)
        assert to_account_from_db is not None, 'Счёт получателя не найден в БД'
        assert to_account_from_db.balance == 0, 'Счёт получателя создан не с нулевым балансом'

        transfer_amount = 0
        response = api_manager.user_steps.transfer_account_invalid(user, from_account, to_account, transfer_amount)

        assert response.error == (
            "Amount must be greater than 0\nAmount must be between 500 and 10000"
        ), 'Сервис не отклонил недопустимую сумму'
        db_session.expire_all()

        assert from_account_from_db.balance == deposit_amount, 'Баланс отправителя изменился, хотя перевод отклонён'
        assert to_account_from_db.balance == 0, 'Баланс получателя изменился, хотя перевод отклонён'

        transaction_from_db = Transaction.get_last_transaction_by_account_id(db_session, from_account.id)
        assert transaction_from_db is not None, 'Депозит из фикстуры не найден в БД'
        assert transaction_from_db.transaction_type == "deposit", 'Перевод записан в БД, хотя был отклонён'
