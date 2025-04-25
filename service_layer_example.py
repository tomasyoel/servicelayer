# Domain Model
class BankAccount:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient funds")
    
    def deposit(self, amount):
        self.balance += amount

# Service Layer
class TransferService:
    @staticmethod
    def transfer(source_account, target_account, amount):
        """Atomic money transfer between accounts"""
        try:
            source_account.withdraw(amount)
            target_account.deposit(amount)
            return True
        except ValueError as e:
            print(f"Transfer failed: {str(e)}")
            return False

# Repository (Simplified)
class AccountRepository:
    @staticmethod
    def find(account_id):
        # Simulate database fetch
        return BankAccount(account_id, 1000)

# Usage Example
if __name__ == "__main__":
    account_a = AccountRepository.find("ACC-123")
    account_b = AccountRepository.find("ACC-456")
    
    print(f"Initial balances: A=${account_a.balance}, B=${account_b.balance}")
    
    TransferService.transfer(account_a, account_b, 200)
    
    print(f"After transfer: A=${account_a.balance}, B=${account_b.balance}")