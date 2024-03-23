from unicodedata import decimal
from decimal import Decimal
from sqlalchemy import (BigInteger, Integer,
                        Column, DateTime,
                        DECIMAL, String)
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import create_session


class Account(ModelBase):
    __tablename__: str = "accounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)

    agency_number: str = Column(String(45), nullable=False)
    account_number: str = Column(String(45), unique=True, nullable=False)
    withdraw_value_limit: int = Column(Integer, nullable=False)
    account_balance: float = Column(DECIMAL(8, 2), nullable=False)
    withdraw_quantity_limit: int = Column(Integer, nullable=False)

    def withdraw(self, withdraw_value):
        if self.withdraw_quantity_limit == 0:
            raise f"Limite de saque excedido. \n"
        else:
            if withdraw_value > self.withdraw_value_limit:
               raise f"Valor por saque excedido! \n"
            elif self.account_balance < withdraw_value:
                raise f"Não foi possível efetuar o saque por falta de saldo!"
            else:
                self.account_balance -= Decimal(str(withdraw_value))
                self.withdraw_quantity_limit -= 1

    def deposit(self, value):
        self.account_balance += Decimal(str(value))

