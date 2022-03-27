import os


class OSdata:
    @staticmethod
    def input_os_data(variable, length):
        """
        Creates an environment variable with the OS and takes user input for the value of the variable.
        The value of the variable should be {length} characters long.
        Returns the input as a string, if it is valid.
        """
        while True:
            try:
                answer = str(input(f"Enter {variable} value: "))
                if len(answer) == length:
                    return answer
                else:
                    raise Exception("Incorrect length")
            except:
                print("Invalid Input")
        return

    @staticmethod
    def get_vars(name, doPrint=True):
        var_name = str(name)
        variable = os.getenv(var_name)
        if doPrint:
            print(variable)


if __name__ == "__main__":
    os_vars = OSdata()

    # creates variable named "api key"
    os.environ['api_key'] = os_vars.input_os_data(variable="key", length=64)
    # creates variable named "api secret"
    os.environ['api_secret'] = os_vars.input_os_data(variable="secret", length=64)