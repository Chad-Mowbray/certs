from caesar_cipher import encrypt
from public_key_cryptography import return_shared_secret


alices_unencrypted_message = "TheBeerRunsAtMidnight"

shared_secret = return_shared_secret()

alices_encrypted_message = encrypt(alices_unencrypted_message, shared_secret["shared_secret_alice"])
# print(alices_encrypted_message)


bob_decrypts_alices_message = encrypt(alices_encrypted_message, -shared_secret["shared_secret_bob"])
# print(bob_decrypts_alices_message)

print(f"""    Alice's original message: {alices_unencrypted_message}
    Alice's encrypted message: {alices_encrypted_message}
    Bob's decryption of Alice's encrypted message: {bob_decrypts_alices_message}""")