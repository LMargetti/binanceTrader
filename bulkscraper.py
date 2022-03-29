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


# USER INPUTS #
# Realistically useless functions, but it was good practice.
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


# CRYPTO HISTORY SCRAPERS #
# Actually useful functions
def get_crypto_history(trade_pair: str, date: list, data_type: str = "klines", time_interval: str = "5m"):
    """
    Downloads the historical crypto data specified by the function parameters:
    > Trade Pair: Any two currencies to trade
    > Data Type: klines (Candle or bars, in Open High Low Close format),
                 aggTrades (Tick data aggregated into 10 second blaocks),
                 trades (record of all trades / tick data)
    > Time interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo
    > Date: ['YYYY','MM'] for monthly or ['YYYY', 'MM', 'DD'] for daily
    If the data type is aggTrades or trades, then only daily time scales are allowed,
    since these data types take up too much storage per file.
    @return: os.path object
    """
    if data_type == "klines":  # klines are much nicer (at least for 5m intervals) with ~1.2 MB per monthly file
        if len(date) == 2:
            time_scale = "monthly"
        else:
            time_scale = "daily"
    else:  # aggTrades and trades contain too much data per month (538 MB for one file!)
        if len(date) == 2:
            date.append("01")
        time_scale = "daily"

    # Parameters
    if data_type == "klines":
        file_parameters = [time_interval]
        url_parameters = [trade_type, time_scale,
                          data_type, trade_pair, time_interval]
    else:
        file_parameters = [data_type]
        url_parameters = [trade_type, time_scale,
                          data_type, trade_pair]

    # Building the file name #
    for scale in date:
        file_parameters.append(scale)

    # File name
    file_name = str(trade_pair)
    for par in file_parameters:
        file_param_name = "-" + str(par)
        file_name += file_param_name
    final_file = file_name + ".csv"
    file_name += ".zip"

    # Building the url #
    url = str(base_url)
    for par in url_parameters:
        url_param_dir = "/" + str(par)
        url += url_param_dir
    url_file_exten = "/" + str(file_name)
    url += url_file_exten
    # print(url)

    # Building file directory #
    file_dir = os.path.join(dataDirectory, file_name)
    final_dir = os.path.join(dataDirectory, final_file)  # just to return
    # print(file_dir)
    file_doesnt_exist = not os.path.exists(final_dir)
    if file_doesnt_exist:
        try:
            wget.download(url, file_dir)
            print(f"Download of {file_name} was successful.")
            # print(f"Find {file_name} in {file_dir}")

            with zipfile.ZipFile(file_dir, 'r') as zip_ref:
                zip_ref.extractall(dataDirectory)
            print(f"{file_name} has been unzipped")
            try:
                os.remove(file_dir)
                print(f"{file_name} has been removed")
                print(f"Find {final_file} in {final_dir}")
            except:
                print(f"{file_name} could not be deleted")
            # return
        except:
            print(f"Download unsuccessful.")
    else:
        print(f"{final_file} already exists.")
    return final_dir


def get_yearly_history(trade_pair: str, year: str, data_type: str = "klines", time_interval: str = "5m"):
    for i in range(12):
        if i < 9:
            month = "0" + f"{i + 1}"
        else:
            month = f"{i + 1}"
        try:
            get_crypto_history(trade_pair, [year, month], data_type, time_interval)
        except:
            print(f"Data for month {month} was not able to be collected.")


# MAIN #
# Nothing really exciting here...
def main():
    parameters = get_user_variables()
    if parameters:
        pair = parameters[0]
        date = parameters[1]
        data_type = parameters[2]
        interval = parameters[3]
        get_crypto_history(trade_pair=pair, date=date, data_type=data_type, time_interval=interval)

    return


# .csv file headers
# --- aggTrades:
# 1)Aggregate   2)tradeId	 3)Price	4)Quantity
# 5)First tradeId   6)Last tradeId  7)Timestamp  8)Was the buyer the maker
# 9)Was the trade the best price match
# --- klines:
# 1)Open time   2)Open  3)High	4)Low	5)Close
# 6)Volume	7)Close time    8)Quote asset volume	9)Number of trades
# 10)Taker buy base asset volume    11) Taker buy quote asset volume	12)Ignore
# --- trades:
# 1)trade Id	2)price    3)qty	4)quoteQty    5)time    6)isBuyerMaker    7)isBestMatch


if __name__ == '__main__':
    main()
