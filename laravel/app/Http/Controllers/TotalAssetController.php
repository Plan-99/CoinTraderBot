<?php

namespace App\Http\Controllers;

use App\Models\TotalAsset;
use Illuminate\Http\Request;

class TotalAssetController extends Controller
{
    public function index(Request $request) {
        $query = TotalAsset::query();
        if ($request->has('query_s')) {
            $queryS = $request->query_s;
            $query->$queryS();
        }
        return $query->paginate();
    }
}
