sudo nohup $1 ./get_price.sh &

cd python
nohup python3 player1.py &
echo "Player 1 start"
sudo mv nohup.out nohup1.out
nohup python3 player2.py &
echo "Player 2 start"
sudo mv nohup.out nohup2.out
cd ../
