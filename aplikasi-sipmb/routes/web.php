<?php

use App\Http\Controllers\CrispDmController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\KlasifikasiController;
use App\Http\Controllers\PrediksiController;
use App\Http\Controllers\LaporanController;
use App\Http\Controllers\PendaftarController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\RekomendasiController;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/dashboard', DashboardController::class)->name('dashboard');

    Route::get('/pendaftar-import/template', [PendaftarController::class, 'template'])->name('pendaftar.import.template');
    Route::post('/pendaftar-import', [PendaftarController::class, 'import'])->name('pendaftar.import');
    Route::resource('pendaftar', PendaftarController::class)->except(['show']);

    Route::get('/klasifikasi', [KlasifikasiController::class, 'index'])->name('klasifikasi.index');
    Route::get('/klasifikasi/{pendaftar}', [KlasifikasiController::class, 'show'])->name('klasifikasi.show');
    Route::post('/klasifikasi/proses-ulang', [KlasifikasiController::class, 'prosesUlang'])->name('klasifikasi.proses-ulang');

    Route::get('/prediksi', [PrediksiController::class, 'index'])->name('prediksi.index');
    Route::post('/prediksi', [PrediksiController::class, 'prediksi'])->name('prediksi.prediksi');

    Route::get('/crisp-dm', [CrispDmController::class, 'index'])->name('crispdm.index');

    Route::get('/rekomendasi', [RekomendasiController::class, 'index'])->name('rekomendasi.index');
    Route::post('/rekomendasi/{pendaftar}/catatan', [RekomendasiController::class, 'simpanCatatan'])->name('rekomendasi.catatan');

    Route::get('/laporan', [LaporanController::class, 'index'])->name('laporan.index');
    Route::get('/laporan/export-pdf', [LaporanController::class, 'exportPdf'])->name('laporan.export-pdf');
    Route::get('/laporan/export-excel', [LaporanController::class, 'exportExcel'])->name('laporan.export-excel');

    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

require __DIR__.'/auth.php';
