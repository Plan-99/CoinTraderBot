nohup zsh ./get_price.sh &

cd python
nohup python player1.py &
echo "Player 1 start"
nohup python player2.py &
echo "Player 2 start"
cd ../
