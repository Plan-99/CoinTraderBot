<?php

namespace App\Http\Controllers;

use App\Models\TotalAsset;
use GuzzleHttp\Client;
use Illuminate\Http\Request;

class TotalAssetController extends Controller
{
    public function index(Request $request) {
        $query = TotalAsset::query();
        $params = $request->query();
        if ($request->has('query_s')) {
            $queryS = $request->query_s;
            $query->$queryS($params);
        }
        return $query->paginate();
    }

    public function getCurrentPrice($symbol) {
        $client = new Client();
        $res = $client->request('GET', "https://api.bithumb.com/public/orderbook/{$symbol}_KRW");
        $result = json_decode($res->getBody()->getContents());
        $ask = $result->data->asks[0];
        $bid = $result->data->bids[0];
        return $ask->quantity > $bid->quantity ? $ask->pirce : $bid->price;
    }
}
