from models.__all_models import Account, Address, Client
from insert_model import *
from utils import read_csv_and_retrieve_accounts, cpf_formatter, make_transaction
import csv
from conf.db_session import create_session
from models.account import Account

bank_clients = []
account_incremental_number = 0

while True:
    operation = input("Which operation do you want to do?\n"
                      "[1] Create Account\n"
                      "[2] List Clients\n"
                      "[3] Creat accounts by CSV file\n"
                      "[4] Deposit\n"
                      "[5] Withdraw\n"
                      "[6] Transfer\n"
                      "[0] Logout \n")

    if operation == "1":

        client = insert_client()

        while True:
            result_input = input("Do you want to create another account to this client? Y/N:").lower()

            if result_input == "y":
                extra_account = insert_account()
                client.accounts.append(extra_account)

                with create_session() as session:
                    session.add(client)
                    session.commit()

            if result_input == "n":
                break

    if operation == "2":
        with create_session() as session:
            data_clients = session.query(Client).filter().all()
            for client in data_clients:
                print(f'\nNome: {client.name}')
                print(f'Endereço: {client.address.street_name}')
                for i in client.accounts:
                    print("Accounts:")
                    print("Account number: ", i.account_number)
                    print("Account Balance: ", i.account_balance)

    if operation == "3":
        file_name_input = input("Digite o nome do arquivo csv \n")
        try:
            if ".csv" not in file_name_input:
                accounts_csv = read_csv_and_retrieve_accounts(file_name=file_name_input + ".csv")
            else:
                accounts_csv = read_csv_and_retrieve_accounts(file_name=file_name_input)
        except:
            print('Arquivo não encontrado, verifique o nome do arquivo e tente novamente!')

        session = create_session()
        for account_ in accounts_csv:
            account = insert_account()
            client_address = Address()
            client_address.street_name = account_["street_name"]
            client_address.number = account_["number"]
            client_address.neighborhood = account_["neighborhood"]
            client_address.state = account_["state"]

            session.add(client_address)
            session.add(account)
            session.commit()

            client = Client()
            client.name = account_["name"]
            client.birthday = account_["birthday"]
            client.cpf = account_["cpf"]
            client.address_id = client_address.id
            client.accounts.append(account)

            session.add(client)
            session.commit()

        session.close()

    if operation == "4":
        deposit_amount = float(input("Enter the amount you wish to deposit: \n"))
        account_number = input("Enter the account number: \n")

        with create_session() as session:
            account = session.query(Account).filter(Account.account_number == account_number).one_or_none()
            account.deposit(value=deposit_amount)
            session.add(account)
            session.commit()

    if operation == "5":
        account_number = input("Enter the account number: \n")
        withdraw_value = float(input("Enter the withdraw amount: \n"))

        with create_session() as session:
            account = session.query(Account).filter(Account.account_number == account_number).one_or_none()
            account.withdraw(withdraw_value=withdraw_value)
            session.add(account)
            session.commit()

    if operation == "6":
        origin_account_number = input("Enter the origin account: \n")
        destination_account_number = input("Enter the destination account: \n")
        transfer_value = float(input("Enter the amount you wish to transfer: \n"))

        make_transaction(origin_account_number=origin_account_number,
                         destination_account_number=destination_account_number,
                         value=transfer_value)

    if operation == "0":
        break
