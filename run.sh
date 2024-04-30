nohup $0 ./get_price.sh &

cd python
nohup python3 player1.py &
echo "Player 1 start"
nohup python3 player2.py &
echo "Player 2 start"
cd ../
