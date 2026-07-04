<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('pendaftars', function (Blueprint $table) {
            $table->id();
            $table->string('nama_pendaftar');
            $table->string('prodi')->nullable();
            $table->string('asal_kota')->nullable();
            $table->enum('kategori_jarak_asal', ['Dekat', 'Sedang', 'Jauh']);
            $table->enum('kategori_asal_sekolah', ['Sekolah Negeri', 'Sekolah Swasta', 'Sekolah Madrasah', 'Pondok Pesantren'])->nullable();
            $table->enum('waktu_pendaftaran', ['Awal Gelombang', 'Tengah Gelombang', 'Akhir Gelombang'])->nullable();
            $table->enum('tingkat_follow_up_internal', ['Belum Dihubungi', 'Kontak Awal', 'Follow Up', 'Follow Up Intensif']);
            $table->enum('status_uang_pendaftaran', ['Belum Lunas', 'Lunas'])->nullable();
            $table->enum('status_test', ['Belum Tes', 'Sudah Tes']);
            $table->enum('kategori_nilai_test', ['Tidak Ada Nilai', 'Nilai Sedang', 'Nilai Tinggi']);
            $table->enum('kategori_penghasilan', [
                'Tidak Diketahui', 'Dibawah Rp.1.000.000', 'Rp.1.000.000 - Rp.2.000.000',
                'Rp.2.000.001 - Rp.4.000.000', 'Rp.4.000.001 - Rp.6.000.000', 'Diatas Rp.6.000.000',
            ]);
            $table->enum('status_retensi_final_target', ['MASUK', 'TIDAK MASUK'])->nullable()
                ->comment('Status aktual historis (label training). Null = pendaftar baru, belum ada kepastian.');
            $table->decimal('prob_masuk', 10, 8)->nullable();
            $table->decimal('prob_tidak_masuk', 10, 8)->nullable();
            $table->enum('prediksi', ['MASUK', 'TIDAK MASUK'])->nullable();
            $table->timestamp('predicted_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('pendaftars');
    }
};
