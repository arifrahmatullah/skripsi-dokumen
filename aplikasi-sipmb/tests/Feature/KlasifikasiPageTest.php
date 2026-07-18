<?php

namespace Tests\Feature;

use App\Models\Pendaftar;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class KlasifikasiPageTest extends TestCase
{
    use RefreshDatabase;

    public function test_halaman_klasifikasi_menampilkan_confusion_matrix(): void
    {
        $user = User::factory()->create();

        foreach (range(1, 10) as $i) {
            Pendaftar::create([
                'nama_pendaftar' => 'Pendaftar '.$i,
                'kategori_jarak_asal' => $i % 2 ? 'Dekat' : 'Jauh',
                'tingkat_follow_up_internal' => $i % 2 ? 'Follow Up Intensif' : 'Belum Dihubungi',
                'status_test' => $i % 2 ? 'Sudah Tes' : 'Belum Tes',
                'kategori_nilai_test' => $i % 2 ? 'Nilai Tinggi' : 'Tidak Ada Nilai',
                'kategori_penghasilan' => 'Tidak Diketahui',
                'status_retensi_final_target' => $i % 2 ? 'MASUK' : 'TIDAK MASUK',
            ]);
        }

        $response = $this->actingAs($user)->get(route('klasifikasi.index'));

        $response->assertOk();
        $response->assertSeeText('Confusion Matrix');
        $response->assertSeeText('true TIDAK MASUK');
        $response->assertSeeText('pred. MASUK');
        $response->assertSeeText('class precision');
        $response->assertSeeText('class recall');
    }

    public function test_halaman_klasifikasi_tetap_tampil_tanpa_data(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->get(route('klasifikasi.index'));

        $response->assertOk();
        $response->assertSeeText('Confusion Matrix');
    }
}
