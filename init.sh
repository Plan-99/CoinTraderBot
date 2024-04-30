cd laravel
composer install
php artisan key:generate
php artisan migrate
php artisan db:seed --class=AssetSeeder

cd ../frontend
npm install
quasar build

cd ../python
pip install -r requirements.txt

cd ../



