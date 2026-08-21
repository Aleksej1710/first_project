import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_account_response import CreditAccountResponse
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_valid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_repay_credit: tuple[CreateUserRequest, CreditAccountResponse]):
        create_user_request, credit_account_response = user_repay_credit

        account_from_db = Account.get_account_by_id(db_session, credit_account_response.id)
        assert account_from_db is not None, 'Счёт из фикстуры не найден в БД'
        assert account_from_db.balance == credit_account_response.balance, 'Фикстура не выдала кредит на счёт'

        credit_from_db = Credit.get_credit_by_id(db_session, credit_account_response.creditId)
        assert credit_from_db is not None, 'Кредит из фикстуры не найден в БД'
        assert credit_from_db.balance == -credit_account_response.amount, 'Фикстура не записала долг по кредиту'

        amount = 5000
        response = api_manager.user_steps.repay_credit_account(create_user_request, credit_account_response, amount)

        assert response.amountDeposited == amount, 'Сервис принял в погашение не ту сумму'
        assert response.creditId == credit_account_response.creditId, 'Погашение отнесено к другому кредиту'

        db_session.expire_all()

        assert credit_from_db is not None, 'Кредит пропал из БД после погашения'
        assert credit_from_db.balance == 0, 'Долг не закрыт после полного погашения'
        assert account_from_db.balance == 0, 'Деньги не списаны со счёта при погашении'

    def test_repay_credit_invalid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_repay_credit: tuple[CreateUserRequest, CreditAccountResponse]):
        create_user_request, credit_account_response = user_repay_credit

        account_from_db = Account.get_account_by_id(db_session, credit_account_response.id)
        assert account_from_db is not None, 'Счёт из фикстуры не найден в БД'
        assert account_from_db.balance == credit_account_response.balance, 'Фикстура не выдала кредит на счёт'

        credit_from_db = Credit.get_credit_by_id(db_session, credit_account_response.creditId)
        assert credit_from_db is not None, 'Кредит из фикстуры не найден в БД'
        assert credit_from_db.balance == -credit_account_response.amount, 'Фикстура не записала долг по кредиту'

        amount = 0
        response = api_manager.user_steps.repay_credit_account_invalid(
            create_user_request, credit_account_response, amount
        )

        assert response.error == "Amount must be greater than 0", 'Сервис не отклонил недопустимую сумму'
        db_session.expire_all()

        assert credit_from_db is not None, 'Кредит пропал из БД после отклонённого погашения'
        assert credit_from_db.balance == -credit_account_response.amount, 'Долг изменился, хотя погашение отклонено'
        assert account_from_db.balance == credit_account_response.balance, 'Баланс изменился, хотя погашение отклонено'
