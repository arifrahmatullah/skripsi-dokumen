<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Pendaftar extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_pendaftar',
        'prodi',
        'asal_kota',
        'no_hp',
        'kategori_jarak_asal',
        'kategori_asal_sekolah',
        'waktu_pendaftaran',
        'tingkat_follow_up_internal',
        'status_uang_pendaftaran',
        'status_test',
        'kategori_nilai_test',
        'kategori_penghasilan',
        'status_retensi_final_target',
        'prob_masuk',
        'prob_tidak_masuk',
        'prediksi',
        'predicted_at',
        'catatan_tindak_lanjut',
        'tindak_lanjut_pada',
    ];

    protected $casts = [
        'prob_masuk' => 'float',
        'prob_tidak_masuk' => 'float',
        'predicted_at' => 'datetime',
        'tindak_lanjut_pada' => 'datetime',
    ];

    public const FITUR = [
        'kategori_jarak_asal',
        'tingkat_follow_up_internal',
        'status_test',
        'kategori_nilai_test',
        'kategori_penghasilan',
    ];

    public function rekomendasiTindakLanjut(): string
    {
        return $this->prediksi === 'MASUK'
            ? 'Prioritas Tinggi - Segera hubungi'
            : 'Prioritas Rendah - Follow up lanjutan';
    }

    /**
     * Persentase peluang MASUK: posterior dinormalisasi terhadap total
     * kedua kelas, karena prob_masuk/prob_tidak_masuk tersimpan sebagai
     * skor mentah hasil perkalian probabilitas.
     */
    public function persentaseMasuk(): ?float
    {
        $total = (float) $this->prob_masuk + (float) $this->prob_tidak_masuk;
        if ($this->prediksi === null || $total <= 0) {
            return null;
        }

        return round((float) $this->prob_masuk / $total * 100, 2);
    }

    public function linkWhatsApp(): ?string
    {
        $digits = preg_replace('/\D+/', '', (string) $this->no_hp);
        if ($digits === '') {
            return null;
        }
        if (str_starts_with($digits, '0')) {
            $digits = '62'.substr($digits, 1);
        } elseif (str_starts_with($digits, '8')) {
            $digits = '62'.$digits;
        }

        $pesan = 'Assalamualaikum '.$this->nama_pendaftar.', kami dari Tim Marketing Universitas Tazkia ingin menindaklanjuti proses pendaftaran Anda.';

        return 'https://wa.me/'.$digits.'?text='.rawurlencode($pesan);
    }
}
