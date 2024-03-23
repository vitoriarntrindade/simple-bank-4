import random
from typing import List, Dict
import csv
from conf.db_session import create_session
from models.account import Account


def read_csv_and_retrieve_accounts(file_name: str) -> List[Dict]:
    with open(file_name, mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=";")

        accounts = []
        for i, row in enumerate(leitor_csv):
            if len(row) == 0:
                continue
            dict = {
                "name": row[0],
                "birthday": row[1],
                "cpf": row[2],
                "street_name": row[3],
                "number": row[4],
                "neighborhood": row[5],
                "state": row[6],
            }

            accounts.append(dict)
        return accounts


def generate_account_number():
    numero_cinco_digitos = random.randint(10000, 99999)
    numero_dois_digitos = random.randint(10, 99)

    return f'{numero_cinco_digitos}-{numero_dois_digitos}'


print(generate_account_number())


def check_if_account_number_exist(account_number: str) -> bool:
    with create_session() as session:
        account = session.query(Account).filter(Account.account_number == account_number).first()

    if not account:
        return True

    return False


def cpf_formatter(cpf: str):
    cpf_formatted = cpf.replace(".", "").replace("-", "")
    return cpf_formatted


def make_transaction(origin_account_number, destination_account_number, value):
    with create_session() as session:
        account_origin = session.query(Account).filter(
            Account.account_number == origin_account_number).first()
        account_origin.withdraw(value)

        destination_account = session.query(Account).filter(
            Account.account_number == destination_account_number).first()
        destination_account.deposit(value)

        session.add(account_origin)
        session.add(destination_account)
        session.commit()
