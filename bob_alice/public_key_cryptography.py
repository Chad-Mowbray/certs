import random

class Key:
    def __init__(self, public_key_base, public_key_modulus):
        self.public_key_base = public_key_base
        self.public_key_modulus = public_key_modulus
        self.private_key_random = random.randint(1,100) 

    def generate_private_key(self):
        return pow(self.public_key_base, self.private_key_random) % self.public_key_modulus

    def generate_shared_secret(self, another):
        return pow(another, self.private_key_random) % self.public_key_modulus


def return_shared_secret():
    public_key_base = 3  
    public_key_modulus = 23 
    
    alice_private_secret = Key(public_key_base, public_key_modulus)
    bob_private_secret = Key(public_key_base, public_key_modulus)
    shared_secret_alice = alice_private_secret.generate_shared_secret(bob_private_secret.generate_private_key())
    shared_secret_bob = bob_private_secret.generate_shared_secret(alice_private_secret.generate_private_key())

    print("*" * 40, "RESULTS", "*" * 40)
    print(f"Public key: public_key_base {public_key_base}, public_key_modulus {public_key_modulus}")
    print(f"Alice's private key: {alice_private_secret.generate_private_key()}, shared secret: {shared_secret_alice}\nBob's private key: {bob_private_secret.generate_private_key()}, shared secret: {shared_secret_bob}")

    return {
        "shared_secret_alice": shared_secret_alice,
        "shared_secret_bob": shared_secret_bob
    }
   
