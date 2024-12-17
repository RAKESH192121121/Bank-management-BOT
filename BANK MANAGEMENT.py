import pickle
import os
import pathlib

# Class for Account Management
class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ""
        self.deposit = 0
        self.type = ""
        self.transactions = []

    def createAccount(self):
        self.accNo = int(input("Enter the account no: "))
        self.name = input("Enter the account holder name: ")
        self.type = input("Enter the type of account [C/S]: ")
        if self.type == 'S':
            self.deposit = float(input("Enter the Initial deposit (>=500 for Savings): "))
            if self.deposit < 500:
                print("Minimum deposit for savings account is 500.")
                return
        elif self.type == 'C':
            self.deposit = float(input("Enter the Initial deposit (>=1000 for Current): "))
            if self.deposit < 1000:
                print("Minimum deposit for current account is 1000.")
                return
        else:
            print("Invalid account type!")
            return
        self.transactions.append(f"Account created with initial deposit of {self.deposit}")
        print("\nAccount Created Successfully.")

    def showAccount(self):
        print("Account Number:", self.accNo)
        print("Account Holder Name:", self.name)
        print("Type of Account:", self.type)
        print("Balance:", self.deposit)
        print("Transaction History:", self.transactions)

    def depositAmount(self, amount):
        self.deposit += amount
        self.transactions.append(f"Deposited {amount}")
        print(f"{amount} deposited successfully!")

    def withdrawAmount(self, amount):
        if amount > self.deposit:
            print("Insufficient balance!")
        else:
            self.deposit -= amount
            self.transactions.append(f"Withdrew {amount}")
            print(f"{amount} withdrawn successfully!")

    def calculateInterest(self):
        if self.type == 'S':  # Interest for savings account
            interest = self.deposit * 0.04  # 4% interest annually
            self.deposit += interest
            self.transactions.append(f"Interest added: {interest}")
            print(f"Interest of {interest} added to the account.")

# Simple login system for authentication
def login(users_db):
    print("Login System")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users_db and users_db[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials, try again.")
        return None

# Admin menu for managing accounts
def adminMenu():
    while True:
        print("\nAdmin Menu")
        print("1. View all accounts")
        print("2. Delete account")
        print("3. Modify account")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            displayAll()
        elif choice == '2':
            num = int(input("Enter account number to delete: "))
            deleteAccount(num)
        elif choice == '3':
            num = int(input("Enter account number to modify: "))
            modifyAccount(num)
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

# User menu for interacting with their own account
def userMenu(username):
    while True:
        print("\nUser Menu")
        print("1. Deposit Amount")
        print("2. Withdraw Amount")
        print("3. Balance Enquiry")
        print("4. View Transaction History")
        print("5. Calculate Interest (Savings only)")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            num = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit: "))
            depositAndWithdraw(num, 1, amount)
        elif choice == '2':
            num = int(input("Enter account number: "))
            amount = float(input("Enter amount to withdraw: "))
            depositAndWithdraw(num, 2, amount)
        elif choice == '3':
            num = int(input("Enter account number: "))
            displaySp(num)
        elif choice == '4':
            num = int(input("Enter account number: "))
            viewTransactionHistory(num)
        elif choice == '5':
            num = int(input("Enter account number: "))
            calculateInterest(num)
        elif choice == '6':
            break
        else:
            print("Invalid choice!")

# Display all accounts
def displayAll():
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        for account in accounts:
            account.showAccount()
        infile.close()
    else:
        print("No records to display")

# Display specific account balance
def displaySp(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        found = False
        for account in accounts:
            if account.accNo == num:
                account.showAccount()
                found = True
        if not found:
            print("Account not found.")
    else:
        print("No records to search.")

# Deposit or withdraw money
def depositAndWithdraw(num, action, amount):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        for account in accounts:
            if account.accNo == num:
                if action == 1:
                    account.depositAmount(amount)
                elif action == 2:
                    account.withdrawAmount(amount)
                break
        else:
            print("Account not found.")
        saveAccounts(accounts)

# Save all account data
def saveAccounts(accounts):
    outfile = open('accounts.data', 'wb')
    pickle.dump(accounts, outfile)
    outfile.close()

# Modify an account's details
def modifyAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        for account in accounts:
            if account.accNo == num:
                account.name = input("Enter new account holder name: ")
                account.type = input("Enter new account type [C/S]: ")
                account.deposit = float(input("Enter new deposit amount: "))
                break
        else:
            print("Account not found.")
        saveAccounts(accounts)

# Delete an account
def deleteAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        accounts = [account for account in accounts if account.accNo != num]
        saveAccounts(accounts)

# View transaction history
def viewTransactionHistory(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        for account in accounts:
            if account.accNo == num:
                print("Transaction History:", account.transactions)
                break
        else:
            print("Account not found.")

# Calculate interest for savings account
def calculateInterest(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        accounts = pickle.load(infile)
        infile.close()
        for account in accounts:
            if account.accNo == num and account.type == 'S':
                account.calculateInterest()
                saveAccounts(accounts)
                break
        else:
            print("Account not found or not a savings account.")

# Main program
def main():
    users_db = {'admin': 'admin123', 'user1': 'userpass'}  # Simple user authentication
    username = login(users_db)
    
    if username:
        if username == 'admin':
            adminMenu()  # Admin functionalities
        else:
            userMenu(username)  # User functionalities

if __name__ == '__main__':
    main()
