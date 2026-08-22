import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.fixture_models import UserWithCredit


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_valid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_repay_credit: UserWithCredit):

        account_from_db = Account.get_account_by_id(db_session, user_repay_credit.credit.id)
        assert account_from_db.balance == user_repay_credit.credit.balance, 'Фикстура не выдала кредит на счёт'
        credit_from_db = Credit.get_credit_by_id(db_session, user_repay_credit.credit.creditId)
        assert credit_from_db.balance == -user_repay_credit.credit.amount, 'Фикстура не записала долг по кредиту'

        amount = user_repay_credit.credit.amount
        response = api_manager.user_steps.repay_credit_account(
            user_repay_credit.user, user_repay_credit.credit, amount
        )
        assert response.amountDeposited == amount, 'Сервис принял в погашение не ту сумму'
        assert response.creditId == user_repay_credit.credit.creditId, 'Погашение отнесено к другому кредиту'
        db_session.expire_all()

        assert credit_from_db.balance == 0, 'Долг не закрыт после полного погашения'
        assert account_from_db.balance == 0, 'Деньги не списаны со счёта при погашении'

    def test_repay_credit_invalid(
            self, db_session: Session,
            api_manager: ApiManager,
            user_repay_credit: UserWithCredit):

        account_from_db = Account.get_account_by_id(db_session, user_repay_credit.credit.id)
        assert account_from_db.balance == user_repay_credit.credit.balance, 'Фикстура не выдала кредит на счёт'
        credit_from_db = Credit.get_credit_by_id(db_session, user_repay_credit.credit.creditId)
        assert credit_from_db.balance == -user_repay_credit.credit.amount, 'Фикстура не записала долг по кредиту'

        amount = 0
        response = api_manager.user_steps.repay_credit_account_invalid(
            user_repay_credit.user, user_repay_credit.credit, amount
        )
        assert response.error == "Amount must be greater than 0", 'Сервис не отклонил недопустимую сумму'
        db_session.expire_all()

        assert credit_from_db.balance == -user_repay_credit.credit.amount, (
            'Долг изменился, хотя погашение отклонено'
        )
        assert account_from_db.balance == user_repay_credit.credit.balance, (
            'Баланс изменился, хотя погашение отклонено'
        )
