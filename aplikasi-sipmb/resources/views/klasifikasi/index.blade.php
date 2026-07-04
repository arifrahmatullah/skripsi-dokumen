<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Hasil Klasifikasi Naive Bayes</h2>
    </x-slot>

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
