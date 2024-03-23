from models.__all_models import *
from conf.db_session import create_session
from sqlalchemy import select
from utils import generate_account_number, check_if_account_number_exist


def insert_address() -> Address:
    print("*" * 30)

    street_name: str = input('Informe o nome da rua: ')
    number: int = int(input('Informe o número: '))
    neighborhood: str = input('Informe o bairro: ')
    state: str = input('Informe o estado: ')

    address: Address = Address(
        street_name=street_name,
        number=number,
        neighborhood=neighborhood,
        state=state)

    with create_session() as session:
        session.add(address)

        session.commit()

    return address


def insert_account() -> Account:
    account_number_ = generate_account_number()
    account_number_is_valid = check_if_account_number_exist(account_number=account_number_)

    if not account_number_is_valid:
        return

    agency_number: str = "001"
    account_number: str = account_number_
    withdraw_value_limit: str = "500"
    account_balance: float = 0.00
    withdraw_quantity_limit: int = 3

    account: Account = Account(
        agency_number=agency_number,
        account_number=account_number,
        withdraw_value_limit=withdraw_value_limit,
        account_balance=account_balance,
        withdraw_quantity_limit=withdraw_quantity_limit)

    with create_session() as session:
        session.add(account)

        session.commit()

    return account


def insert_client() -> Client:
    address = insert_address()
    account = insert_account()

    nome: str = input("Insira seu nome completo: ")
    birthday: str = input("Informe sua data de nascimento: ")
    cpf: str = input("Informe seu número de CPF: ")

    client: Client = Client(
        name=nome,
        birthday=birthday,
        cpf=cpf,
        address_id=address.id
    )

    client.accounts.append(account)

    with create_session() as session:
        session.add(client)

        session.commit()

    return client
