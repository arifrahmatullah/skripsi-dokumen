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
    ];

    protected $casts = [
        'prob_masuk' => 'float',
        'prob_tidak_masuk' => 'float',
        'predicted_at' => 'datetime',
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
}
