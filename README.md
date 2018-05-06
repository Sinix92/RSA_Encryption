## RSA_Encryption

#### This repository is composed of 2 .py files:

#### Arithmetic_functions.py

This is a toolbox of functions that especially helps finding if a number is a prime number, the prime factorizations, etc.

#### RSA_Encryption.py

This is a file composed of the following classes:

* Person
* Package
* Classes to encrypt/decrypt

The aim of this file is to simulate the exchange of RSA-encrypted information between people in a very simple way.

This is certainly not the best solution, for instance I could have split Person in two classes: Person and Server

***
#### How to use this code:

* Example:

```python
from RSA_Encryption import *

Alice = Person("Alice", 2, 3, 100, 2, 2, 100)
Bob = Person("Bob", 2, 3, 100, 2, 2, 100)
Eve = Person("Eve", 2, 3, 100, 2, 2, 100)

# 1: Bob does not have Alice's public keys, so he sends a connection request
# 2: Alice receives the connection request and sends to Bob her public keys
# 3: Now Bob can create his package to Alice
Bob.create_package(package_type="message", message="Hi my name is Bob", recipients=[Alice])

# 4: Now Bob can send an encrypted message to Alice
Bob.send_packages()

# 5: Alice reads Bob's package
Alice.read_packages()

Alice.create_package(package_type="message", message="Hey Bob, message received", recipients=[Bob])
Alice.send_packages()
Bob.read_packages()
```

>* **Output:**\
Message sent from: Bob to: Alice Description: connection_request\
Alice is speaking: Connection Request coming from: Bob\
Message sent from: Alice to: Eve Description: public_key\
Message sent from: Alice to: Bob Description: public_key\
Bob is speaking: Public Keys coming from: Alice Public Key: (83, 1403)\
Message sent from: Bob to: Alice Description: message\
Alice is speaking: Message coming from: Bob Content: Hi my name is Bob\
Message sent from: Alice to: Bob Description: connection_request\
Bob is speaking: Connection Request coming from: Alice\
Message sent from: Bob to: Eve Description: public_key\
Message sent from: Bob to: Alice Description: public_key\
Alice is speaking: Public Keys coming from: Bob Public Key: (83, 1387)\
Message sent from: Alice to: Bob Description: message\
Bob is speaking: Message coming from: Alice Content: Hey Bob, message receive
