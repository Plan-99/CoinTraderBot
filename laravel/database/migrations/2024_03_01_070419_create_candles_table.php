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
        Schema::create('candles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('candle_seq_log_id')->constrained();
            $table->string('symbol');
            $table->unsignedDouble('opening_price');
            $table->unsignedDouble('high_price');
            $table->unsignedDouble('low_price');
            $table->unsignedDouble('closing_price');
            $table->unsignedDouble('trade_price');
            $table->timestamp('timestamp');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('candles');
    }
};
