from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os.path

# file path
absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)
dataDirectory = os.path.join(fileDirectory, 'cryptodata')
testDirectory = "C:/Users/liamm/PycharmProjects/binanceTrader/binanceTrader/cryptodata/BNBUSDT-5m-2021-09.csv"


def get_file_dir(base_dir, trade_pair, date, trade_type, time_interval="5m"):
    """
    Takes all the required parameters to find the correct file.
    @param trade_type: string
    @param base_dir: string
    @param trade_pair: string
    @param time_interval: string
    @param date: list
    @return: string
    """
    if trade_type == "klines":
        dir_vars = [time_interval]
    else:
        dir_vars = []
    for i in date:
        dir_vars.append(i)
    file_name = trade_pair
    for v in dir_vars:
        var = "-" + v
        file_name += var
    file_name += ".csv"
    file_dir = os.path.join(base_dir, file_name)
    return file_dir


def unix_to_datetime(total_ms):
    """
    Converts unix millisecond timestamp to date and time in form: %Y/%m/%d %H:%M:%S
    @param total_ms: integer
    @return: string
    """
    ts = round(total_ms / 1000)
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return date


def csv_to_pd(file_dir, data_type="klines", print_result=False):
    """
    Converts a csv file of historical data to a pandas dataframe with the correct column names
    @param file_dir: string
    @param data_type: string
    @param print_result: boolean
    @return: None
    """
    headers = []

    # headers for each data type
    if data_type == "klines":
        headers = ["Open time", "Open", "High", "Low", "Close",
                   "Volume", "Close time", "Quote asset volume", "Number of trades",
                   "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    elif data_type == "aggTrades":
        headers = ["Aggregate tradeId", "Price", "Quantity", "First tradeId",
                   "Last tradeId", "Timestamp", "Was the buyer the maker",
                   "Was the trade the best price match"]
    elif data_type == "trades":
        headers = ["trade Id", "price", "qty", "quoteQty", "time", "isBuyerMaker", "isBestMatch"]

    # creating dataframe
    df = pd.read_csv(file_dir, header=0, names=headers)

    # converting any timestamps to utc datetime and setting index
    if data_type == "klines":
        df['Open time'] = df['Open time'].apply(unix_to_datetime)
        df['Close time'] = df['Close time'].apply(unix_to_datetime)
        df.set_index(keys=['Open time'], inplace=True)

    elif data_type == "aggTrades":
        df['Timestamp'] = df['Timestamp'].apply(unix_to_datetime)
        df.set_index('Timestamp', inplace=True)

    elif data_type == "trades":
        df['time'] = df['time'].apply(unix_to_datetime)
        df.set_index('time', inplace=True)

    if print_result:
        print(df)
    return df


def clean_kline_df(df: pd.DataFrame, dropped_columns=None, extra_default=None, print_result=False):
    """
    Removes pointless columns from a dataframe to minimise on clutter and
    memory usage (not sure if that's neccesarily a problem).
    The extra default parameter just allows for any extra columns to be removed, on top of the default ones
    @param df: DataFrame
    @param dropped_columns: list or None
    @param extra_default: list or None
    @param print_result: boolean
    @return: DataFrame
    """
    if dropped_columns is None:
        dropped_columns = ["Quote asset volume", "Number of trades", "Taker buy base asset volume",
                           "Taker buy quote asset volume", "Ignore"]
        if extra_default is not None:
            for i in extra_default:
                dropped_columns.append(i)
    df = df.drop(columns=dropped_columns)
    if print_result:
        print(df)
    return df


def SMA(df: pd.DataFrame, window, apply_to_column=True, print_result=False):
    """
    Calculates the simple moving average over a given period in a dataframe,
    returns either the SMA for that point or returns the input dataframe with a SMA column
    @param apply_to_column: boolean
    @param df: DataFrame (klines only)
    @param window: int
    @param print_result: boolean
    @return: int or DataFrame
    """
    if apply_to_column:
        df['SMA'] = df['Close'].rolling(window).mean()
        if print_result:
            print(df)
        return df
    else:
        window_sample = df['Close'].head(window)
        average = window_sample.mean()
        if print_result:
            print(f"Current MA: {average}")
        return average

# Values:
# Open, High, Low, Close, Vol, open time, close time
# Indicators:
# MA, RSI (relative strength index), MACD, EMA


test_df = csv_to_pd(testDirectory)

clean_test = clean_kline_df(test_df, extra_default=["Volume"])

sma_test_df = SMA(clean_test, 30)

current_MA = SMA(clean_test, 30, apply_to_column=False)

sma_test_df.plot()

plt.show()
