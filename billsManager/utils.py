import random
import string

def generate_virtual_account_number():
    # Generate a random 10-digit account number
    digits = string.digits
    virtual_account_number = ''.join(random.choice(digits) for _ in range(10))
    return virtual_account_number