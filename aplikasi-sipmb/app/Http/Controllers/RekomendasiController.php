<?php

namespace App\Http\Controllers;

use App\Models\Pendaftar;
use Illuminate\Http\Request;

class RekomendasiController extends Controller
{
    public function index(Request $request)
    {
        $pendaftar = Pendaftar::whereNotNull('prediksi')
            ->when($request->filled('q'), fn ($q) => $q->where('nama_pendaftar', 'like', '%'.$request->q.'%'))
            ->when($request->filled('prediksi'), fn ($q) => $q->where('prediksi', $request->prediksi))
            ->orderByDesc('prob_masuk')
            ->paginate(15)
            ->withQueryString();

        return view('rekomendasi.index', compact('pendaftar'));
    }

    public function simpanCatatan(Request $request, Pendaftar $pendaftar)
    {
        $data = $request->validate([
            'catatan_tindak_lanjut' => ['required', 'string', 'max:1000'],
        ], [], ['catatan_tindak_lanjut' => 'catatan']);

        $pendaftar->update([
            'catatan_tindak_lanjut' => $data['catatan_tindak_lanjut'],
            'tindak_lanjut_pada' => now(),
        ]);

        return back()->with('status', 'Catatan tindak lanjut untuk '.$pendaftar->nama_pendaftar.' berhasil disimpan.');
    }
}
