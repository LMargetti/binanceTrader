import os.path
import wget
import math
import zipfile

# file path
absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)
dataDirectory = os.path.join(fileDirectory, 'cryptodata')

# default url variables
base_url = "https://data.binance.vision/data"
trade_type = "spot"


def get_user_variables():
    """
    Takes user input to assign values for all the required options.
    A valid output will be of form: [currency_pair, date, data_type, time_interval]
    @return: list or boolean
    """

    currency_pair = input("Enter trade pair: ").upper()
    variables = [currency_pair]

    year = get_scale_value('year', 4)
    month = get_scale_value('month', 2)
    ans = input("Do you want to input the day value? (Y/N) ").upper()
    if ans == "Y":
        day = get_scale_value('day', 2)
        date = [year, month, day]
    else:
        date = [year, month]
    variables.append(date)

    extra = input("Do you want to input values for data_type or time_interval? (Y/N) ").upper()
    if extra == "Y":
        try:
            trade_data = input("Enter data type [klines, aggTrades or trades]: ")
            type_options = ['klines', 'aggTrades', 'trades']
            if trade_data not in type_options:
                raise Exception(f"{trade_data} option not found.")
            else:
                variables.append(trade_data)
        except:
            print("Invalid input.")
        try:
            interval_input = input("Enter time interval: ")
            interval_options = ['1m', '3m', '5m', '15m', '30m', '1h', '2h',
                                '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1mo']
            if interval_input not in interval_options:
                raise Exception(f"{interval_input} option not found.")
            else:
                variables.append(interval_input)
        except:
            print("Invalid input.")
    else:
        trade_data = "klines"
        variables.append(trade_data)
        interval = "5m"
        variables.append(interval)

    print("Variables chosen:")
    for var in variables:
        print(var)
    try:
        check = input("Is this correct? (Y/N) ").upper()
        if check == "N":
            return False
        elif check == "Y":
            return variables
    except:
        print("Invalid answer")


def get_scale_value(scale, digits):
    """
    Takes the time scale required (year, month, day) and checks if it is an integer and 'digits' long.
    @param scale: string
    @param digits: int
    @return: int
    """
    try:
        scale_input = int(input(f"Enter the {scale} you want: "))
        input_digits = int(math.log10(scale_input)) + 1
        if not isinstance(scale_input, int) or (input_digits != digits):
            raise TypeError
        else:
            return scale_input
    except:
        print("Incorrect format")


def get_crypto_history(trade_pair: str, date: list, data_type: str = "klines", time_interval: str = "5m"):
    """
    Downloads the historical crypto data specified by the function parameters:
    > Trade Pair: Any two currencies to trade
    > Data Type: klines (Candle or bars, in Open High Low Close format),
                 aggTrades (Tick data aggregated into 10 second blaocks),
                 trades (record of all trades / tick data)
    > Time interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo
    > Date: ['YYYY','MM'] for monthly or ['YYYY', 'MM', 'DD'] for daily
    """

    if len(date) == 2:
        time_scale = "monthly"
    else:
        time_scale = "daily"

    # Building the file name #
    # Parameters
    file_parameters = [time_interval]
    for scale in date:
        file_parameters.append(scale)

    # File name
    file_name = str(trade_pair)
    for par in file_parameters:
        file_param_name = "-" + str(par)
        file_name += file_param_name
    file_name += ".zip"

    # Building the url #
    url_parameters = [trade_type, time_scale,
                      data_type, trade_pair, time_interval]
    url = str(base_url)
    for par in url_parameters:
        url_param_dir = "/" + str(par)
        url += url_param_dir
    url_file_exten = "/" + str(file_name)
    url += url_file_exten
    # print(url)

    # Building file directory #
    file_dir = os.path.join(dataDirectory, file_name)
    # print(file_dir)
    try:
        wget.download(url, file_dir)
        print(f"Download of {file_name} was successful.")
        print(f"Find {file_name} in {file_dir}")
        # return
    except:
        print(f"Download unsuccessful.")

    with zipfile.ZipFile(file_dir, 'r') as zip_ref:
        zip_ref.extractall(dataDirectory)


def main():
    parameters = get_user_variables()
    if parameters:
        pair = parameters[0]
        date = parameters[1]
        data_type = parameters[2]
        interval = parameters[3]
        get_crypto_history(trade_pair=pair, date=date, data_type=data_type, time_interval=interval)

    return


if __name__ == '__main__':
    main()
