## Change .env

There are two .env files: in laravel, in python.

## Initialize
```shell
sudo zsh ./init.sh
```

## Run
```shell
sudo nohup zsh ./get_price.sh &

cd python
nohup python3 player1.py &
mv nohup.out nohup1.out
nohup python3 player2.py &
mv nohup.out nohup2.out
cd ../
```
