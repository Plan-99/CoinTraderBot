sudo nohup $1 ./get_price.sh &

cd /var/www/CoinTraderBot/python
nohup python3 player1.py &
echo "Player 1 start"
cd ~
sudo mv nohup.out nohup1.out
cd /var/www/CoinTraderBot/python
nohup python3 player2.py &
echo "Player 2 start"
cd ~
sudo mv nohup.out nohup2.out
cd ../
