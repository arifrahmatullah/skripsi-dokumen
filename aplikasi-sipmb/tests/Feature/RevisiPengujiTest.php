<?php

namespace Tests\Feature;

use App\Models\Pendaftar;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RevisiPengujiTest extends TestCase
{
    use RefreshDatabase;

    private function buatDataBerlabel(int $jumlah = 10): void
    {
        foreach (range(1, $jumlah) as $i) {
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
    }

    private array $inputPrediksi = [
        'kategori_jarak_asal' => 'Dekat',
        'tingkat_follow_up_internal' => 'Follow Up Intensif',
        'status_test' => 'Sudah Tes',
        'kategori_nilai_test' => 'Nilai Tinggi',
        'kategori_penghasilan' => 'Tidak Diketahui',
    ];

    // Poin 1: halaman CRISP-DM

    public function test_halaman_crisp_dm_menampilkan_enam_tahap(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel();

        $response = $this->actingAs($user)->get(route('crispdm.index'));

        $response->assertOk();
        foreach (['Business Understanding', 'Data Understanding', 'Data Preparation', 'Modeling', 'Evaluation', 'Deployment'] as $tahap) {
            $response->assertSeeText($tahap);
        }
    }

    public function test_halaman_crisp_dm_tetap_tampil_tanpa_data(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->get(route('crispdm.index'));

        $response->assertOk();
        $response->assertSeeText('Model belum dilatih');
    }

    // Poin 2: guard konsistensi model

    public function test_probabilitas_tidak_dihitung_saat_data_training_kurang(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel(4); // di bawah minimal 10

        $response = $this->actingAs($user)->post(route('klasifikasi.proses-ulang'), [], ['HTTP_REFERER' => route('klasifikasi.index')]);
        $response->assertSessionHas('status', fn ($s) => str_contains($s, 'Klasifikasi tidak dijalankan'));

        $this->assertSame(0, Pendaftar::whereNotNull('prediksi')->count());

        $halaman = $this->actingAs($user)->get(route('klasifikasi.index'));
        $halaman->assertSeeText('Model belum memenuhi syarat pelatihan');
    }

    public function test_tambah_pendaftar_saat_model_belum_siap_tidak_diberi_prediksi(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel(2);

        $this->actingAs($user)->post(route('pendaftar.store'), array_merge($this->inputPrediksi, [
            'nama_pendaftar' => 'Calon Baru',
        ]));

        $this->assertNull(Pendaftar::where('nama_pendaftar', 'Calon Baru')->first()->prediksi);
    }

    // Poin 3: prediksi data baru

    public function test_prediksi_data_baru_menampilkan_hasil_dan_rincian_tanpa_menyimpan(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel();

        $response = $this->actingAs($user)->post(route('prediksi.prediksi'), $this->inputPrediksi);

        $response->assertOk();
        $response->assertSeeText('Hasil Prediksi');
        $response->assertSeeText('Peluang Masuk');
        $response->assertSeeText('Rincian Perhitungan Naive Bayes');
        $response->assertSeeText('Prior P(Y)');

        // data simulasi tidak boleh tersimpan
        $this->assertSame(10, Pendaftar::count());
    }

    public function test_prediksi_ditolak_saat_model_belum_siap(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel(3);

        $response = $this->actingAs($user)->post(route('prediksi.prediksi'), $this->inputPrediksi);

        $response->assertRedirect(route('prediksi.index'));
        $response->assertSessionHas('status', fn ($s) => str_contains($s, 'Prediksi tidak dapat dijalankan'));
    }

    // Poin 4: detail confusion matrix

    public function test_confusion_matrix_menampilkan_detail_tp_tn_fp_fn_dan_rumus(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel();

        $response = $this->actingAs($user)->get(route('klasifikasi.index'));

        $response->assertOk();
        $response->assertSeeText('TP (True Positive)');
        $response->assertSeeText('FN (False Negative)');
        $response->assertSeeText('Akurasi = (TP+TN)/(TP+TN+FP+FN)');
        $response->assertSeeText('Presisi = TP/(TP+FP)');
    }

    // Poin 5: catatan tindak lanjut

    public function test_catatan_tindak_lanjut_dapat_disimpan(): void
    {
        $user = User::factory()->create();
        $this->buatDataBerlabel();
        $target = Pendaftar::first();
        $target->update(['prediksi' => 'MASUK', 'prob_masuk' => 0.5, 'prob_tidak_masuk' => 0.1]);

        $response = $this->actingAs($user)->post(route('rekomendasi.catatan', $target), [
            'catatan_tindak_lanjut' => 'Sudah dihubungi via WhatsApp, menunggu konfirmasi.',
        ], ['HTTP_REFERER' => route('rekomendasi.index')]);

        $response->assertSessionHas('status', fn ($s) => str_contains($s, 'Catatan tindak lanjut'));

        $target->refresh();
        $this->assertSame('Sudah dihubungi via WhatsApp, menunggu konfirmasi.', $target->catatan_tindak_lanjut);
        $this->assertNotNull($target->tindak_lanjut_pada);

        $halaman = $this->actingAs($user)->get(route('rekomendasi.index'));
        $halaman->assertSeeText('Sudah dihubungi via WhatsApp');
    }
}
