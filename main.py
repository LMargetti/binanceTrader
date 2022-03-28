import ccxt
import bulkscraper

bulkscraper.get_crypto_history("BNBUSDT", ["2022", "02"])
import zipfile
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)