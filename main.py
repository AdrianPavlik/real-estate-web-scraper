import os
from dotenv import load_dotenv

keys = None

def __init__():
    global keys
    keys = load_dotenv("./keys.env")

def __main__():
    __init__()
    print(os.environ.get("TEST"))

__main__()