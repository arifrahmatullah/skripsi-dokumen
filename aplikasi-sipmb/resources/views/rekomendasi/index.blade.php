<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Rekomendasi Tindak Lanjut</h2>
    </x-slot>

    <form method="GET" class="flex flex-wrap items-center gap-3 mb-5">
        <div class="flex-1 max-w-md min-w-52">
            <input type="text" name="q" value="{{ request('q') }}" placeholder="Cari nama pendaftar..."
                   class="w-full rounded-lg border-gray-200 bg-white shadow-sm text-sm focus:border-brand-500 focus:ring-brand-500">
        </div>
        <select name="prediksi" onchange="this.form.submit()"
                class="rounded-lg border-gray-200 bg-white shadow-sm text-sm focus:border-brand-500 focus:ring-brand-500">
            <option value="">Semua Prediksi</option>
            <option value="MASUK" @selected(request('prediksi') === 'MASUK')>MASUK</option>
            <option value="TIDAK MASUK" @selected(request('prediksi') === 'TIDAK MASUK')>TIDAK MASUK</option>
        </select>
        <button type="submit"
                class="px-4 py-2.5 bg-brand-600 text-white text-sm font-semibold rounded-lg hover:bg-brand-700 transition shadow-sm">
            Cari
        </button>
        @if (request()->hasAny(['q', 'prediksi']))
            <a href="{{ route('rekomendasi.index') }}" class="text-sm text-gray-400 hover:text-gray-600 font-medium">Reset</a>
        @endif
    </form>

    <div class="space-y-3">
        @forelse ($pendaftar as $row)
            @php
                $isMasuk = $row->prediksi === 'MASUK';
                $persen = $row->persentaseMasuk();
                $wa = $row->linkWhatsApp();
            @endphp
            <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-4 flex flex-wrap items-center gap-4">
                <div class="flex items-center gap-3 flex-1 min-w-52">
                    <span class="w-1.5 h-10 rounded-full {{ $isMasuk ? 'bg-accent-500' : 'bg-gray-300' }}"></span>
                    <div>
                        <div class="font-bold text-gray-800">{{ $row->nama_pendaftar }}</div>
                        <div class="text-xs text-gray-500">{{ $row->rekomendasiTindakLanjut() }}</div>
                    </div>
                </div>

                <div class="w-44 shrink-0">
                    <div class="flex items-baseline justify-between mb-1">
                        <span class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">Peluang Masuk</span>
                        <span class="text-sm font-bold {{ $isMasuk ? 'text-accent-600' : 'text-gray-500' }}">
                            {{ $persen !== null ? number_format($persen, 1).'%' : '-' }}
                        </span>
                    </div>
                    <div class="h-2 rounded-full bg-gray-100 overflow-hidden">
                        <div class="h-full rounded-full {{ $isMasuk ? 'bg-accent-500' : 'bg-gray-300' }}" style="width: {{ $persen ?? 0 }}%"></div>
                    </div>
                </div>

                <div class="flex items-center gap-3 shrink-0">
                    <span class="px-3 py-1 rounded-full text-xs font-bold {{ $isMasuk ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                        {{ $row->prediksi }}
                    </span>
                    @if ($wa)
                        <a href="{{ $wa }}" target="_blank" rel="noopener"
                           class="px-3.5 py-2 bg-green-500 text-white text-xs font-bold rounded-lg hover:bg-green-600 transition shadow-sm">
                            Hubungi
                        </a>
                    @else
                        <span class="px-3.5 py-2 bg-gray-100 text-gray-400 text-xs font-bold rounded-lg cursor-not-allowed"
                              title="No. HP belum diisi — lengkapi di menu Data Pendaftar">
                            Hubungi
                        </span>
                    @endif
                    <a href="{{ route('klasifikasi.show', $row) }}" class="text-brand-600 text-sm font-medium hover:text-brand-800">Detail</a>
                </div>

                <details class="basis-full border-t border-gray-50 pt-3 -mt-1">
                    <summary class="text-xs font-medium cursor-pointer {{ $row->catatan_tindak_lanjut ? 'text-accent-600' : 'text-gray-400 hover:text-gray-600' }}">
                        {{ $row->catatan_tindak_lanjut ? 'Catatan tindak lanjut (terakhir '.$row->tindak_lanjut_pada?->format('d/m/Y H:i').')' : '+ Tambah catatan tindak lanjut' }}
                    </summary>
                    <form method="POST" action="{{ route('rekomendasi.catatan', $row) }}" class="mt-2 flex items-start gap-2">
                        @csrf
                        <textarea name="catatan_tindak_lanjut" rows="2" required maxlength="1000"
                                  placeholder="Contoh: Sudah dihubungi via WhatsApp 18/07, menunggu konfirmasi pembayaran..."
                                  class="flex-1 rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500 transition">{{ $row->catatan_tindak_lanjut }}</textarea>
                        <button type="submit"
                                class="px-3.5 py-2 bg-brand-600 text-white text-xs font-bold rounded-lg hover:bg-brand-700 transition shrink-0">
                            Simpan
                        </button>
                    </form>
                </details>
            </div>
        @empty
            <p class="text-gray-400 text-sm">
                {{ request()->hasAny(['q', 'prediksi']) ? 'Tidak ada pendaftar yang cocok dengan pencarian.' : 'Belum ada data yang bisa direkomendasikan.' }}
            </p>
        @endforelse
    </div>

    <div class="mt-5">{{ $pendaftar->links() }}</div>
</x-app-layout>
