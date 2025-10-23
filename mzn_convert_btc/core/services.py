import requests
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent
load_dotenv(ROOT_DIR / '.env')

EXCHANGE_API = os.getenv('EXCHANGE_API')
COINGECKO_API = os.getenv('COINGECKO_API')

class ExchangeService:

    @staticmethod
    def get_usd_per_mzn():
       
        try:
            resp = requests.get(EXCHANGE_API)
            resp.raise_for_status()
            data = resp.json()

            usd_to_mzn = data['rates']['USD']

            mzn_to_usd = 1 / usd_to_mzn
            return round(mzn_to_usd, 4)  
        except Exception as e:
            print("Erro ao buscar taxa de câmbio:", e)
            return None

    @staticmethod
    def convert_mzn_to_usd(mzn_amount):

        try:
            resp = requests.get(EXCHANGE_API)
            resp.raise_for_status()
            data = resp.json()
            usd_rate = data['rates']['USD']  # já é MZN → USD
            return round(mzn_amount * usd_rate, 2)
        except Exception as e:
            print("Erro ao buscar taxa de câmbio:", e)
            return None
        
    @staticmethod
    def convert_usd_to_btc(usd_amount):
        try:
            url = f'{COINGECKO_API}'
            params = {"ids": "bitcoin", "vs_currencies": "usd"}
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            btc_price_usd = data['bitcoin']['usd']
            btc_amount = usd_amount / btc_price_usd
            return round(btc_amount, 8)
        except Exception as e:
            print("Erro ao buscar preço do Bitcoin:", e)
            return None
        

if __name__ == "__main__":
    try:
        valor_mzn = float(input("Digite o valor em MZN: "))
        usd = ExchangeService.convert_mzn_to_usd(valor_mzn)
        btc = ExchangeService.convert_usd_to_btc(usd)
        if usd is not None:
            print(f"{valor_mzn} MZN = {usd} USD = {btc} BTC")
        else:
            print("Não foi possível calcular a conversão.")
    except ValueError:
        print("Digite um número válido")
