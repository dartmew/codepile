import os
from utils.helpers import greet

def main():
    name = os.getenv("USER", "World")
    print(greet(name))

if __name__ == "__main__":
    main()