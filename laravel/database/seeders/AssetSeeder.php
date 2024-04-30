<?php

namespace Database\Seeders;

use App\Models\Asset;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class AssetSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        for ($i = 1; $i <= 10; $i++) {
            Asset::create([
                'player_id' => $i,
                'symbol' => 'KRW',
                'buy_price' => 0,
                'quantity' => 10000000
            ]);
        }
    }
}
