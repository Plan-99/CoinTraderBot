<?php

namespace App\Console\Commands;

use App\Models\Candle;
use App\Models\CandleSeqLog;
use Carbon\Carbon;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class StoreCandleCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:store-candle {--to=} {--from=}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $client = new Client();
        $res = $client->request('GET', 'https://api.bithumb.com/public/ticker/ALL_KRW');
        $result = json_decode($res->getBody()->getContents());
        $symbols = collect($result->data)->keys();
        $fromRaw = $this->option('from') ?
            str_replace('T', ' ', $this->option('from')) : Carbon::now()->format('Y-m-d H:i:s');
        $from = str_replace(' ', 'T', Carbon::createFromFormat('Y-m-d H:i:s', $fromRaw)->subHours(9)->format('Y-m-d H:i:s'));
        $to = $this->option('to');
        DB::beginTransaction();
        $candleSeq = CandleSeqLog::create([
            'from' => $fromRaw,
            'to' => $to,
            'created_at' => now()
        ]);
        foreach ($symbols as $i => $symbol) {
            $lastTimestamp = $from;
            $go = true;
            $process = $i + 1;
            while ($go) {
                try {
                    $res = $client->request('GET', "https://api.upbit.com/v1/candles/minutes/1?market=KRW-{$symbol}&count=200&to={$lastTimestamp}");
                    $remainingReqStr = $res->getHeader('Remaining-Req')[0];
                    $limit = $this->strToObject($remainingReqStr);
                    if ((int) $limit['sec'] === 0 || $limit['min'] === 0) {
                        sleep(1);
                    }
                    $result = json_decode($res->getBody()->getContents());
                    foreach($result as $data) {
                        if ($to > $data->candle_date_time_kst) {
                            echo "$symbol logging completed! ($process/{$symbols->count()})\n";
                            $go = false;
                            break;
                        }
                        $idx = $symbol . Carbon::createFromFormat('Y-m-d H:i:s', str_replace('T', ' ', $data->candle_date_time_kst))->format('YmdHis');
                        Candle::firstOrCreate([
                            'idx' => $idx,
                        ], [
                            'candle_seq_log_id' => $candleSeq->id,
                            'symbol' => $symbol,
                            'timestamp' => $data->candle_date_time_kst,
                            'opening_price' => (float) $data->opening_price,
                            'high_price' => (float) $data->high_price,
                            'low_price' => (float) $data->low_price,
                            'closing_price' => (float) $data->trade_price,
                            'trade_price' => (float) $data->candle_acc_trade_price,
                        ]);
                        $lastTimestamp = $data->candle_date_time_utc;
                    }
                } catch (ClientException $e) {
                    $remainingReqStr = $e->getResponse()->getHeader('Remaining-Req')[0];
                    $limit = $this->strToObject($remainingReqStr);
                    if ((int) $limit['sec'] === 0 || $limit['min'] === 0) {
                        sleep(1);
                    }
                    if ($e->getCode() === 404) {
                        echo "Undefined symbol: {$symbol} ($process/{$symbols->count()})\n";
                    } elseif ($e->getCode() === 429) {
                        echo "Too many requests\n";
                        exit;
                    }
                    $go = false;
                }
            }
        }
        echo "$fromRaw ~ $to data has been stored!\n";
        DB::commit();
    }

    private function strToObject($str): array
    {
        $parts = explode('; ', $str);
        $result = [];
        foreach ($parts as $part) {
            list($key, $value) = explode('=', $part);
            $result[$key] = $value;
        }
        return $result;
    }
}
