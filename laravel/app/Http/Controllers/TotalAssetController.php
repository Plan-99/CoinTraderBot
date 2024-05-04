<?php

namespace App\Http\Controllers;

use App\Models\Asset;
use App\Models\TotalAsset;
use GuzzleHttp\Client;
use Illuminate\Http\Request;

class TotalAssetController extends Controller
{
    public function index(Request $request) {
        $query = TotalAsset::query();
        $params = $request->query();
        $queryS = $request->query_s;

        return $this->$queryS($params);
    }

    public function groupBySymbol($params) {
        $player_id = $params['player_id'];
        $assets = Asset::where('player_id', $player_id)->get();
        $symbols = [];

        foreach ($assets->groupBy('symbol') as $symbol_code => $assetList) {
            $symbol = [
                'symbol' => $symbol_code,
                'buy_amount' => 0,
                'current_amount' => 0,
            ];
            foreach ($assetList as $asset) {
                $currentPrice = $asset['symbol'] === 'KRW' ? 1 : $this->getCurrentPrice($asset['symbol']);
                $symbol['buy_amount'] += $asset['buy_price'] * $asset['quantity'];
                $symbol['current_amount'] += $currentPrice * $asset['quantity'];
                $symbol['current_price'] = $currentPrice;
            }
            $symbols[] = $symbol;
        }

        return ['data' => $symbols];
    }

    public function groupByPlayer($player_id) {
        $assets = Asset::all();
        $players = [];

        foreach ($assets->groupBy('player_id') as $player_id => $assetList) {
            $player = [
                'player_id' => $player_id,
                'buy_amount' => 0,
                'current_amount' => 0,
            ];
            foreach ($assetList as $asset) {
                $currentPrice = $asset['symbol'] === 'KRW' ? 1 : $this->getCurrentPrice($asset['symbol']);
                $player['buy_amount'] += $asset['buy_price'] * $asset['quantity'];
                $player['current_amount'] += $currentPrice * $asset['quantity'];
            }
            $players[] = $player;
        }

        return ['data' => $players];
    }

    public function getCurrentPrice($symbol) {
        $client = new Client();
        $res = $client->request('GET', "https://api.bithumb.com/public/orderbook/{$symbol}_KRW");
        $result = json_decode($res->getBody()->getContents());
        $ask = $result->data->asks[0];
        $bid = $result->data->bids[0];
        return $ask->quantity > $bid->quantity ? (int) $ask->price : (int) $bid->price;
    }
}
