<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TotalAsset extends Model
{
    use HasFactory;

    protected $table = 'total_asset';

    public function scopeGroupByPlayer($query, $params) {
        return $query->selectRaw('SUM(buy_amount) as buy_amount, SUM(current_amount) as current_amount, player_id')->groupBy('player_id');
    }

    public function scopeGroupBySymbol($query, $params) {
        return $query->where('player_id', $params['player_id']);
    }
}
