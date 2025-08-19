"""This Script generates a Fernet Key and prints a utf-8 string of it to the standard output.

To generate a key, pass in the argument "generate_key" like

```
python3 -m embeddable_activities generate_key
```

This key may be used to set the SECRET_KEY environment variable for the web server.
If thus used, do not share the key with anyone.
"""
from sys import argv
from cryptography.fernet import Fernet
def main():
    if len(argv) != 2 or argv[1] != "generate_key":
        print(__doc__)
        exit(0)

    print(Fernet.generate_key().decode('utf-8'))
    

    

if __name__ == "__main__":
    main()