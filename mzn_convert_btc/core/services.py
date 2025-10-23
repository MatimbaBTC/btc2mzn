import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis de ambiente
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent
load_dotenv(ROOT_DIR / '.env')

EXCHANGE_API = os.getenv('EXCHANGE_API')


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

        rate = ExchangeService.get_usd_per_mzn()

        if rate is None:
            return None
        return round(mzn_amount * rate, 2)
    


if __name__ == "__main__":
    try:
        valor_mzn = float(input("Digite o valor em MZN: "))
        usd = ExchangeService.convert_mzn_to_usd(valor_mzn)
        if usd is not None:
            print(f"{valor_mzn} MZN = {usd} USD")
        else:
            print("Não foi possível calcular a conversão.")
    except ValueError:
        print("Digite um número válido")
