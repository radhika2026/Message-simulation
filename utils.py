import random
import string

def generate_random_message(length=100):
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return message


def generate_random_phone_number():
    # Generate area code
    area_code = "{}{}{}".format(random.randint(2, 9), random.randint(0, 9), random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8]))
    # Generate exchange code
    exchange_code = "{}{}{}".format(random.randint(2, 9), random.randint(0, 9), random.randint(0, 9))
    # Generate subscriber number
    subscriber_number = "{}{}{}{}".format(random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    # Combine to create phone number
    phone_number = "({}) {}-{}".format(area_code, exchange_code, subscriber_number)
    
    return phone_number

