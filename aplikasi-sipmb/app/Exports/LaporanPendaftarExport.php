<?php

namespace App\Exports;

use Illuminate\Support\Collection;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;

class LaporanPendaftarExport implements FromCollection, WithHeadings, WithMapping
{
    public function __construct(private Collection $pendaftar)
    {
    }

    public function collection(): Collection
    {
        return $this->pendaftar;
    }

    public function headings(): array
    {
        return [
            'No', 'Nama Pendaftar', 'Kategori Jarak Asal', 'Tingkat Follow Up',
            'Status Test', 'Kategori Nilai Test', 'Kategori Penghasilan',
            'P(MASUK|X)', 'P(TIDAK MASUK|X)', 'Prediksi', 'Rekomendasi Tindak Lanjut',
        ];
    }

    public function map($row): array
    {
        static $no = 0;
        $no++;

        return [
            $no,
            $row->nama_pendaftar,
            $row->kategori_jarak_asal,
            $row->tingkat_follow_up_internal,
            $row->status_test,
            $row->kategori_nilai_test,
            $row->kategori_penghasilan,
            $row->prob_masuk,
            $row->prob_tidak_masuk,
            $row->prediksi,
            $row->rekomendasiTindakLanjut(),
        ];
    }
}
