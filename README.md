## Public Key Cryptography

What is the difference between HTTP and HTTPS?  
HTTPS adds some extra steps to the initial interaction between a client (browser) and a server.  The end result of all those steps is an agreement between the client and the browser to use a specific encryption mechanism.  So when you send your credit card number in a form, even if someone intercepts the message (very easy to do as we'll see), there won't be anything useful for a potential attacker to steal.

(Wireshark)

We are going to present a somewhat simplified overview.

// https://www.thesslstore.com/blog/explaining-ssl-handshake/


With HTTPS, before any application data is sent, the server sends the browser its certificate.  A certificate is basically just a filled out form that is meant to prove that the server is who it says it is.  


How does this happen?  The short answer is: certificates.

HTTPS uses encryption 

TLS handshake

(show flow diagram)


## Ceasar Cipher Example
We already know about the Ceasar Cipher.  If you want to exchange encrypted letters with someone using a Ceasar Cipher, you both need to have the same secret number.  But if you are the writer, how do you tell your reader what the secret number is?  You can't simply write in in the top corner of the letter, because anyone who intercepts the letter would be able to decode it.  There are some ways around this.  You might have a dead-drop that you both know about, where you can place the secret number.  But then how do you securely communicate about the dead-drop's location...  It seems like an infinite regression.

Fortunately, there is some math thing that solves this problem for us.  In fact, it is the basis of secure communication on the internet--the "S" in HTTPS.  

Through some kind of magic, public key cryptography allows two people to share encrypted information even when the encryptor uses a publicly available key.  It sounds strange, but here is how it goes.

Alice and Bob want to pass secret messages to each other.  Here is what they do:
Alice generates two very large numbers that are mathematically related, but impossible to guess
Alice keeps one of them to herself <b>(private key)</b>, and posts the other one publicly as her pinned Tweet<b>(public key)</b>.

Bob does the same thing.  
Bob generates two very large numbers that are mathematically related, but impossible to guess.
Bob keeps one of them to himself <b>(private key)</b>, and posts the other one publicly as his pinned Tweet <b>(public key)</b>.

When Bob wants to send a message to Alice, he encrypts his message with <i>Alice's</i> <b>(public key)</b>.  Alice then uses her <b>(private key)</b> to decrypt Bob's message.

The same thing happens when Alice wants to send a message to Bob:
When Alice wants to send a message to Bob, she encrypts her message with <i>Bob's</i> <b>(public key)</b>.  Bob then uses his <b>(private key)</b> to decrypt Alice's message.


It sounds crazy, and it involves math that I won't bother trying to figure out, but we can build a very simple model that shows how it works using very small numbers.

We'll use a Ceasar Cipher to show how Alice and Bob can send an receive encrypted messages without knowing the other's private key.  

Here is how the keys are generated:

```python
# public_key_cryptography.py
import random

class Key:
    def __init__(self, public_key_base, public_key_modulus):
        self.public_key_base = public_key_base
        self.public_key_modulus = public_key_modulus
        self.private_key = random.randint(1,100) 

    def generate_public_key(self):
        return pow(self.public_key_base, self.private_key) % self.public_key_modulus

    def generate_shared_secret(self, another):
        return pow(another, self.private_key) % self.public_key_modulus


def return_shared_secret():
    public_key_base = 3  
    public_key_modulus = 23 
    
    alice_private_secret = Key(public_key_base, public_key_modulus)
    bob_private_secret = Key(public_key_base, public_key_modulus)
    shared_secret_alice = alice_private_secret.generate_shared_secret(bob_private_secret.generate_public_key())
    shared_secret_bob = bob_private_secret.generate_shared_secret(alice_private_secret.generate_public_key())

    return {
        "shared_secret_alice": shared_secret_alice,
        "shared_secret_bob": shared_secret_bob
    }
```

Feel free to let your eyes glaze over.  The point is that, through some mathmatical wizardry, both Alice and Bob end up deciding on the same number for the Ceasar Cipher.

If we now run alice_bob_message_exchange.py, we see that an encrypted message can be sent and received, even though both parties have withheld information.

