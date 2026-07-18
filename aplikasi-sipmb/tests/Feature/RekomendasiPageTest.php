<?php

namespace Tests\Feature;

use App\Models\Pendaftar;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RekomendasiPageTest extends TestCase
{
    use RefreshDatabase;

    private function buatPendaftar(array $override = []): Pendaftar
    {
        return Pendaftar::create(array_merge([
            'nama_pendaftar' => 'Budi Santoso',
            'kategori_jarak_asal' => 'Dekat',
            'tingkat_follow_up_internal' => 'Follow Up Intensif',
            'status_test' => 'Sudah Tes',
            'kategori_nilai_test' => 'Nilai Tinggi',
            'kategori_penghasilan' => 'Tidak Diketahui',
            'prob_masuk' => 0.0003,
            'prob_tidak_masuk' => 0.0001,
            'prediksi' => 'MASUK',
        ], $override));
    }

    public function test_persentase_masuk_dinormalisasi_dari_kedua_kelas(): void
    {
        $p = $this->buatPendaftar();

        $this->assertSame(75.0, $p->persentaseMasuk());
    }

    public function test_link_whatsapp_mengubah_awalan_nol_menjadi_62(): void
    {
        $p = $this->buatPendaftar(['no_hp' => '0812-3456-7890']);

        $this->assertStringStartsWith('https://wa.me/6281234567890?text=', $p->linkWhatsApp());
        $this->assertNull($this->buatPendaftar()->linkWhatsApp());
    }

    public function test_pencarian_nama_dan_filter_prediksi(): void
    {
        $user = User::factory()->create();
        $this->buatPendaftar(['nama_pendaftar' => 'Budi Santoso']);
        $this->buatPendaftar([
            'nama_pendaftar' => 'Siti Aminah',
            'prediksi' => 'TIDAK MASUK',
            'prob_masuk' => 0.0001,
            'prob_tidak_masuk' => 0.0003,
        ]);

        $cari = $this->actingAs($user)->get(route('rekomendasi.index', ['q' => 'budi']));
        $cari->assertOk();
        $cari->assertSeeText('Budi Santoso');
        $cari->assertDontSeeText('Siti Aminah');

        $filter = $this->actingAs($user)->get(route('rekomendasi.index', ['prediksi' => 'TIDAK MASUK']));
        $filter->assertOk();
        $filter->assertSeeText('Siti Aminah');
        $filter->assertDontSeeText('Budi Santoso');

        $kosong = $this->actingAs($user)->get(route('rekomendasi.index', ['q' => 'tidak ada']));
        $kosong->assertSeeText('Tidak ada pendaftar yang cocok dengan pencarian.');
    }

    public function test_halaman_rekomendasi_menampilkan_persentase_dan_tombol_hubungi(): void
    {
        $user = User::factory()->create();
        $this->buatPendaftar(['no_hp' => '081234567890']);

        $response = $this->actingAs($user)->get(route('rekomendasi.index'));

        $response->assertOk();
        $response->assertSeeText('Peluang Masuk');
        $response->assertSeeText('75.0%');
        $response->assertSee('https://wa.me/6281234567890', false);
        $response->assertSeeText('Hubungi');
    }
}
