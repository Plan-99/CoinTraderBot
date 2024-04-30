<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        DB::statement("CREATE VIEW total_asset AS
                            SELECT
                                assets.symbol,
                                SUM(assets.quantity) as total_quantity,
                                assets.player_id,
                                SUM(assets.buy_price * assets.quantity) as buy_amount,
                                CASE WHEN assets.symbol = 'KRW'
                                    THEN 1 * SUM(assets.quantity)
                                    ELSE (SELECT closing_price FROM candles WHERE candles.symbol = assets.symbol ORDER BY timestamp DESC LIMIT 1) * SUM(assets.quantity)
                                    END
                                as current_amount
                            FROM assets GROUP BY symbol, player_id");
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        DB::statement("DROP VIEW total_asset");
    }
};
