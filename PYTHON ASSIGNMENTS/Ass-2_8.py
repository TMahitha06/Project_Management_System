class BankAccount:
    def __init__(self, account_number, initial_balance):
        self.account_number = account_number          
        self._balance = initial_balance               
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited {amount}. New balance: {self._balance}")
        else:
            print("Deposit amount must be positive.")
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Withdrew {amount}. New balance: {self._balance}")
        else:
            print("Insufficient funds or invalid amount.")
    def get_balance(self):
        return self._balance
acc = BankAccount("12345", 1000)
print(acc.account_number)      
print(acc.get_balance())       
try:
    acc._balance = 5000        
    print("Modified _balance directly to", acc._balance)
except AttributeError:
    print("Cannot modify private attribute directly")
acc.deposit(500)
acc.withdraw(200)
