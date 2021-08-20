"""
This module will be used to generate passwords
"""

import string
from random import *


def password_gen():
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(characters) for _ in range(randint(8, 16)))
    return password