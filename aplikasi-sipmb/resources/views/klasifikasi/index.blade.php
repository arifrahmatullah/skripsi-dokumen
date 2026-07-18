<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Hasil Klasifikasi Naive Bayes</h2>
    </x-slot>

    @if (! $kesiapan['siap'])
        <div class="mb-5 px-4 py-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm">
            <span class="font-semibold">Model belum memenuhi syarat pelatihan.</span>
            {{ $kesiapan['alasan'] }}
            Probabilitas sengaja tidak dihitung agar hasil klasifikasi tetap konsisten dengan karakteristik algoritma Naive Bayes
            (minimal {{ $kesiapan['minimal'] }} data berlabel dan kedua kelas terwakili).
        </div>
    @endif

    <div class="flex flex-wrap items-center justify-between gap-3 mb-5">
        <div class="flex gap-3 text-sm">
            @foreach ([
                ['label' => 'Akurasi', 'val' => $evaluasi['acc']],
                ['label' => 'Presisi', 'val' => $evaluasi['prec']],
                ['label' => 'Recall', 'val' => $evaluasi['rec']],
                ['label' => 'F1-Score', 'val' => $evaluasi['f1']],
            ] as $m)
                <div class="bg-white rounded-lg ring-1 ring-gray-100 shadow-sm px-4 py-2">
                    <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">{{ $m['label'] }}</div>
                    <div class="font-bold text-brand-800">{{ number_format($m['val'], 2) }}%</div>
                </div>
            @endforeach
        </div>
        <form method="POST" action="{{ route('klasifikasi.proses-ulang') }}">
            @csrf
            <button class="px-4 py-2.5 bg-accent-500 text-white text-sm font-semibold rounded-lg hover:bg-accent-600 transition shadow-sm shadow-accent-500/20">
                Proses Ulang
            </button>
        </form>
    </div>

    @php
        $tp = $evaluasi['tp']; $tn = $evaluasi['tn']; $fp = $evaluasi['fp']; $fn = $evaluasi['fn'];
        $precTidakMasuk = ($tn + $fn) > 0 ? round($tn / ($tn + $fn) * 100, 2) : 0.0;
        $precMasuk      = ($tp + $fp) > 0 ? round($tp / ($tp + $fp) * 100, 2) : 0.0;
        $recTidakMasuk  = ($tn + $fp) > 0 ? round($tn / ($tn + $fp) * 100, 2) : 0.0;
        $recMasuk       = ($tp + $fn) > 0 ? round($tp / ($tp + $fn) * 100, 2) : 0.0;
    @endphp
    <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden mb-5">
        <div class="px-5 py-4 border-b border-gray-100 flex flex-wrap items-baseline justify-between gap-2">
            <h3 class="font-bold text-gray-800">Confusion Matrix</h3>
            <p class="text-xs text-gray-400">
                Pengujian pada {{ $evaluasi['n_test'] }} data uji (split 80/20 dari {{ $evaluasi['n_train'] + $evaluasi['n_test'] }} data berlabel) —
                <span class="font-semibold text-gray-600">accuracy: {{ number_format($evaluasi['acc'], 2) }}%</span>
            </p>
        </div>
        <div class="overflow-x-auto p-5">
            <table class="text-sm border border-gray-200 min-w-[480px]">
                <thead>
                    <tr class="text-left text-xs text-gray-500">
                        <th class="px-4 py-2.5 border border-gray-200 bg-gray-50"></th>
                        <th class="px-4 py-2.5 border border-gray-200 bg-gray-50 font-semibold">true TIDAK MASUK</th>
                        <th class="px-4 py-2.5 border border-gray-200 bg-gray-50 font-semibold">true MASUK</th>
                        <th class="px-4 py-2.5 border border-gray-200 bg-gray-50 font-semibold">class precision</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="px-4 py-2.5 border border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500">pred. TIDAK MASUK</td>
                        <td class="px-4 py-2.5 border border-gray-200 bg-amber-50 font-bold text-gray-800">{{ $tn }} <span class="text-[10px] font-semibold text-amber-600">(TN)</span></td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ $fn }} <span class="text-[10px] font-semibold text-gray-400">(FN)</span></td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ number_format($precTidakMasuk, 2) }}%</td>
                    </tr>
                    <tr>
                        <td class="px-4 py-2.5 border border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500">pred. MASUK</td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ $fp }} <span class="text-[10px] font-semibold text-gray-400">(FP)</span></td>
                        <td class="px-4 py-2.5 border border-gray-200 bg-amber-50 font-bold text-gray-800">{{ $tp }} <span class="text-[10px] font-semibold text-amber-600">(TP)</span></td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ number_format($precMasuk, 2) }}%</td>
                    </tr>
                    <tr>
                        <td class="px-4 py-2.5 border border-gray-200 bg-gray-50 text-xs font-semibold text-gray-500">class recall</td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ number_format($recTidakMasuk, 2) }}%</td>
                        <td class="px-4 py-2.5 border border-gray-200 text-gray-600">{{ number_format($recMasuk, 2) }}%</td>
                        <td class="px-4 py-2.5 border border-gray-200"></td>
                    </tr>
                </tbody>
            </table>

            @php $totalUji = $tp + $tn + $fp + $fn; @endphp
            <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-1.5 text-xs text-gray-500">
                <p><span class="font-semibold text-gray-600">TP (True Positive)</span> = {{ $tp }} — diprediksi MASUK dan benar MASUK</p>
                <p><span class="font-semibold text-gray-600">TN (True Negative)</span> = {{ $tn }} — diprediksi TIDAK MASUK dan benar TIDAK MASUK</p>
                <p><span class="font-semibold text-gray-600">FP (False Positive)</span> = {{ $fp }} — diprediksi MASUK padahal TIDAK MASUK</p>
                <p><span class="font-semibold text-gray-600">FN (False Negative)</span> = {{ $fn }} — diprediksi TIDAK MASUK padahal MASUK</p>
            </div>
            <div class="mt-3 pt-3 border-t border-gray-100 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-1.5 text-xs text-gray-500 font-mono">
                <p>Akurasi = (TP+TN)/(TP+TN+FP+FN) = ({{ $tp }}+{{ $tn }})/{{ max($totalUji, 1) }} = <span class="font-bold text-gray-700">{{ number_format($evaluasi['acc'], 2) }}%</span></p>
                <p>Presisi = TP/(TP+FP) = {{ $tp }}/{{ $tp + $fp }} = <span class="font-bold text-gray-700">{{ number_format($evaluasi['prec'], 2) }}%</span></p>
                <p>Recall = TP/(TP+FN) = {{ $tp }}/{{ $tp + $fn }} = <span class="font-bold text-gray-700">{{ number_format($evaluasi['rec'], 2) }}%</span></p>
                <p>F1-Score = 2&times;P&times;R/(P+R) = <span class="font-bold text-gray-700">{{ number_format($evaluasi['f1'], 2) }}%</span></p>
            </div>
        </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-sm">
                <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-400">
                    <tr>
                        <th class="px-5 py-3 font-semibold">No</th>
                        <th class="px-5 py-3 font-semibold">Nama</th>
                        <th class="px-5 py-3 font-semibold">P(MASUK|X)</th>
                        <th class="px-5 py-3 font-semibold">P(TIDAK MASUK|X)</th>
                        <th class="px-5 py-3 font-semibold">Prediksi</th>
                        <th class="px-5 py-3 font-semibold">Aksi</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    @forelse ($pendaftar as $i => $row)
                        <tr class="hover:bg-gray-50/60">
                            <td class="px-5 py-3 text-gray-500">{{ $pendaftar->firstItem() + $i }}</td>
                            <td class="px-5 py-3 font-medium text-gray-800">{{ $row->nama_pendaftar }}</td>
                            <td class="px-5 py-3 text-gray-600 font-mono text-xs">{{ number_format($row->prob_masuk, 6) }}</td>
                            <td class="px-5 py-3 text-gray-600 font-mono text-xs">{{ number_format($row->prob_tidak_masuk, 6) }}</td>
                            <td class="px-5 py-3">
                                <span class="px-2.5 py-1 rounded-full text-xs font-bold {{ $row->prediksi === 'MASUK' ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                                    {{ $row->prediksi ?? '-' }}
                                </span>
                            </td>
                            <td class="px-5 py-3">
                                <a href="{{ route('klasifikasi.show', $row) }}" class="text-brand-600 hover:text-brand-800 font-medium">Detail</a>
                            </td>
                        </tr>
                    @empty
                        <tr><td colspan="6" class="px-5 py-8 text-center text-gray-400">Belum ada data.</td></tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        <div class="px-5 py-4 border-t border-gray-100">
            {{ $pendaftar->links() }}
        </div>
    </div>
</x-app-layout>
