from utils import UserInputMethods
from pathlib import Path
import wget
import zipfile

# file path
dataDirectory = Path.cwd() / 'cryptodata'

# default url variables
base_url = "https://data.binance.vision/data"
trade_type = "spot"


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
    file_dir = dataDirectory / file_name
    final_dir = dataDirectory / final_file
    # print(file_dir)
    if not final_dir.isfile():
        try:
            wget.download(url, file_dir)
            print(f"Download of {file_name} was successful.")

            with zipfile.ZipFile(file_dir, 'r') as zip_ref:
                zip_ref.extractall(dataDirectory)
            print(f"{file_name} has been unzipped")
            try:
                file_dir.unlink()
                print(f"{file_name} has been removed")
                print(f"Find {final_file} in {str(final_dir)}")
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
    parameters = UserInputMethods.get_user_variables()
    if parameters:
        pair = parameters[0]
        date = parameters[1]
        data_type = parameters[2]
        interval = parameters[3]
        get_crypto_history(trade_pair=pair, date=date, data_type=data_type, time_interval=interval)

    return


if __name__ == '__main__':
    main()
