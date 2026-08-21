from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session
from sqlalchemy import or_


class TransactionCrudDb:
    @staticmethod
    def get_last_transaction_by_account_id(db: Session, account_id: int) -> Transaction | None:
        return (
            db.query(Transaction)
            .filter(
                or_(
                    Transaction.to_account_id == account_id,
                    Transaction.from_account_id == account_id,
                )
            )
            .order_by(Transaction.id.desc())
            .first()
        )