from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

conn = pymysql.connect(host=os.getenv('DB_HOST'),
                       user=os.getenv('DB_USER'),
                       password=os.getenv('DB_PASSWORD'),
                       db=os.getenv('DB_NAME'),
                       charset='utf8')

cursor = conn.cursor()

query = f'''
    CREATE TABLE IF NOT EXISTS trade_logs (
      `player_id` INT UNSIGNED NOT NULL,
      `symbol` VARCHAR(45) NOT NULL,
      `price` FLOAT UNSIGNED NOT NULL,
      `quantity` FLOAT NOT NULL,
      `amount` FLOAT GENERATED ALWAYS AS (price * quantity) STORED,
      `type` ENUM('buy', 'sell') NOT NULL,
      `balance` FLOAT NOT NULL,
      `traded_at` DATETIME NOT NULL);
'''
cursor.execute(query)
query = '''
    CREATE TABLE IF NOT EXISTS assets (
      `player_id` INT UNSIGNED NOT NULL,
      `symbol` VARCHAR(45) NOT NULL,
      `buy_price` FLOAT UNSIGNED NULL,
      `quantity` FLOAT NOT NULL);
  '''
cursor.execute(query)
query = '''
    INSERT INTO assets VALUES 
      (1, 'KRW', 0, 10000000),
      (2, 'KRW', 0, 10000000),
      (3, 'KRW', 0, 10000000),
      (4, 'KRW', 0, 10000000),
      (5, 'KRW', 0, 10000000),
      (6, 'KRW', 0, 10000000),
      (7, 'KRW', 0, 10000000),
      (8, 'KRW', 0, 10000000),
      (9, 'KRW', 0, 10000000),
      (10, 'KRW', 0, 10000000);
'''
cursor.execute(query)
conn.commit()

