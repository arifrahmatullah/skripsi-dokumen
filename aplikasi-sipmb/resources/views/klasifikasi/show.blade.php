<x-app-layout>
    <x-slot name="header">
        <div class="flex items-center gap-3">
            <a href="{{ route('klasifikasi.index') }}" class="px-3 py-1.5 border border-gray-200 text-gray-600 text-sm font-medium rounded-lg hover:bg-gray-50 transition">
                &larr; Kembali
            </a>
            <h2 class="font-bold text-lg text-gray-800">
                Detail Prediksi &mdash; {{ $pendaftar->nama_pendaftar }}
            </h2>
        </div>
    </x-slot>

    @php
        $labelAtribut = [
            'kategori_jarak_asal' => 'Kategori Jarak Asal',
            'tingkat_follow_up_internal' => 'Tingkat Follow Up',
            'status_test' => 'Status Test',
            'kategori_nilai_test' => 'Kategori Nilai Test',
            'kategori_penghasilan' => 'Kategori Penghasilan',
        ];
        $kelasUtama = $result['prediksi'];
        $breakdown = $result['breakdown'][$kelasUtama];
        $isMasuk = $kelasUtama === 'MASUK';
    @endphp

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7">
            <h3 class="font-bold text-sm text-gray-800 mb-4">Atribut Pendaftar</h3>
            <ul class="text-sm space-y-2 mb-7">
                @foreach ($labelAtribut as $field => $label)
                    <li class="flex justify-between border-b border-dashed border-gray-100 pb-2">
                        <span class="text-gray-500">{{ $label }}</span>
                        <span class="font-semibold text-gray-800">{{ $pendaftar->$field }}</span>
                    </li>
                @endforeach
            </ul>

            <h3 class="font-bold text-sm text-gray-800 mb-4">
                Rincian Probabilitas &mdash; Kelas {{ $kelasUtama }}
            </h3>
            <div class="space-y-4">
                @php $priorPct = min($breakdown['prior'] * 100, 100); @endphp
                <div>
                    <div class="flex justify-between text-xs mb-1.5"><span class="text-gray-500">Prior P({{ $kelasUtama }})</span><span class="font-semibold text-gray-700">{{ number_format($breakdown['prior'] * 100, 2) }}%</span></div>
                    <div class="h-2 rounded-full bg-gray-100"><div class="h-2 rounded-full bg-brand-500" style="width: {{ $priorPct }}%"></div></div>
                </div>
                @foreach ($labelAtribut as $field => $label)
                    @php $pct = min($breakdown[$field] * 100, 100); @endphp
                    <div>
                        <div class="flex justify-between text-xs mb-1.5">
                            <span class="text-gray-500">P({{ $label }}={{ $pendaftar->$field }} | {{ $kelasUtama }})</span>
                            <span class="font-semibold text-gray-700">{{ number_format($breakdown[$field] * 100, 2) }}%</span>
                        </div>
                        <div class="h-2 rounded-full bg-gray-100"><div class="h-2 rounded-full bg-brand-500" style="width: {{ $pct }}%"></div></div>
                    </div>
                @endforeach
                <div class="pt-2">
                    <div class="flex justify-between text-xs mb-1.5 font-bold">
                        <span class="text-gray-700">Posterior P({{ $kelasUtama }}|X)</span>
                        <span class="text-accent-600">{{ number_format(($isMasuk ? $result['prob_masuk'] : $result['prob_tidak_masuk']) * 100, 4) }}%</span>
                    </div>
                    <div class="h-2.5 rounded-full bg-gray-100">
                        <div class="h-2.5 rounded-full bg-accent-500" style="width: {{ min(($isMasuk ? $result['prob_masuk'] : $result['prob_tidak_masuk']) * 100, 100) }}%"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7 text-center h-fit">
            <div class="px-4 py-4 rounded-xl {{ $isMasuk ? 'bg-accent-500' : 'bg-gray-400' }}">
                <div class="text-white/80 text-[11px] uppercase tracking-wide font-semibold mb-1">Prediksi</div>
                <div class="text-white font-bold text-lg">{{ $result['prediksi'] }}</div>
            </div>
            <dl class="mt-5 text-sm text-left space-y-2">
                <div class="flex justify-between"><dt class="text-gray-500">P(MASUK|X)</dt><dd class="font-mono text-xs font-semibold text-gray-800">{{ number_format($result['prob_masuk'], 8) }}</dd></div>
                <div class="flex justify-between"><dt class="text-gray-500">P(TIDAK MASUK|X)</dt><dd class="font-mono text-xs font-semibold text-gray-800">{{ number_format($result['prob_tidak_masuk'], 8) }}</dd></div>
            </dl>
        </div>
    </div>
</x-app-layout>
