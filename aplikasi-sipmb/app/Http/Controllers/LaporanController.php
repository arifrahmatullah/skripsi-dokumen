<?php

namespace App\Http\Controllers;

use App\Exports\LaporanPendaftarExport;
use App\Models\Pendaftar;
use Barryvdh\DomPDF\Facade\Pdf;
use Illuminate\Http\Request;
use Maatwebsite\Excel\Facades\Excel;

class LaporanController extends Controller
{
    private function filtered(Request $request)
    {
        return Pendaftar::query()
            ->when($request->filled('dari'), fn ($q) => $q->whereDate('created_at', '>=', $request->dari))
            ->when($request->filled('sampai'), fn ($q) => $q->whereDate('created_at', '<=', $request->sampai))
            ->when($request->filled('status'), fn ($q) => $q->where('prediksi', $request->status))
            ->orderByDesc('id');
    }

    public function index(Request $request)
    {
        $pendaftar = $this->filtered($request)->paginate(15)->withQueryString();

        return view('laporan.index', compact('pendaftar'));
    }

    /**
     * dompdf sangat berat untuk tabel besar (>~300 baris bisa menghabiskan
     * ratusan MB memori), jadi PDF dibatasi jumlah barisnya. Untuk laporan
     * lengkap gunakan Export Excel.
     */
    private const MAX_BARIS_PDF = 300;

    public function exportPdf(Request $request)
    {
        ini_set('memory_limit', '512M');

        $pendaftar = $this->filtered($request)->limit(self::MAX_BARIS_PDF)->get();
        $totalTersedia = $this->filtered($request)->count();

        $pdf = Pdf::loadView('laporan.pdf', compact('pendaftar', 'totalTersedia'))->setPaper('a4', 'landscape');

        return $pdf->download('laporan-rekomendasi-tindak-lanjut.pdf');
    }

    public function exportExcel(Request $request)
    {
        $pendaftar = $this->filtered($request)->get();

        return Excel::download(new LaporanPendaftarExport($pendaftar), 'laporan-rekomendasi-tindak-lanjut.xlsx');
    }
}
