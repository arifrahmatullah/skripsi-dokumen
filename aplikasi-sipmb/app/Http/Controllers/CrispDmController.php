<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;
use App\Services\NaiveBayesService;
use Illuminate\Support\Facades\DB;

class CrispDmController extends Controller
{
    public function index(NaiveBayesService $nb)
    {
        $kesiapan = $nb->statusKesiapan();

        $total = Pendaftar::count();
        $terklasifikasi = Pendaftar::whereNotNull('prediksi')->count();
        $prediksiMasuk = Pendaftar::where('prediksi', 'MASUK')->count();
        $sudahDitindaklanjuti = Pendaftar::whereNotNull('tindak_lanjut_pada')->count();

        $distribusiFitur = [];
        foreach (Pendaftar::FITUR as $f) {
            $counts = Pendaftar::select($f, DB::raw('count(*) as jml'))
                ->whereNotNull($f)
                ->groupBy($f)
                ->pluck('jml', $f);
            // urutkan mengikuti urutan kategori yang didefinisikan model
            $distribusiFitur[$f] = collect(NaiveBayesService::NILAI_ATRIBUT[$f])
                ->mapWithKeys(fn ($v) => [$v => $counts[$v] ?? 0]);
        }

        $model = null;
        $evaluasi = null;
        if ($kesiapan['siap']) {
            $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();
            $model = $nb->train($labeled);
            $evaluasi = $nb->evaluate();
        }

        return view('crispdm.index', compact(
            'kesiapan', 'total', 'terklasifikasi', 'prediksiMasuk',
            'sudahDitindaklanjuti', 'distribusiFitur', 'model', 'evaluasi'
        ));
    }
}
