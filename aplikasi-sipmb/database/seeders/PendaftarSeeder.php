<?php

namespace Database\Seeders;

use App\Models\Pendaftar;
use Illuminate\Database\Seeder;

class PendaftarSeeder extends Seeder
{
    public function run(): void
    {
        $path = database_path('seeders/data_pendaftar.csv');
        $handle = fopen($path, 'r');
        $header = fgetcsv($handle);

        $batch = [];
        $now = now();

        while (($row = fgetcsv($handle)) !== false) {
            $data = array_combine($header, $row);

            $batch[] = [
                'nama_pendaftar' => $data['nama_pendaftar'],
                'prodi' => $data['prodi'],
                'asal_kota' => $data['asal_kota'] !== '' ? $data['asal_kota'] : null,
                'kategori_jarak_asal' => $data['kategori_jarak_asal'],
                'kategori_asal_sekolah' => $data['kategori_asal_sekolah'],
                'waktu_pendaftaran' => $data['waktu_pendaftaran'],
                'tingkat_follow_up_internal' => $data['tingkat_follow_up_internal'],
                'status_uang_pendaftaran' => $data['status_uang_pendaftaran'],
                'status_test' => $data['status_test'],
                'kategori_nilai_test' => $data['kategori_nilai_test'],
                'kategori_penghasilan' => $data['kategori_penghasilan'],
                'status_retensi_final_target' => $data['status_retensi_final_target'],
                'created_at' => $now,
                'updated_at' => $now,
            ];

            if (count($batch) >= 200) {
                Pendaftar::insert($batch);
                $batch = [];
            }
        }
        if (! empty($batch)) {
            Pendaftar::insert($batch);
        }

        fclose($handle);

        $this->command->info('Pendaftar seeded: ' . Pendaftar::count());
    }
}
