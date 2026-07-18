<?php

namespace App\Http\Controllers;

use App\Exports\TemplateImportPendaftarExport;
use App\Imports\PendaftarImport;
use App\Models\Pendaftar;
use App\Services\NaiveBayesService;
use Illuminate\Http\Request;
use Maatwebsite\Excel\Facades\Excel;

class PendaftarController extends Controller
{
    private array $rules = [
        'nama_pendaftar' => ['required', 'string', 'max:255'],
        'prodi' => ['nullable', 'string', 'max:255'],
        'asal_kota' => ['nullable', 'string', 'max:255'],
        'no_hp' => ['nullable', 'string', 'max:20'],
        'kategori_jarak_asal' => ['required', 'in:Dekat,Sedang,Jauh'],
        'kategori_asal_sekolah' => ['nullable', 'in:Sekolah Negeri,Sekolah Swasta,Sekolah Madrasah,Pondok Pesantren'],
        'waktu_pendaftaran' => ['nullable', 'in:Awal Gelombang,Tengah Gelombang,Akhir Gelombang'],
        'tingkat_follow_up_internal' => ['required', 'in:Belum Dihubungi,Kontak Awal,Follow Up,Follow Up Intensif'],
        'status_uang_pendaftaran' => ['nullable', 'in:Belum Lunas,Lunas'],
        'status_test' => ['required', 'in:Belum Tes,Sudah Tes'],
        'kategori_nilai_test' => ['required', 'in:Tidak Ada Nilai,Nilai Sedang,Nilai Tinggi'],
        'kategori_penghasilan' => ['required', 'in:Tidak Diketahui,Dibawah Rp.1.000.000,Rp.1.000.000 - Rp.2.000.000,Rp.2.000.001 - Rp.4.000.000,Rp.4.000.001 - Rp.6.000.000,Diatas Rp.6.000.000'],
        'status_retensi_final_target' => ['nullable', 'in:MASUK,TIDAK MASUK'],
    ];

    public function index(Request $request)
    {
        $pendaftar = Pendaftar::query()
            ->when($request->filled('q'), fn ($q) => $q->where('nama_pendaftar', 'like', '%'.$request->q.'%'))
            ->orderByDesc('id')
            ->paginate(15)
            ->withQueryString();

        return view('pendaftar.index', compact('pendaftar'));
    }

    public function create()
    {
        return view('pendaftar.form', ['pendaftar' => new Pendaftar()]);
    }

    public function store(Request $request, NaiveBayesService $nb)
    {
        $data = $request->validate($this->rules);
        $pendaftar = Pendaftar::create($data);
        $this->reklasifikasi($nb, $pendaftar);

        return redirect()->route('pendaftar.index')->with('status', 'Data pendaftar berhasil ditambahkan.');
    }

    public function edit(Pendaftar $pendaftar)
    {
        return view('pendaftar.form', compact('pendaftar'));
    }

    public function update(Request $request, Pendaftar $pendaftar, NaiveBayesService $nb)
    {
        $data = $request->validate($this->rules);
        $pendaftar->update($data);
        $this->reklasifikasi($nb, $pendaftar);

        return redirect()->route('pendaftar.index')->with('status', 'Data pendaftar berhasil diperbarui.');
    }

    public function import(Request $request, NaiveBayesService $nb)
    {
        $request->validate([
            'file' => ['required', 'file', 'mimes:xlsx,xls,csv,txt', 'max:5120'],
        ], [], ['file' => 'file import']);

        $import = new PendaftarImport();
        Excel::import($import, $request->file('file'));

        if ($import->jumlahBerhasil > 0) {
            $nb->classifyAll();
        }

        $pesan = $import->jumlahBerhasil.' data pendaftar berhasil diimpor dan diklasifikasi.';
        if ($import->barisGagal !== []) {
            $pesan .= ' '.count($import->barisGagal).' baris dilewati.';
        }

        return redirect()->route('pendaftar.index')
            ->with('status', $pesan)
            ->with('import_gagal', array_slice($import->barisGagal, 0, 10));
    }

    public function template()
    {
        return Excel::download(new TemplateImportPendaftarExport(), 'template-import-pendaftar.xlsx');
    }

    public function destroy(Pendaftar $pendaftar)
    {
        $pendaftar->delete();

        return redirect()->route('pendaftar.index')->with('status', 'Data pendaftar berhasil dihapus.');
    }

    private function reklasifikasi(NaiveBayesService $nb, Pendaftar $pendaftar): void
    {
        if (! $nb->statusKesiapan()['siap'] || ! $nb->fiturLengkap($pendaftar)) {
            $pendaftar->update([
                'prob_masuk' => null,
                'prob_tidak_masuk' => null,
                'prediksi' => null,
                'predicted_at' => null,
            ]);

            return;
        }

        $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();
        $model = $nb->train($labeled);
        $result = $nb->predict($model, $pendaftar);
        $pendaftar->update([
            'prob_masuk' => $result['prob_masuk'],
            'prob_tidak_masuk' => $result['prob_tidak_masuk'],
            'prediksi' => $result['prediksi'],
            'predicted_at' => now(),
        ]);
    }
}
