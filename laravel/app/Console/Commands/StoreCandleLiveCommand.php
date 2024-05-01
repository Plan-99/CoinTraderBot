<?php

namespace App\Console\Commands;

use App\Models\Candle;
use App\Models\CandleSeqLog;
use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class StoreCandleLiveCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:store-candle-live {--log}';

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
        while (true) {
            $candleSeq = CandleSeqLog::latest()->first();
            $toRaw = $candleSeq ? $candleSeq->from : Carbon::now()->subDay()->format('Y-m-d H:i:s');
            $to = str_replace(' ', 'T', $toRaw);
            $logOption = $this->option('log') ? '--log' : '';
            Artisan::call("app:store-candle --to={$to} {$logOption}");
            Candle::where('timestamp', '<', Carbon::now()->subDays(2))->delete();
        }
    }
}
