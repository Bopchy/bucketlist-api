import string
import random


def random_username_generator():
    # Randomly generate lowercase name of 5 letters
    name_length = 4
    name_chars = string.ascii_lowercase
    name = ''.join(random.choice(name_chars) for num in range(name_length))

    digit_length = 2
    digit_chars = string.digits
    digits = ''.join(random.choice(digit_chars) for num in range(digit_length))

    username = name + digits
    return username
