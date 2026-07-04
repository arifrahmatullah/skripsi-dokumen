<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;

class RekomendasiController extends Controller
{
    public function index()
    {
        $pendaftar = Pendaftar::whereNotNull('prediksi')
            ->orderByDesc('prob_masuk')
            ->paginate(15);

        return view('rekomendasi.index', compact('pendaftar'));
    }
}
