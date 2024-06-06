
import os
import random
import string
import subprocess
from datetime import datetime, timedelta

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    print("Random String:", generate_random_string())
    print("Current Time:", get_current_time())
