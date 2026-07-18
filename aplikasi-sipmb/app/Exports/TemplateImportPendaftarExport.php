<?php

namespace App\Exports;

use Maatwebsite\Excel\Concerns\FromArray;
use Maatwebsite\Excel\Concerns\WithHeadings;

class TemplateImportPendaftarExport implements FromArray, WithHeadings
{
    public function headings(): array
    {
        return [
            'Nama Pendaftar', 'Prodi', 'Asal Kota', 'No HP', 'Kategori Jarak Asal',
            'Kategori Asal Sekolah', 'Waktu Pendaftaran', 'Tingkat Follow Up Internal',
            'Status Uang Pendaftaran', 'Status Test', 'Kategori Nilai Test',
            'Kategori Penghasilan', 'Status Retensi Final Target',
        ];
    }

    public function array(): array
    {
        return [
            [
                'Contoh Pendaftar A', 'Manajemen Bisnis Syariah', 'Bogor', '081234567890', 'Dekat',
                'Sekolah Negeri', 'Awal Gelombang', 'Follow Up Intensif',
                'Lunas', 'Sudah Tes', 'Nilai Tinggi',
                'Rp.2.000.001 - Rp.4.000.000', 'MASUK',
            ],
            [
                'Contoh Pendaftar B', 'Akuntansi Syariah', 'Medan', '', 'Jauh',
                'Pondok Pesantren', 'Akhir Gelombang', 'Belum Dihubungi',
                'Belum Lunas', 'Belum Tes', 'Tidak Ada Nilai',
                'Tidak Diketahui', '',
            ],
        ];
    }
}
