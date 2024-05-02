from trader import Trader
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SEC')


def trade(trader, symbol):
    decision = trader.decide(symbol)
    if decision['status'] == 'failed':
        print(decision, trader.player_id)
    elif decision['alert'] == 'buy':
        res = trader.buy(symbol, 1000000)
        if (res['status'] == 'success'):
            print(res, 'buy', trader.player_id, symbol)
    elif decision['alert'] == 'sell':
        res = trader.sell(symbol, decision['reason'])
        if (res['status'] == 'success'):
            print(res, 'sell', trader.player_id, symbol)


def main():
    trader = Trader(api_key, api_secret, 2)
    symbols = trader.get_symbols()
    for symbol in symbols:
        trade(trader, symbol)


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    main()

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
