import os.path
import wget

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)
dataDirectory = os.path.join(fileDirectory, 'cryptodata')

base_url = "https://data.binance.vision/data"
time_scale = "monthly"
trade_type = "spot"


def get_crypto_history(trade_pair: str, data_type: str = "klines", time_interval: str = "5m", date: list = None):
    """
    Downloads the historical crypto data specified by the function parameters:
    > Trade Pair: Any two currencies to trade
    > Data Type: klines (Candle or bars, in Open High Low Close format),
                 aggTrades (Tick data aggregated into 10 second blaocks),
                 trades (record of all trades / tick data)
    > Time interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo
    > Date: ['YYYY','MM']
    """
    if date is None:
        date = ["2020", "01"]

    # Building the file name
    file_parameters = [time_interval, date[0], date[1]]
    file_name = str(trade_pair)
    for par in file_parameters:
        file_param_name = "-" + str(par)
        file_name += file_param_name
    file_name += ".zip"

    # Building the url
    url_parameters = [trade_type, time_scale,
                      data_type, trade_pair, time_interval]
    url = str(base_url)
    for par in url_parameters:
        url_param_dir = "/" + str(par)
        url += url_param_dir
    url_file_exten = "/" + str(file_name)
    url += url_file_exten
    # print(url)

    # Building file directory
    file_dir = os.path.join(dataDirectory, file_name)
    # print(file_dir)
    try:
        wget.download(url, file_dir)
        print(f"Download of {file_name} was successful.")
        print(f"Find {file_name} in {file_dir}")
        return
    except:
        print(f"Download unsuccessful.")


def main():
    return


# Example
# get_crypto_history(trade_pair="BNBBUSD", date=['2022', '02'])

if __name__ == '__main__':
    main()