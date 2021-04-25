import json
import math
import os


def get_id_number(bank_name, banks_dict):
    """
    method creates id for new user
    id depends on bank and of how many user bank have
    banks_dict: allows to find id for first bank user
    return id_number
    """
    if banks_dict[bank_name]:
        bank = banks_dict[bank_name]
        last_client = bank[len(bank) - 1]
        return last_client["ID"] + 1
    else:
        i = 1
        for bank in banks_dict:
            if bank == bank_name:
                return i * 100
            i += 1


def find_person_by_id(number_id, banks_dict):
    """
    method search for user data with id_number, if id doesn't exist raise an Exception
    return dictionary "client" with all data about client
    """
    for bank in banks_dict:
        for user in banks_dict[bank]:
            if user["ID"] == number_id:
                return user

    raise Exception("There is not such id number")


def get_bank_name(number_id, bank_names):
    # method looks for user bank name, by his/hers id, and returns this name
    return bank_names[math.floor(number_id / 100) - 1]


def banks_names(banks_dict):
    # method create a list with bank names, and returns it
    bank_names = []
    for key in banks_dict:
        bank_names.append(key)
    return bank_names


def add_client(user_name, user_surname, user_age, bank_name, banks_dict):
    """ method create a dictionary with data about client, and add client to bank list
        returns id for user information
    """
    number_id = get_id_number(bank_name, banks)
    new_client = {"name": user_name, "surname": user_surname, "age": user_age, "ID": number_id, "funds": 0, "loan": 0}
    banks_dict[bank_name].append(new_client)
    return number_id


def withdrawal(user, money, banks_dict):
    # check if there is a possibility to make a withdrawal, if not make a withdrawal, else raise exception
    user = find_person_by_id(user["ID"], banks_dict)
    if money > user["funds"]:
        raise Exception("You don't have enough money on your account")

    else:
        user["funds"] -= money


def deposit(user, money):
    user["funds"] += money


def credit(user, money):
    user["loan"] -= money


def loan_repayment(user, money):
    # check if user need to pay off, if amount of money is bigger than loan, than raise an exception
    if user["loan"] + money <= 0:
        user["loan"] += money
    else:
        raise Exception("You don't have this big loan")


def transfer(user, payee_id, money, banks_dict):
    # check if user have enough money to make transfer, if not raise exception, else make transfer
    if money > user["funds"]:
        raise Exception("You don't have enough money on your account")
    else:
        payee = find_person_by_id(payee_id, banks_dict)
        user["funds"] -= money
        payee["funds"] += money


def delete_account(user, bank):
    # delete account if user doesn't have a loan
    if user["loan"] < 0:
        raise Exception("You can't delete account with a loan")
    else:
        bank.remove(user)


def change_bank(user, banks_dict, new_bank_name, last_bank_name):
    # change bank if user doesn't have a loan (change : create new account, delete old one
    if user["loan"] < 0:
        raise Exception("You can't change account when you have a loan")
    else:
        new_user = user
        new_user["ID"] = get_id_number(new_bank_name, banks_dict)
        banks_dict[last_bank_name].remove(user)
        banks[new_bank_name].append(new_user)
        return new_user["ID"]


def add_bank(banks_dict, bank, bank_name, bank_names):
    # add bank to dictionary,and update bank_names list
    banks_dict[bank_name] = bank
    bank_names.append(bank_name)


def try_if_int(variable):
    # check if variable can be converted to in, if not raise an exception
    try:
        int(variable)
        return True
    except ValueError:
        raise Exception("This is not an integer")


