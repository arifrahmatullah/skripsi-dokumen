<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Rekomendasi Tindak Lanjut</h2>
    </x-slot>

    <div class="space-y-3">
        @forelse ($pendaftar as $row)
            @php $isMasuk = $row->prediksi === 'MASUK'; @endphp
            <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <span class="w-1.5 h-10 rounded-full {{ $isMasuk ? 'bg-accent-500' : 'bg-gray-300' }}"></span>
                    <div>
                        <div class="font-bold text-gray-800">{{ $row->nama_pendaftar }}</div>
                        <div class="text-xs text-gray-500">{{ $row->rekomendasiTindakLanjut() }}</div>
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <span class="px-3 py-1 rounded-full text-xs font-bold {{ $isMasuk ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                        {{ $row->prediksi }}
                    </span>
                    <a href="{{ route('klasifikasi.show', $row) }}" class="text-brand-600 text-sm font-medium hover:text-brand-800">Detail</a>
                </div>
            </div>
        @empty
            <p class="text-gray-400 text-sm">Belum ada data yang bisa direkomendasikan.</p>
        @endforelse
    </div>

    <div class="mt-5">{{ $pendaftar->links() }}</div>
</x-app-layout>
