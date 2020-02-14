title: Venture Into Cryptography with PyCryptodome!
date: 2020-02-14 07:00
category: Cryptography
slug: pycryptodome
author: Martin Uribe
summary: learning about how to encrypt files

# Into the cryptography rabbit hole!

As dumb as it is, I have an unsecure text file that I use to keep track of all my username and passwords for all of the sites that I frequent. In order to not be so "hackable", I've decided to encrypt the file.

I had recently written a couple of coding challenges for [Pybites Code Challenges](https://codechalleng.es/) site, using the [cryptography](https://cryptography.io/en/latest/) module. One was a coding challenge and the other a testing one. Unfortunately, that module is **NOT** part of Python's Standard Library!

I didn't specifically install it, but it seems to come pre-installed with [Anaconda](https://www.anaconda.com/distribution/), which I use. I was looking through all of the modules that I had, when I came across the cryptography one. That's when I first got the idea for the challenges. It started as a single challenge, but I really liked how the tests came out and decided to split it up into coding and testing bites.

I pushed them to the Pybites Github private repo and it sat there for a bit before [Bob Belderbos](https://codechalleng.es/profiles/pybob) decided to add them. Tha's when the problems started! He discovered that the module was not available so he installed it. It worked perfectly for the coding challenge, but for the testing one, when the call to the [Pytest](https://docs.pytest.org/en/latest/)/[Mutpy](https://github.com/mutpy/mutpy) instance is made, it loosed the path to the module!

We were discussing the issue on the [Pybites](https://pybit.es/pages/community.html) Slack channel when [Mike Driscoll](https://codechalleng.es/profiles/driscollis) the creator of [The Mouse vs Python](http://www.blog.pythonlibrary.org/), mentioned the [PyCryptodome](https://www.pycryptodome.org/en/latest/) module. He initially thought that the problem was with installing the cryptography module. In the end, Bob was not able to figure out how to get it to work, so the challenge had to be removed from the platform.

Regardless, I was intrigued by pycryptodome, so I started to look into how it worked. It seemed pretty cool, so that's when I came up with the idea of encrypting my password file. It took a little bit of work, but I was able to encrypt the file into a binary. The problem came when I started to try and retrieve the data. The module complained about the data being too large!

I decided to create an encrypted binary for each entry. So far that's worked, but now I have to figure out how to scan the directory and list the ones that are available in order to be able to retrieve/update them. I've been using the logging module as well, so now I have to figure out how to do some log rotation to keep from taking up too much drive space. I might even play around with creating a UI for it, to make it easier to use.

Since I used my [toepack](https://github.com/clamytoe/toepack) [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template, it's a package. It's gotten big enough that I've moved the two classes, (`Entry`, `Vault`) into their own files. It works out pretty good because the `app.py` file now only contains:

```python
from .entry import Entry
from .vault import Vault, logger


def main():
    logger.debug("Entering main.")
    ip = Entry("ip", "http://192.168.2.1", "admin", "admin")

    v = Vault()
    v.encrypt_file(ip)
    v.decrypt_file(ip.name)


if __name__ == "__main__":
    logger.debug("Running as a module.")
    main()
```

Seperating the code like this will come in handy when it comes to either creating a [Click](https://palletsprojects.com/p/click/) CLI interface or a GUI one.

The results of encrypting that `Entity` object looks like this:

```
3�#4����!�0/
N9"L�,رT�o8a�����cH�.
O���}�wV&�*um��S�MO�7�`Ӂ�xZ� �BD�n�z@f�ue�x�ڒ����c՞������2��{MW�5����{��j������36	���r	~
                         |��Bzu�5��!a7܄o7h1���qkE�N�
�&�T�*puM:��U x">��ت4%��                           �H�����Y6><Q
����99���献W���'��uZ%$������%$�x��ef`�˲D��i�3���0������:
�W<���[�����^�ΐ�DGACqI�ސ���7��ŵ�|D��P�_%�9�lI�֐���u�����_ �"��!���P���5�Pw�M4�
�L��P�[��՜t9��|r� ������D��Uh��w��ۆ�kH]L�~��D���ˤ�󗣰Ӧ��
~xh�lA�d��٧�e܎�                                           �S
                  �͚��m�Q��>����{�	+�{'?A-��s��)�^ݞR%  
```

The log file for that run looks like this:

```
2020-02-13 14:05:17,812 - [INFO] - root - Creating vault: /home/mohh/Documents/.passlock/ip.bin
2020-02-13 14:05:17,812 - [INFO] - root - Importing public key: plock.pub
2020-02-13 14:05:17,812 - [INFO] - root - Public key accessed: /home/mohh/.passlock/plock.pub
2020-02-13 14:05:17,815 - [INFO] - root - Generating random byte for session key
2020-02-13 14:05:17,815 - [INFO] - root - Generating encrypted session key
2020-02-13 14:05:17,819 - [INFO] - root - Generating AES cipher
2020-02-13 14:05:17,820 - [INFO] - root - Encrypting data to create cipher text
2020-02-13 14:05:17,820 - [INFO] - root - Writing cipher text to: ip.bin
2020-02-13 14:05:17,820 - [WARNING] - root - /home/mohh/Documents/.passlock/ip.bin already exists!
2020-02-13 14:05:17,820 - [INFO] - root - Successfully wrote to: /home/mohh/Documents/.passlock/ip.bin
2020-02-13 14:05:17,821 - [INFO] - root - Opening file for reading: /home/mohh/Documents/.passlock/ip.bin
2020-02-13 14:05:17,821 - [INFO] - root - Importing private key: plock
2020-02-13 14:05:17,821 - [INFO] - root - Private key accessed: /home/mohh/.passlock/plock
2020-02-13 14:05:18,150 - [INFO] - root - Extracting encrypted session key
2020-02-13 14:05:18,151 - [INFO] - root - Generating RSA cipher key from imported private key
2020-02-13 14:05:18,151 - [INFO] - root - Decrypting extracted session key
2020-02-13 14:05:18,171 - [INFO] - root - Session key was successfully restored
2020-02-13 14:05:18,171 - [INFO] - root - Generating AES cipher from session key
2020-02-13 14:05:18,172 - [INFO] - root - Decrypting and verifying cipher text
2020-02-13 14:05:18,172 - [INFO] - root - Closing: ip.bin
2020-02-13 14:05:18,172 - [INFO] - root - Generating new Entry object from decrypted data
2020-02-13 14:05:18,172 - [INFO] - root - Returning decrypted text for: ip
```

Not sure if that's too much information but logging each step in the process really comes in handy when trying to figure out issues at work. I've tried to keep all sensitive data out of it unless the logging is switched to `debug`.

Retrieving the encrypted data looks like this:

```
Successfully created: /home/mohh/Documents/.passlock/ip.bin

[ip]
INFO: http://192.168.2.1
USER: admin
PASS: admin
```

> **NOTE**: This are not real username and passwords!
