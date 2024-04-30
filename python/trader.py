import numpy as np
from xcoin_api import XcoinApi
import pymysql
from dotenv import load_dotenv
import os


class Trader(XcoinApi):
    def __init__(self, api_key, api_secret, player_id):
        load_dotenv()
        super().__init__(api_key, api_secret)
        self.conn = pymysql.connect(host=os.getenv('DB_HOST'),
                                    user=os.getenv('DB_USER'),
                                    password=os.getenv('DB_PASSWORD'),
                                    db=os.getenv('DB_NAME'),
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.player_id = player_id
        self.my_asset = None
        self.get_my_asset()

    def get_current_price(self, symbol, type='asks'):
        res = self.publicCall(f"/assetsstatus/multichain/{symbol}")
        if res['status'] != '0000':
            return {
                'status': 'failed',
                'message': 'Undefined Symbol'
            }

        if res['data'][0]['deposit_status'] == 0 or res['data'][0]['withdrawal_status'] == 0:
            return {
                'status': 'failed',
                'message': 'Unsafe Symbol',
            }

        res = self.publicCall(f"/orderbook/{symbol}_KRW")
        if res['status'] == '0000':
            price = float(res['data'][type][0]['price'])
            quantity = float(res['data'][type][0]['quantity'])
            return {
                'status': 'succeed',
                'price': price,
                'trade_volume': price * quantity
            }
        else:
            return {
                'status': 'failed',
                'message': 'Undefined Symbol'
            }

    def get_symbols(self):
        query = f'''
            SELECT symbol FROM candles GROUP BY symbol
        '''
        self.cursor.execute(query)
        symbols = self.cursor.fetchall()
        return [symbol[0] for symbol in symbols]

    def buy(self, symbol, amount):
        res = self.get_current_price(symbol, 'asks')
        if res['status'] == 'failed':
            return res
        price = res['price']
        quantity = amount / price
        query = f'''
            SELECT quantity FROM assets WHERE player_id = {self.player_id} and symbol = 'KRW'
        '''
        self.cursor.execute(query)
        balance = self.cursor.fetchone()[0]
        if balance < amount:
            return {
                'status': 'failed',
                'message': "You don't have enough money",
            }
        query = f'''
            INSERT INTO trade_logs
            (player_id, symbol, price, quantity, type, balance, traded_at) VALUE
            ({self.player_id}, '{symbol}', {price}, {quantity}, 'buy',
                (SELECT quantity FROM assets WHERE player_id = {self.player_id} and symbol = 'KRW') - {amount},
            NOW()
            )
        '''
        self.cursor.execute(query)
        query = f'''
            UPDATE assets SET quantity = quantity - {amount} WHERE player_id = {self.player_id} and symbol = 'KRW' 
        '''
        self.cursor.execute(query)
        query = f'''
            INSERT INTO assets VALUE ({self.player_id}, '{symbol}', {price}, {quantity})
        '''
        self.cursor.execute(query)
        self.conn.commit()
        self.my_asset.append((symbol, price, quantity))
        return {
            'symbol': symbol,
            'price': price,
            'amount': amount,
            'status': 'succeed',
        }

    def sell(self, symbol, reason):
        res = self.get_current_price(symbol, 'bids')
        if res['status'] == 'failed':
            return res
        price = res['price']

        query = f'''
            SELECT SUM(quantity) FROM assets WHERE player_id = {self.player_id} and symbol = '{symbol}' GROUP BY symbol
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if not res:
            return {
                'status': 'failed',
                'message': "You don't have such symbol"
            }
        quantity = res[0]
        amount = quantity * price
        query = f'''
                   INSERT INTO trade_logs
                   (player_id, symbol, price, quantity, type, balance, traded_at, reason) VALUE
                   ({self.player_id}, '{symbol}', {price}, {quantity}, 'sell',
                       (SELECT quantity FROM assets WHERE player_id = {self.player_id} and symbol = 'KRW') + {amount * (1 - 0.0004)},
                   NOW(),
                   '{reason}'
                   )
               '''
        self.cursor.execute(query)
        query = f'''
            UPDATE assets SET quantity = quantity + {amount} WHERE player_id = {self.player_id} and symbol = 'KRW' 
        '''
        self.cursor.execute(query)
        query = f'''
            DELETE FROM assets WHERE symbol = '{symbol}'
        '''
        self.cursor.execute(query)
        self.conn.commit()
        return {
            'status': 'succeed',
            'symbol': symbol,
            'price': price,
            'amount': amount,
            'reason': reason
        }

    def decide(self, symbol):
        query = f'''
            SELECT * FROM candles WHERE symbol = '{symbol}'
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        threshold_rate = 0.005
        criterion_price = res[0][4] # opening_price
        flow_arr = []
        increasing = None
        for row in res:
            high_price = row[5]
            low_price = row[6]
            if high_price > criterion_price * (1 + threshold_rate):
                if not increasing:
                    flow_arr.append(criterion_price)
                criterion_price = high_price
                increasing = True
            elif low_price < criterion_price * (1 - threshold_rate):
                if increasing:
                    flow_arr.append(criterion_price)
                criterion_price = low_price
                increasing = False

        alert = None

        res = self.get_current_price(symbol)
        if res['status'] == 'succeed':
            current_price = res['price']
        else:
            return res

        res = self.sell_sloss(symbol, current_price)
        if res:
            return {
                'status': 'succeed',
                'alert': 'sell',
                'reason': 'sloss'
            }

        if self.player_id == 1:  # 지지선과 저항선에 의한 trading
            increasing_rate = 0.3

            criterion_price = np.mean(flow_arr) + (flow_arr[len(flow_arr) - 1] - flow_arr[0]) * increasing_rate

            trade_threshold_rate = 0.01

            buy_price = criterion_price * (1 - trade_threshold_rate)
            sell_price = criterion_price * (1 + trade_threshold_rate)

            if current_price < buy_price:
                alert = 'buy'
            elif current_price > sell_price:
                alert = 'sell'

        if self.player_id == 2:  # 상승 추이에 따른 trading
            increasing_threshold_range = [0.02, 0.1]
            increasing_slope = (flow_arr[len(flow_arr) - 1] - flow_arr[len(flow_arr) - 2]) / flow_arr[len(flow_arr) - 2]
            if increasing_threshold_range[0] < increasing_slope < increasing_threshold_range[1]:
                alert = 'buy'
            elif - increasing_threshold_range[0] > - increasing_slope > - increasing_threshold_range[1]:
                alert = 'sell'

        return {
            'status': 'succeed',
            'alert': alert,
            'reason': 'mechanism'
        }

    def get_my_asset(self):
        query = f'''
            SELECT symbol, buy_price, quantity FROM assets WHERE symbol != 'KRW' and player_id = {self.player_id}
        '''
        self.cursor.execute(query)
        assets = self.cursor.fetchall()
        self.my_asset = [asset for asset in assets]

    def sell_sloss(self, symbol, price):
        sloss = 0.05
        for asset in self.my_asset:
            if asset[0] == symbol and (asset[1] * (1 + sloss) < price or asset[1] * (1 - sloss) > price):
                return True

        return False






