cd laravel
composer install
php artisan key:generate
php artisan migrate
php artisan db:seed --class=AssetSeeder

cd ../frontend
npm install
quasar build

cd ../
nohup ./get_price.sh &
nohup ./run.sh 0 &
nohup ./run.sh 1 &

