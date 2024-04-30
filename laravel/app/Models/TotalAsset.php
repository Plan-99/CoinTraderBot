<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TotalAsset extends Model
{
    use HasFactory;

    protected $table = 'total_asset';

    public function scopeGroupByPlayer($query) {
        return $query->selectRaw('SUM(buy_amount) as buy_amount, SUM(current_amount) as current_amount, player_id')->groupBy('player_id');
    }
}
