<?php

namespace Tests\Feature;

use App\Models\Pendaftar;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\UploadedFile;
use Tests\TestCase;

class PendaftarImportTest extends TestCase
{
    use RefreshDatabase;

    private function csvValid(): string
    {
        $baris = [
            'Nama Pendaftar,Prodi,Asal Kota,No HP,Kategori Jarak Asal,Kategori Asal Sekolah,Waktu Pendaftaran,Tingkat Follow Up Internal,Status Uang Pendaftaran,Status Test,Kategori Nilai Test,Kategori Penghasilan,Status Retensi Final Target',
        ];
        foreach (range(1, 5) as $i) {
            $baris[] = "Calon Masuk {$i},Manajemen Bisnis Syariah,Bogor,0812345678{$i},Dekat,Sekolah Negeri,Awal Gelombang,Follow Up Intensif,Lunas,Sudah Tes,Nilai Tinggi,Rp.2.000.001 - Rp.4.000.000,MASUK";
            $baris[] = "Calon Tidak Masuk {$i},Akuntansi Syariah,Medan,,Jauh,Pondok Pesantren,Akhir Gelombang,Belum Dihubungi,Belum Lunas,Belum Tes,Tidak Ada Nilai,Tidak Diketahui,TIDAK MASUK";
        }
        $baris[] = 'Baris Rusak,,,,KategoriSalah,,,Belum Dihubungi,,Belum Tes,Tidak Ada Nilai,Tidak Diketahui,';

        return implode("\n", $baris);
    }

    public function test_import_csv_menyimpan_baris_valid_dan_melewati_baris_rusak(): void
    {
        $user = User::factory()->create();
        $file = UploadedFile::fake()->createWithContent('pendaftar.csv', $this->csvValid());

        $response = $this->actingAs($user)->post(route('pendaftar.import'), ['file' => $file]);

        $response->assertRedirect(route('pendaftar.index'));
        $response->assertSessionHas('status', fn ($s) => str_contains($s, '10 data pendaftar berhasil diimpor'));
        $response->assertSessionHas('import_gagal', fn ($g) => count($g) === 1 && str_contains($g[0], 'Baris 12'));

        $this->assertSame(10, Pendaftar::count());
        $this->assertDatabaseHas('pendaftars', [
            'nama_pendaftar' => 'Calon Masuk 1',
            'status_retensi_final_target' => 'MASUK',
        ]);

        // setelah import, seluruh data harus sudah diklasifikasi
        // (10 data berlabel dengan dua kelas = memenuhi syarat pelatihan model)
        $this->assertSame(0, Pendaftar::whereNull('prediksi')->count());
    }

    public function test_import_menolak_file_selain_excel_csv(): void
    {
        $user = User::factory()->create();
        $file = UploadedFile::fake()->createWithContent('data.pdf', 'bukan spreadsheet');

        $response = $this->actingAs($user)->post(route('pendaftar.import'), ['file' => $file]);

        $response->assertSessionHasErrors('file');
        $this->assertSame(0, Pendaftar::count());
    }

    public function test_template_import_dapat_diunduh(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->get(route('pendaftar.import.template'));

        $response->assertOk();
        $response->assertDownload('template-import-pendaftar.xlsx');
    }
}
