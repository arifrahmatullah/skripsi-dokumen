<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;
use App\Services\NaiveBayesService;

class DashboardController extends Controller
{
    public function __invoke(NaiveBayesService $nb)
    {
        if (Pendaftar::whereNull('predicted_at')->exists()) {
            $nb->classifyAll();
        }

        $total = Pendaftar::count();
        $masuk = Pendaftar::where('prediksi', 'MASUK')->count();
        $tidakMasuk = Pendaftar::where('prediksi', 'TIDAK MASUK')->count();
        $evaluasi = $nb->evaluate();

        $terbaru = Pendaftar::latest('predicted_at')->limit(5)->get();

        return view('dashboard', compact('total', 'masuk', 'tidakMasuk', 'evaluasi', 'terbaru'));
    }
}
