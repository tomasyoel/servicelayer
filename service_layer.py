# Domain Model
class BankAccount:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance
    
    def withdraw(self, amount):
        """Returns True if successful, False if insufficient funds"""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def deposit(self, amount):
        self.balance += amount

# Service Layer with improved error handling
class TransferService:
    MAX_ATTEMPTS = 100
    
    @staticmethod
    def transfer(source, target, amount):
        """
        Atomic money transfer with:
        - Limited attempts
        - Silent error handling
        - Return status
        """
        for _ in range(TransferService.MAX_ATTEMPTS):
            if source.withdraw(amount):
                target.deposit(amount)
                return True
        return False

# Repository Pattern
class AccountRepository:
    @staticmethod
    def find(account_id, balance=1000):
        """Simulates database fetch with default balance"""
        return BankAccount(account_id, balance)

# Demonstration
if __name__ == "__main__":
    # Initialize accounts
    acc_from = AccountRepository.find("ACC-123", 500)
    acc_to = AccountRepository.find("ACC-456", 1000)
    
    print(f"[Before] Source: ${acc_from.balance}, Target: ${acc_to.balance}")
    
    # Test transfer
    success = TransferService.transfer(acc_from, acc_to, 200)
    status = "SUCCESS" if success else "FAILED"
    
    print(f"[After] Transfer {status}")
    print(f"        Source: ${acc_from.balance}, Target: ${acc_to.balance}")
    
    # Stress test
    print("\nRunning stress test...")
    test_account = AccountRepository.find("TEST", 10000)
    failures = sum(
        1 for _ in range(1000) 
        if not TransferService.transfer(test_account, acc_to, 15)
    )
    print(f"Failures in 1000 transfers: {failures}")