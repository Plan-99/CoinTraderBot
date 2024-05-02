while :
do
  cd laravel
  php artisan app:store-candle-live --log
  cd ../
  cd python
  python3 player1.py
  echo "Player 1 trade end"
  python3 player2.py
  echo "Player 2 trade end"
  cd ../
done
