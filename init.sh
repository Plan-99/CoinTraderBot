cd laravel
composer install
php artisan key:generate
php artisan migrate
php artisan db:seed --class=AssetSeeder
php artisan storage:link
chmod -R 777 storage/
chmod -R 777 public/storage/

cd ../frontend
npm install
quasar build

cd ../python
pip install -r requirements.txt

cd ../



