import os


def input_api_data(variable):
    try:
        answer = str(input(f"Enter API {variable}: "))
        if len(answer) == 64:
            var_name = 'binance_' + str(variable)
            print(var_name)
            os.environ[var_name] = answer
        else:
            raise Exception("Incorrect length")
    except:
        print("Invalid Input")
    return


input_api_data(variable="cheese")
# os.environ['binance_apisecret'] = input(Enter )
