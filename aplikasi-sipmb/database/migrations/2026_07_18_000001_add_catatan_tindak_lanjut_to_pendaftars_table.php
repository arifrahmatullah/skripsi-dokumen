<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('pendaftars', function (Blueprint $table) {
            $table->text('catatan_tindak_lanjut')->nullable()->after('prediksi');
            $table->timestamp('tindak_lanjut_pada')->nullable()->after('catatan_tindak_lanjut');
        });
    }

    public function down(): void
    {
        Schema::table('pendaftars', function (Blueprint $table) {
            $table->dropColumn(['catatan_tindak_lanjut', 'tindak_lanjut_pada']);
        });
    }
};
