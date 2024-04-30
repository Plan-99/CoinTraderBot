sudo nohup $1 ./get_price.sh &

cd python
sudo nohup python3 player1.py &
echo "Player 1 start"
sudo nohup python3 player2.py &
echo "Player 2 start"
cd ../
