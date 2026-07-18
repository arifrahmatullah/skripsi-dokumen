<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Prediksi Data Baru</h2>
    </x-slot>

    @php
        $labelFitur = [
            'kategori_jarak_asal' => 'Kategori Jarak Asal',
            'tingkat_follow_up_internal' => 'Tingkat Follow Up Internal',
            'status_test' => 'Status Test',
            'kategori_nilai_test' => 'Kategori Nilai Test',
            'kategori_penghasilan' => 'Kategori Penghasilan',
        ];
        $options = \App\Services\NaiveBayesService::NILAI_ATRIBUT;
        $selectClass = 'block mt-1.5 w-full rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500 transition';
    @endphp

    @if (! $kesiapan['siap'])
        <div class="mb-5 px-4 py-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm">
            <span class="font-semibold">Model belum siap digunakan.</span>
            {{ $kesiapan['alasan'] }} Lengkapi label "Status Retensi Aktual" pada menu Data Pendaftar terlebih dahulu.
        </div>
    @endif

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {{-- Form input karakteristik --}}
        <form method="POST" action="{{ route('prediksi.prediksi') }}"
              class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7">
            @csrf
            <h3 class="font-bold text-gray-800 mb-1">Karakteristik Calon Mahasiswa</h3>
            <p class="text-xs text-gray-400 mb-5">
                Simulasi prediksi — data yang dimasukkan di sini <span class="font-semibold">tidak disimpan</span> ke database.
            </p>

            <div class="space-y-4">
                @foreach ($labelFitur as $field => $label)
                    <div>
                        <x-input-label for="{{ $field }}" value="{{ $label }}" />
                        <select id="{{ $field }}" name="{{ $field }}" required class="{{ $selectClass }}">
                            <option value="">— Pilih —</option>
                            @foreach ($options[$field] as $val)
                                <option value="{{ $val }}" @selected(old($field, $input[$field] ?? null) === $val)>{{ $val }}</option>
                            @endforeach
                        </select>
                        <x-input-error :messages="$errors->get($field)" class="mt-1" />
                    </div>
                @endforeach
            </div>

            <div class="mt-6">
                <x-primary-button :disabled="! $kesiapan['siap']">Jalankan Prediksi</x-primary-button>
            </div>
        </form>

        {{-- Hasil prediksi --}}
        <div class="space-y-4">
            @if ($hasil)
                @php $isMasuk = $hasil['prediksi'] === 'MASUK'; @endphp
                <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-bold text-gray-800">Hasil Prediksi</h3>
                        <span class="px-3 py-1 rounded-full text-xs font-bold {{ $isMasuk ? 'bg-accent-100 text-accent-700' : 'bg-gray-100 text-gray-500' }}">
                            {{ $hasil['prediksi'] }}
                        </span>
                    </div>

                    <div class="mb-4">
                        <div class="flex items-baseline justify-between mb-1">
                            <span class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">Peluang Masuk</span>
                            <span class="text-2xl font-bold {{ $isMasuk ? 'text-accent-600' : 'text-gray-500' }}">
                                {{ number_format($hasil['persen_masuk'], 1) }}%
                            </span>
                        </div>
                        <div class="h-2.5 rounded-full bg-gray-100 overflow-hidden">
                            <div class="h-full rounded-full {{ $isMasuk ? 'bg-accent-500' : 'bg-gray-300' }}"
                                 style="width: {{ $hasil['persen_masuk'] }}%"></div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-3 text-sm mb-4">
                        <div class="bg-gray-50 rounded-lg p-3">
                            <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">P(MASUK|X)</div>
                            <div class="font-mono text-xs font-bold text-gray-700">{{ number_format($hasil['prob_masuk'], 8) }}</div>
                        </div>
                        <div class="bg-gray-50 rounded-lg p-3">
                            <div class="text-[11px] uppercase tracking-wide text-gray-400 font-semibold">P(TIDAK MASUK|X)</div>
                            <div class="font-mono text-xs font-bold text-gray-700">{{ number_format($hasil['prob_tidak_masuk'], 8) }}</div>
                        </div>
                    </div>

                    <p class="text-sm text-gray-600">
                        Rekomendasi tindak lanjut:
                        <span class="font-semibold text-gray-800">
                            {{ $isMasuk ? 'Prioritas Tinggi - Segera hubungi' : 'Prioritas Rendah - Follow up lanjutan' }}
                        </span>
                    </p>
                    <p class="text-xs text-gray-400 mt-2">Model dilatih dari {{ $hasil['n_train'] }} data historis berlabel.</p>
                </div>

                {{-- Rincian perhitungan --}}
                <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden">
                    <div class="px-5 py-4 border-b border-gray-100">
                        <h3 class="font-bold text-gray-800">Rincian Perhitungan Naive Bayes</h3>
                        <p class="text-xs text-gray-400">P(Y|X) &prop; P(Y) &times; &prod; P(x<sub>i</sub>|Y)</p>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm">
                            <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-400">
                                <tr>
                                    <th class="px-5 py-2.5 font-semibold">Komponen</th>
                                    <th class="px-5 py-2.5 font-semibold">MASUK</th>
                                    <th class="px-5 py-2.5 font-semibold">TIDAK MASUK</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-50">
                                <tr>
                                    <td class="px-5 py-2.5 text-gray-600">Prior P(Y)</td>
                                    <td class="px-5 py-2.5 font-mono text-xs text-gray-700">{{ number_format($hasil['breakdown']['MASUK']['prior'], 6) }}</td>
                                    <td class="px-5 py-2.5 font-mono text-xs text-gray-700">{{ number_format($hasil['breakdown']['TIDAK MASUK']['prior'], 6) }}</td>
                                </tr>
                                @foreach ($labelFitur as $field => $label)
                                    <tr>
                                        <td class="px-5 py-2.5 text-gray-600">
                                            P({{ $label }} = <span class="font-medium text-gray-800">{{ $input[$field] }}</span> | Y)
                                        </td>
                                        <td class="px-5 py-2.5 font-mono text-xs text-gray-700">{{ number_format($hasil['breakdown']['MASUK'][$field], 6) }}</td>
                                        <td class="px-5 py-2.5 font-mono text-xs text-gray-700">{{ number_format($hasil['breakdown']['TIDAK MASUK'][$field], 6) }}</td>
                                    </tr>
                                @endforeach
                                <tr class="bg-gray-50 font-semibold">
                                    <td class="px-5 py-2.5 text-gray-800">Hasil perkalian P(Y|X)</td>
                                    <td class="px-5 py-2.5 font-mono text-xs {{ $isMasuk ? 'text-accent-600' : 'text-gray-700' }}">{{ number_format($hasil['prob_masuk'], 8) }}</td>
                                    <td class="px-5 py-2.5 font-mono text-xs {{ ! $isMasuk ? 'text-brand-700' : 'text-gray-700' }}">{{ number_format($hasil['prob_tidak_masuk'], 8) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            @else
                <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7 text-center text-sm text-gray-400">
                    Pilih karakteristik calon mahasiswa di samping, lalu klik
                    <span class="font-semibold text-gray-500">Jalankan Prediksi</span> untuk melihat hasil klasifikasi
                    beserta rincian perhitungan probabilitasnya.
                </div>
            @endif
        </div>
    </div>
</x-app-layout>
