import os
from osVariables import OSdata


def main():
    os_vars = OSdata()
    os_vars.get_vars('api_key')
    os_vars.get_vars('api_secret')
    return


if __name__ == "__main__":
    main()

