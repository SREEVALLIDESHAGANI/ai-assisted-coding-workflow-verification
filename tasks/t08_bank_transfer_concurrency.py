# Task 8: Thread-Safe Bank Account Transfer
import threading

class ThreadSafeAccount:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()

def safe_transfer(from_acc: ThreadSafeAccount, to_acc: ThreadSafeAccount, amount: float) -> bool:
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    
    # Global deterministic lock ordering to prevent deadlock
    first_lock = from_acc if from_acc.account_id < to_acc.account_id else to_acc
    second_lock = to_acc if from_acc.account_id < to_acc.account_id else from_acc
    
    with first_lock.lock:
        with second_lock.lock:
            if from_acc.balance < amount:
                return False
            from_acc.balance -= amount
            to_acc.balance += amount
            return True
