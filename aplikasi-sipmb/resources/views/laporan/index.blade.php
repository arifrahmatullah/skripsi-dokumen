<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Cetak / Export Laporan</h2>
    </x-slot>

    <form method="GET" class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-6 mb-5">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
                <x-input-label value="Tanggal Dari" />
                <input type="date" name="dari" value="{{ request('dari') }}" class="block mt-1.5 w-full rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500">
            </div>
            <div>
                <x-input-label value="Tanggal Sampai" />
                <input type="date" name="sampai" value="{{ request('sampai') }}" class="block mt-1.5 w-full rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500">
            </div>
            <div>
                <x-input-label value="Status Prediksi" />
                <select name="status" class="block mt-1.5 w-full rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500">
                    <option value="">Semua</option>
                    <option value="MASUK" @selected(request('status') === 'MASUK')>MASUK</option>
                    <option value="TIDAK MASUK" @selected(request('status') === 'TIDAK MASUK')>TIDAK MASUK</option>
                </select>
            </div>
            <button class="px-4 py-2.5 bg-brand-700 text-white text-sm font-semibold rounded-lg hover:bg-brand-800 transition">Filter</button>
        </div>
        <div class="mt-5 flex gap-3">
            <a href="{{ route('laporan.export-pdf', request()->query()) }}" class="px-4 py-2.5 bg-accent-500 text-white text-sm font-semibold rounded-lg hover:bg-accent-600 transition shadow-sm shadow-accent-500/20">Export PDF</a>
            <a href="{{ route('laporan.export-excel', request()->query()) }}" class="px-4 py-2.5 bg-accent-500 text-white text-sm font-semibold rounded-lg hover:bg-accent-600 transition shadow-sm shadow-accent-500/20">Export Excel</a>
        </div>
    </form>

    <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-sm">
                <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-400">
                    <tr>
                        <th class="px-5 py-3 font-semibold">No</th>
                        <th class="px-5 py-3 font-semibold">Nama</th>
                        <th class="px-5 py-3 font-semibold">Prediksi</th>
                        <th class="px-5 py-3 font-semibold">Tgl. Input</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    @forelse ($pendaftar as $i => $row)
                        <tr class="hover:bg-gray-50/60">
                            <td class="px-5 py-3 text-gray-500">{{ $pendaftar->firstItem() + $i }}</td>
                            <td class="px-5 py-3 font-medium text-gray-800">{{ $row->nama_pendaftar }}</td>
                            <td class="px-5 py-3">
                                <span class="px-2.5 py-1 rounded-full text-xs font-bold {{ $row->prediksi === 'MASUK' ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                                    {{ $row->prediksi ?? '-' }}
                                </span>
                            </td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->created_at->format('d-m-Y') }}</td>
                        </tr>
                    @empty
                        <tr><td colspan="4" class="px-5 py-8 text-center text-gray-400">Tidak ada data.</td></tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        <div class="px-5 py-4 border-t border-gray-100">{{ $pendaftar->links() }}</div>
    </div>
</x-app-layout>