if __name__ == "__main__":

    # check if file exist, if exist upload data to variable 'banks', else create dictionary 'banks'
    if os.path.exists("data.json"):
        with open("data.json", 'r') as json_file:
            banks = json.load(json_file)
    else:
        banks = {}

    names = banks_names(banks)  # create list with banks names

    # create data
    add_bank(banks, [], "mBank", names)

    add_client("Zofia", "Misiewicz", 36, "mBank", banks)
    add_client("Franciszek", "Wiosna", 70, "mBank", banks)
    add_client("Konstanty", "Wajda", 24, "mBank", banks)

    add_bank(banks, [], "ING Bank Slaski", names)

    add_client("Elena", "Wolska", 40, "ING Bank Slaski", banks)
    add_client("Jakub", "Kondrat", 55, "ING Bank Slaski", banks)
    add_client("Maciej", "Blicharczyk", 33, "ING Bank Slaski", banks)

    bank1 = banks[names[0]]
    bank3 = banks['mBank']
    bank4 = banks['ING Bank Slaski']
    bank2 = banks[names[1]]

    # testing methods
    deposit(bank3[0], 13568)
    deposit(bank3[1], 240678)
    deposit(bank3[2], 300)
    withdrawal(bank3[0], 3000, banks)
    delete_account(bank3[2], bank3)
    deposit(bank4[0], 130000)
    deposit(bank4[1], 3490)
    deposit(bank4[2], 690)
    change_bank(bank4[0], banks, "mBank", "ING Bank Slaski")
    credit(bank1[0], 2000)
    withdrawal(bank1[1], 20, banks)
    loan_repayment(bank1[0], 150)
    delete_account(bank1[2], bank1)
    transfer(bank2[2], 100, 20, banks)
    withdrawal(bank3[0], 200, banks)
    transfer(bank4[1], 300, 30, banks)
    delete_account(bank2[1], bank2)

    operation_number = 0
    # interaction with user
    while operation_number != 9:
        operation_number = input(
            "If you would like to:\n -check your funds -press 0 \n"
            " - create an account - press 1\n -make a withdrawal - press 2 \n"
            " -make a deposit - press 3 \n -take a credit - press 4 \n"
            " - make a loan repayment -press 5 \n - make a transfer - press 6 \n"
            " -change a bank -press 7 \n -delete account - press 8 \n if you want to close menu- press 9 \n")

        if try_if_int(operation_number):
            operation_number = int(operation_number)
            if operation_number < 0 or operation_number > 9:
                print("Something went wrong, please try again")

        if operation_number == 1:
            name = input("type your name: ")
            surname = input("type your surname: ")
            age = input("type your age: ")
            if try_if_int(age):
                age = int(age)
            i = 1
            for name in names:
                print("{} {}".format(i, name))
                i += 1

            which_bank = int(input("which bank would you like to choose? Press number \n "))
            name = names[which_bank - 1]
            id_number = add_client(name, surname, age, name, banks)
            print("operation was successful, your new ID: {}".format(id_number))

        elif operation_number < 9:
            id_number = input("Enter you ID number: ")
            if try_if_int(id_number):
                id_number = int(id_number)
            client = find_person_by_id(id_number, banks)

            if operation_number == 0:
                txt = "there is {} on your account"
                print(txt.format(client["funds"]))

            if operation_number == 2:
                cash = input("Enter the amount you want to withdrawal: ")
                if try_if_int(cash):
                    cash = int(cash)
                withdrawal(client, cash, banks)
                print("operation was successful")

            if operation_number == 3:
                cash = input("Enter the amount you want to deposit: ")
                if try_if_int(cash):
                    cash = int(cash)
                deposit(client, cash)
                print("operation was successful")

            if operation_number == 4:
                cash = input("Enter the amount of the loan: ")
                if try_if_int(cash):
                    cash = int(cash)
                credit(client, cash)
                print("operation was successful")

            if operation_number == 5:
                cash = input("Enter the amount of the loan repayment: ")
                if try_if_int(cash):
                    cash = int(cash)
                loan_repayment(client, cash)
                print("operation was successful")

            if operation_number == 6:
                cash = input("Enter the amount of the transfer: ")
                if try_if_int(cash):
                    cash = int(cash)
                id_payee = int(input("Enter payee ID: "))
                transfer(client, id_payee, cash, banks)
                print("operation was successful")

            if operation_number == 7:
                name = get_bank_name(client["ID"], names)
                i = 1
                for name in names:
                    if name != name:
                        print("{} {}".format(i, name))
                    i += 1
                which_bank = int(input("Which bank would you like to choose? Press the number \n "))
                new_id = change_bank(client, banks, names[which_bank - 1], name)
                print("Operation was successful, your new ID in new bank is {}".format(new_id))

            if operation_number == 8:
                name = get_bank_name(client["ID"], names)
                print(name)
                delete_account(client, banks[name])
                print("operation was successful")

    # saving data to json file
    with open('data.json', 'w') as outfile:
        json.dump(banks, outfile, indent=4)
