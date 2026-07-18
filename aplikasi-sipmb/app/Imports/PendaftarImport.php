<?php

namespace App\Imports;

use App\Models\Pendaftar;
use Illuminate\Support\Collection;
use Maatwebsite\Excel\Concerns\SkipsEmptyRows;
use Maatwebsite\Excel\Concerns\ToCollection;
use Maatwebsite\Excel\Concerns\WithHeadingRow;

class PendaftarImport implements ToCollection, WithHeadingRow, SkipsEmptyRows
{
    public int $jumlahBerhasil = 0;

    /** @var string[] pesan kegagalan per baris yang dilewati */
    public array $barisGagal = [];

    private const KOLOM_WAJIB = [
        'nama_pendaftar',
        'kategori_jarak_asal',
        'tingkat_follow_up_internal',
        'status_test',
        'kategori_nilai_test',
        'kategori_penghasilan',
    ];

    private const NILAI_VALID = [
        'kategori_jarak_asal' => ['Dekat', 'Sedang', 'Jauh'],
        'kategori_asal_sekolah' => ['Sekolah Negeri', 'Sekolah Swasta', 'Sekolah Madrasah', 'Pondok Pesantren'],
        'waktu_pendaftaran' => ['Awal Gelombang', 'Tengah Gelombang', 'Akhir Gelombang'],
        'tingkat_follow_up_internal' => ['Belum Dihubungi', 'Kontak Awal', 'Follow Up', 'Follow Up Intensif'],
        'status_uang_pendaftaran' => ['Belum Lunas', 'Lunas'],
        'status_test' => ['Belum Tes', 'Sudah Tes'],
        'kategori_nilai_test' => ['Tidak Ada Nilai', 'Nilai Sedang', 'Nilai Tinggi'],
        'kategori_penghasilan' => [
            'Tidak Diketahui', 'Dibawah Rp.1.000.000', 'Rp.1.000.000 - Rp.2.000.000',
            'Rp.2.000.001 - Rp.4.000.000', 'Rp.4.000.001 - Rp.6.000.000', 'Diatas Rp.6.000.000',
        ],
        'status_retensi_final_target' => ['MASUK', 'TIDAK MASUK'],
    ];

    public function collection(Collection $rows): void
    {
        foreach ($rows as $i => $row) {
            $noBaris = $i + 2; // baris 1 pada file = judul kolom
            $gagal = [];

            $data = [
                'nama_pendaftar' => trim((string) ($row['nama_pendaftar'] ?? '')),
                'prodi' => trim((string) ($row['prodi'] ?? '')) ?: null,
                'asal_kota' => trim((string) ($row['asal_kota'] ?? '')) ?: null,
                'no_hp' => trim((string) ($row['no_hp'] ?? '')) ?: null,
            ];

            if ($data['nama_pendaftar'] === '') {
                $gagal[] = 'nama pendaftar kosong';
            }

            foreach (self::NILAI_VALID as $kolom => $daftarValid) {
                $mentah = trim(preg_replace('/\s+/', ' ', (string) ($row[$kolom] ?? '')));

                if ($mentah === '') {
                    if (in_array($kolom, self::KOLOM_WAJIB, true)) {
                        $gagal[] = 'kolom '.str_replace('_', ' ', $kolom).' kosong';
                    }
                    $data[$kolom] = null;
                    continue;
                }

                $cocok = null;
                foreach ($daftarValid as $valid) {
                    if (strcasecmp($valid, $mentah) === 0) {
                        $cocok = $valid;
                        break;
                    }
                }

                if ($cocok === null) {
                    $gagal[] = "nilai '{$mentah}' pada kolom ".str_replace('_', ' ', $kolom).' tidak dikenali';
                    continue;
                }

                $data[$kolom] = $cocok;
            }

            if ($gagal !== []) {
                $this->barisGagal[] = 'Baris '.$noBaris.': '.implode('; ', $gagal).'.';
                continue;
            }

            Pendaftar::create($data);
            $this->jumlahBerhasil++;
        }
    }
}
