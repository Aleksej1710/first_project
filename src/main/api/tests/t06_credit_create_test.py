import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreateCredit:
    def test_create_credit_valid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_credit_account: tuple[CreateUserRequest, CreateAccountResponse]):
        user_request, create_account_response = user_credit_account

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert account_from_db is not None, 'Счёт из фикстуры не найден в БД'
        assert account_from_db.balance == 0, 'Новый счёт создан не с нулевым балансом'

        credit = 5000
        term_months = 12
        response = api_manager.user_steps.credit_account(user_request, create_account_response, credit, term_months)
        db_session.expire_all()

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert account_from_db is not None, 'Счёт пропал из БД после выдачи кредита'
        assert account_from_db.balance == credit, 'Кредитные средства не зачислены на счёт'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db is not None, 'Кредит не записан в БД'
        assert credit_from_db.amount == credit, 'Сумма кредита в БД не совпадает с запрошенной'
        assert credit_from_db.term_months == term_months, 'Срок кредита в БД не совпадает с запрошенным'
        assert credit_from_db.account_id == create_account_response.id, 'Кредит привязан к чужому счёту'

    def test_create_credit_invalid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_credit_account: tuple[CreateUserRequest, CreateAccountResponse]):
        user_request, create_account_response = user_credit_account

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert account_from_db is not None, 'Счёт из фикстуры не найден в БД'
        assert account_from_db.balance == 0, 'Новый счёт создан не с нулевым балансом'

        amount = 50000
        term_months = 12
        response = api_manager.user_steps.credit_account_invalid(
            user_request, create_account_response, amount, term_months
        )

        assert response.error == "Amount must be between 5000 and 15000", 'Сервис не отклонил недопустимую сумму'
        db_session.expire_all()

        assert account_from_db.balance == 0, 'Баланс изменился, хотя заявка на кредит отклонена'

        credit_from_db = Credit.get_credit_by_account_id(db_session, create_account_response.id)
        assert credit_from_db is None, 'Кредит создан, хотя заявка отклонена'
