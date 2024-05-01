<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('trade_logs', function (Blueprint $table) {
            $table->id();
            $table->unsignedInteger('player_id');
            $table->string('symbol');
            $table->unsignedDouble('price');
            $table->unsignedDouble('quantity');
            $table->unsignedDouble('amount')->storedAs('price * quantity');
            $table->enum('type', ['sell', 'buy']);
            $table->unsignedDouble('balance');
            $table->timestamp('traded_at');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('trade_logs');
    }
};
