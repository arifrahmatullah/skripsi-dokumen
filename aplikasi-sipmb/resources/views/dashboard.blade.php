<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Dashboard</h2>
    </x-slot>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        @php
            $cards = [
                ['big' => number_format($total, 0, ',', '.'), 'label' => 'Total Pendaftar', 'accent' => false],
                ['big' => number_format($masuk, 0, ',', '.'), 'label' => 'Prediksi MASUK', 'accent' => true],
                ['big' => number_format($tidakMasuk, 0, ',', '.'), 'label' => 'Prediksi TIDAK MASUK', 'accent' => false, 'muted' => true],
                ['big' => number_format($evaluasi['acc'], 2, ',', '.').'%', 'label' => 'Akurasi Model', 'accent' => false],
            ];
        @endphp
        @foreach ($cards as $c)
            <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-5">
                <div class="w-9 h-9 rounded-lg flex items-center justify-center mb-3 {{ $c['accent'] ? 'bg-accent-100' : 'bg-brand-50' }}">
                    <span class="w-2.5 h-2.5 rounded-full {{ $c['accent'] ? 'bg-accent-500' : (($c['muted'] ?? false) ? 'bg-gray-400' : 'bg-brand-600') }}"></span>
                </div>
                <div class="text-2xl font-bold {{ $c['accent'] ? 'text-accent-600' : 'text-brand-900' }}">{{ $c['big'] }}</div>
                <div class="text-xs text-gray-500 mt-1">{{ $c['label'] }}</div>
            </div>
        @endforeach
    </div>

    <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-100">
            <h3 class="font-bold text-sm text-gray-800">Ringkasan Prediksi Terbaru</h3>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-sm">
                <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-400">
                    <tr>
                        <th class="px-5 py-3 font-semibold">No</th>
                        <th class="px-5 py-3 font-semibold">Nama Pendaftar</th>
                        <th class="px-5 py-3 font-semibold">Status Test</th>
                        <th class="px-5 py-3 font-semibold">Nilai Test</th>
                        <th class="px-5 py-3 font-semibold">Prediksi</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    @forelse ($terbaru as $i => $row)
                        <tr class="hover:bg-gray-50/60">
                            <td class="px-5 py-3 text-gray-500">{{ $i + 1 }}</td>
                            <td class="px-5 py-3 font-medium text-gray-800">{{ $row->nama_pendaftar }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->status_test }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->kategori_nilai_test }}</td>
                            <td class="px-5 py-3">
                                <span class="px-2.5 py-1 rounded-full text-xs font-bold {{ $row->prediksi === 'MASUK' ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                                    {{ $row->prediksi }}
                                </span>
                            </td>
                        </tr>
                    @empty
                        <tr><td colspan="5" class="px-5 py-8 text-center text-gray-400">Belum ada data.</td></tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>
</x-app-layout>
