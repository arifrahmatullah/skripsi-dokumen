<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Proses Data Mining — Alur CRISP-DM</h2>
    </x-slot>

    @php
        $labelFitur = [
            'kategori_jarak_asal' => 'Kategori Jarak Asal',
            'tingkat_follow_up_internal' => 'Tingkat Follow Up Internal',
            'status_test' => 'Status Test',
            'kategori_nilai_test' => 'Kategori Nilai Test',
            'kategori_penghasilan' => 'Kategori Penghasilan',
        ];
    @endphp

    <p class="text-sm text-gray-500 mb-6 max-w-3xl">
        Halaman ini menampilkan penerapan metodologi <span class="font-semibold">CRISP-DM</span>
        (Cross-Industry Standard Process for Data Mining) pada sistem, dengan data aktual yang
        sedang tersimpan di aplikasi.
    </p>

    <div class="space-y-5 max-w-4xl">
        {{-- 1. Business Understanding --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">1</span>
                <h3 class="font-bold text-gray-800">Business Understanding</h3>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed">
                Tim Marketing Universitas Tazkia perlu memprioritaskan tindak lanjut konfirmasi
                pendaftaran mahasiswa baru. Sistem mengklasifikasikan calon mahasiswa ke kelas
                <span class="font-semibold">MASUK</span> atau <span class="font-semibold">TIDAK MASUK</span>
                menggunakan algoritma Naive Bayes, sehingga upaya follow up dapat difokuskan pada
                pendaftar dengan peluang masuk tertinggi.
            </p>
        </div>

        {{-- 2. Data Understanding --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">2</span>
                <h3 class="font-bold text-gray-800">Data Understanding</h3>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm mb-4">
                @foreach ([
                    ['label' => 'Total Data', 'val' => $total],
                    ['label' => 'Data Berlabel', 'val' => $kesiapan['n_berlabel']],
                    ['label' => 'Label MASUK', 'val' => $kesiapan['n_masuk']],
                    ['label' => 'Label TIDAK MASUK', 'val' => $kesiapan['n_tidak_masuk']],
                ] as $s)
                    <div class="bg-gray-50 rounded-lg p-3">
                        <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">{{ $s['label'] }}</div>
                        <div class="text-xl font-bold text-brand-800">{{ $s['val'] }}</div>
                    </div>
                @endforeach
            </div>
            <details>
                <summary class="text-sm text-brand-600 font-medium cursor-pointer hover:text-brand-800">
                    Lihat distribusi nilai tiap atribut
                </summary>
                <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                    @foreach ($distribusiFitur as $f => $counts)
                        <div class="border border-gray-100 rounded-lg overflow-hidden">
                            <div class="px-4 py-2 bg-gray-50 text-xs font-semibold text-gray-500">{{ $labelFitur[$f] }}</div>
                            <table class="w-full text-xs">
                                @foreach ($counts as $nilai => $jml)
                                    <tr class="border-t border-gray-50">
                                        <td class="px-4 py-1.5 text-gray-600">{{ $nilai }}</td>
                                        <td class="px-4 py-1.5 text-right font-semibold text-gray-700">{{ $jml }}</td>
                                    </tr>
                                @endforeach
                            </table>
                        </div>
                    @endforeach
                </div>
            </details>
        </div>

        {{-- 3. Data Preparation --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">3</span>
                <h3 class="font-bold text-gray-800">Data Preparation</h3>
            </div>
            <ul class="text-sm text-gray-600 space-y-1.5 list-disc ms-5 leading-relaxed">
                <li>Atribut prediktor yang digunakan: <span class="font-medium text-gray-800">{{ implode(', ', array_values($labelFitur)) }}</span> — seluruhnya bertipe kategorik sesuai karakteristik Naive Bayes.</li>
                <li>Hanya data dengan label <span class="font-medium">Status Retensi Aktual</span> (hasil akhir yang sudah dipastikan) yang dipakai sebagai data training.</li>
                <li>Data dengan atribut belum lengkap otomatis <span class="font-medium">dikeluarkan dari perhitungan</span> (tidak diprediksi) untuk menjaga konsistensi hasil.</li>
                <li>Nilai kategori dinormalisasi saat input/import (pencocokan kategori baku, pembersihan spasi).</li>
            </ul>
        </div>

        {{-- 4. Modeling --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">4</span>
                <h3 class="font-bold text-gray-800">Modeling — Naive Bayes</h3>
            </div>
            @if (! $kesiapan['siap'])
                <div class="px-4 py-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm">
                    <span class="font-semibold">Model belum dilatih.</span> {{ $kesiapan['alasan'] }}
                    Syarat: minimal {{ $kesiapan['minimal'] }} data berlabel dengan kedua kelas terwakili.
                </div>
            @else
                <p class="text-sm text-gray-600 mb-3">
                    Model dilatih dari <span class="font-semibold">{{ $model['n_train'] }}</span> data berlabel
                    dengan <span class="font-medium">Laplace smoothing</span>.
                    Prior probability:
                    <span class="font-mono text-xs">P(MASUK) = {{ number_format($model['prior']['MASUK'] / max($model['n_train'], 1), 4) }}</span>,
                    <span class="font-mono text-xs">P(TIDAK MASUK) = {{ number_format($model['prior']['TIDAK MASUK'] / max($model['n_train'], 1), 4) }}</span>
                </p>
                <details>
                    <summary class="text-sm text-brand-600 font-medium cursor-pointer hover:text-brand-800">
                        Lihat tabel conditional probability P(x|Y)
                    </summary>
                    <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                        @foreach ($model['cond'] as $f => $perKelas)
                            <div class="border border-gray-100 rounded-lg overflow-hidden">
                                <div class="px-4 py-2 bg-gray-50 text-xs font-semibold text-gray-500">{{ $labelFitur[$f] }}</div>
                                <table class="w-full text-xs">
                                    <tr class="border-t border-gray-50 text-gray-400">
                                        <td class="px-4 py-1.5">Nilai</td>
                                        <td class="px-4 py-1.5 text-right">MASUK</td>
                                        <td class="px-4 py-1.5 text-right">TIDAK MASUK</td>
                                    </tr>
                                    @foreach ($perKelas['MASUK'] as $nilai => $p)
                                        <tr class="border-t border-gray-50">
                                            <td class="px-4 py-1.5 text-gray-600">{{ $nilai }}</td>
                                            <td class="px-4 py-1.5 text-right font-mono text-gray-700">{{ number_format($p, 4) }}</td>
                                            <td class="px-4 py-1.5 text-right font-mono text-gray-700">{{ number_format($perKelas['TIDAK MASUK'][$nilai], 4) }}</td>
                                        </tr>
                                    @endforeach
                                </table>
                            </div>
                        @endforeach
                    </div>
                </details>
            @endif
        </div>

        {{-- 5. Evaluation --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">5</span>
                <h3 class="font-bold text-gray-800">Evaluation</h3>
            </div>
            @if (! $evaluasi)
                <p class="text-sm text-gray-500">Evaluasi belum dapat dijalankan karena model belum dilatih.</p>
            @else
                <p class="text-sm text-gray-600 mb-3">
                    Pengujian split 80/20: {{ $evaluasi['n_train'] }} data training, {{ $evaluasi['n_test'] }} data uji.
                </p>
                <div class="flex flex-wrap gap-3 text-sm mb-3">
                    @foreach ([
                        ['label' => 'Akurasi', 'val' => $evaluasi['acc']],
                        ['label' => 'Presisi', 'val' => $evaluasi['prec']],
                        ['label' => 'Recall', 'val' => $evaluasi['rec']],
                        ['label' => 'F1-Score', 'val' => $evaluasi['f1']],
                    ] as $m)
                        <div class="bg-gray-50 rounded-lg px-4 py-2">
                            <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">{{ $m['label'] }}</div>
                            <div class="font-bold text-brand-800">{{ number_format($m['val'], 2) }}%</div>
                        </div>
                    @endforeach
                </div>
                <a href="{{ route('klasifikasi.index') }}" class="text-sm text-brand-600 font-medium hover:text-brand-800">
                    Lihat confusion matrix lengkap di halaman Hasil Klasifikasi &rarr;
                </a>
            @endif
        </div>

        {{-- 6. Deployment --}}
        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6">
            <div class="flex items-center gap-3 mb-3">
                <span class="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center text-sm font-bold shrink-0">6</span>
                <h3 class="font-bold text-gray-800">Deployment</h3>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm mb-3">
                @foreach ([
                    ['label' => 'Data Terklasifikasi', 'val' => $terklasifikasi],
                    ['label' => 'Prediksi MASUK', 'val' => $prediksiMasuk],
                    ['label' => 'Prediksi TIDAK MASUK', 'val' => $terklasifikasi - $prediksiMasuk],
                    ['label' => 'Sudah Ditindaklanjuti', 'val' => $sudahDitindaklanjuti],
                ] as $s)
                    <div class="bg-gray-50 rounded-lg p-3">
                        <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">{{ $s['label'] }}</div>
                        <div class="text-xl font-bold text-brand-800">{{ $s['val'] }}</div>
                    </div>
                @endforeach
            </div>
            <p class="text-sm text-gray-600 leading-relaxed">
                Hasil klasifikasi diterapkan sebagai daftar prioritas pada menu
                <a href="{{ route('rekomendasi.index') }}" class="text-brand-600 font-medium hover:text-brand-800">Rekomendasi</a>
                (lengkap dengan aksi Hubungi via WhatsApp dan catatan tindak lanjut), prediksi kasus baru tersedia pada menu
                <a href="{{ route('prediksi.index') }}" class="text-brand-600 font-medium hover:text-brand-800">Prediksi Data Baru</a>,
                dan hasil dapat diekspor melalui menu
                <a href="{{ route('laporan.index') }}" class="text-brand-600 font-medium hover:text-brand-800">Laporan</a>.
            </p>
        </div>
    </div>
</x-app-layout>
