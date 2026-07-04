<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;
use App\Services\NaiveBayesService;

class KlasifikasiController extends Controller
{
    public function index(NaiveBayesService $nb)
    {
        $pendaftar = Pendaftar::orderByDesc('prob_masuk')->paginate(15);
        $evaluasi = $nb->evaluate();

        return view('klasifikasi.index', compact('pendaftar', 'evaluasi'));
    }

    public function show(Pendaftar $pendaftar, NaiveBayesService $nb)
    {
        $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();
        $model = $nb->train($labeled);
        $result = $nb->predict($model, $pendaftar);

        return view('klasifikasi.show', compact('pendaftar', 'result'));
    }

    public function prosesUlang(NaiveBayesService $nb)
    {
        $nb->classifyAll();

        return back()->with('status', 'Klasifikasi seluruh data pendaftar berhasil diproses ulang.');
    }
}
