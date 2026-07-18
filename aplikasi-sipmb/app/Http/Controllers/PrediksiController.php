<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;
use App\Services\NaiveBayesService;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;

class PrediksiController extends Controller
{
    public function index(NaiveBayesService $nb)
    {
        return view('prediksi.index', [
            'kesiapan' => $nb->statusKesiapan(),
            'hasil' => null,
            'input' => [],
        ]);
    }

    public function prediksi(Request $request, NaiveBayesService $nb)
    {
        $rules = [];
        foreach (Pendaftar::FITUR as $f) {
            $rules[$f] = ['required', Rule::in(NaiveBayesService::NILAI_ATRIBUT[$f])];
        }
        $input = $request->validate($rules);

        $kesiapan = $nb->statusKesiapan();
        if (! $kesiapan['siap']) {
            return redirect()->route('prediksi.index')
                ->with('status', 'Prediksi tidak dapat dijalankan: '.$kesiapan['alasan']);
        }

        $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();
        $model = $nb->train($labeled);

        // Simulasi: data tidak disimpan ke database
        $calon = new Pendaftar($input);
        $hasil = $nb->predict($model, $calon);

        $total = $hasil['prob_masuk'] + $hasil['prob_tidak_masuk'];
        $hasil['persen_masuk'] = $total > 0 ? round($hasil['prob_masuk'] / $total * 100, 2) : null;
        $hasil['n_train'] = $model['n_train'];

        return view('prediksi.index', compact('kesiapan', 'hasil', 'input'));
    }
}
