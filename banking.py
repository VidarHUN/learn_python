from random import randint
import sqlite3


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


MAIN_MENU = [
    "1. Create an account",
    "2. Log into account",
    "0. Exit"
]

SUB_MENU = [
    "1. Balance",
    "2. Add income",
    "3. Do transfer",
    "4. Close account",
    "5. Log out",
    "0. Exit"
]

IIN = 400000

class CreditCard:
    def __init__(self, card_number, pin, balance=0):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance

    def get_balance(self):
        print("Balance: {}".format(str(self.balance)))

    def get_card_number(self):
        return self.card_number

    def get_pin(self):
        return self.pin

    def close(self):
        cur.execute('DELETE FROM card WHERE number = "{}";'.format(self.card_number))
        conn.commit()
        print("The account has been closed!")

    def add_income(self):
        income = int(input("Enter income: \n").strip())
        self.balance += income
        cur.execute('UPDATE card SET balance = {} WHERE number = "{}";'.format(str(self.balance), self.card_number))
        conn.commit()
        print("Income was added!")

    def transfer(self):
        print("Transfer")
        card2 = input("Enter card number: \n").strip()
        cur.execute('SELECT * FROM card WHERE number = "{}";'.format(card2))
        record = cur.fetchone()
        print(card2)
        print(luhn_algorithm(card2[:15]))
        if card2 != luhn_algorithm(card2[:15]):
            print("Probably you made mistake in the card number. Please try again!")
            return
        if card2 == self.card_number:
            print("You can't transfer money to the same account!")
            return
        if record is None:
            print("Such a card does not exist.")
            return
        money = int(input("Enter how much money you want to transfer:\n").strip())
        if money > self.balance:
            print("Not enough money!")
            return
        self.balance -= money
        cur.execute('UPDATE card SET balance = {} WHERE number = "{}";'.format(str(self.balance), self.card_number))
        t_balance = int(record[3]) + money
        cur.execute('UPDATE card SET balance = {} WHERE number = "{}";'.format(str(t_balance), card2))
        conn.commit()
        print("Success!")

def create_table():
    global conn, cur
    cur.execute('CREATE TABLE card (id INTEGER NOT NULL PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
    conn.commit()


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def menu():
    print(*MAIN_MENU, sep='\n')


def submenu():
    print(*SUB_MENU, sep='\n')


def luhn_checker(nums):
    check_sum = 0
    check_offset = (len(nums) + 1) % 2
    for i, n in enumerate(nums):
        if (i + check_offset) % 2 == 0:
            n_ = int(n) * 2
            check_sum += n_ -9 if n_ > 9 else n_
        else:
            check_sum += int(n)
    return check_sum % 10


def luhn_algorithm(nums):
    modulo = luhn_checker(nums)
    if modulo == 0:
        nums += '0'
    else:
        nums += str(10-modulo)
    return nums


def gen_card_number():
    account_identifier = random_with_N_digits(9)
    return str(luhn_algorithm(str(IIN) + str(account_identifier)))


def gen_pin():
    return str(random_with_N_digits(4))


def gen_credit_card(card_number, pin):
    global conn, cur
    cur.execute('SELECT number FROM card WHERE number = "{}"'.format(card_number))
    record = cur.fetchone()
    if record is not None:
        return False
    else:
        cur.execute('INSERT INTO card (number, pin) VALUES ("{}", "{}")'.format(card_number, pin))
        conn.commit()
        print("Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}".format(card_number, pin))
        return True


def login():
    card_number = input("Enter your card number: ").strip()
    pin = input("Enter your PIN: ").strip()

    cur.execute('SELECT number, pin, balance FROM card WHERE number="{}" AND pin="{}"'.format(card_number, pin))
    credit_card = cur.fetchone()

    if credit_card is not None:
        print("You have successfully logged in!")
        return CreditCard(credit_card[0], credit_card[1], credit_card[2])
    else:
        print("Wrong card number or PIN!")
        return False


def logout():
    print("You have successfully logged out!")


def exit():
    print("Bye!")


while True:
    menu()
    choice = input().strip()
    if choice == "1":
        gen_credit_card(gen_card_number(), gen_pin())
    elif choice == "0":
        exit()
        break
    elif choice == "2":
        card = login()
        if not card:
            continue
        while True:
            submenu()
            choice = input().strip()
            if choice == "1":
                card.get_balance()
            elif choice == "2":
                card.add_income()
            elif choice == "3":
                card.transfer()
            elif choice == "4":
                card.close()
                continue
            elif choice == "5":
                logout()
            elif choice == "0":
                exit()
                break
        else:
            continue
        break
