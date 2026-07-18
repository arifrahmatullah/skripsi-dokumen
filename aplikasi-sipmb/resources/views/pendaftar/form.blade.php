<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">
            {{ $pendaftar->exists ? 'Ubah Data Pendaftar' : 'Tambah Data Pendaftar' }}
        </h2>
    </x-slot>

    @php
        $options = \App\Services\NaiveBayesService::NILAI_ATRIBUT;
        $asalSekolah = ['Sekolah Negeri', 'Sekolah Swasta', 'Sekolah Madrasah', 'Pondok Pesantren'];
        $waktu = ['Awal Gelombang', 'Tengah Gelombang', 'Akhir Gelombang'];
        $uangPendaftaran = ['Belum Lunas', 'Lunas'];
        $target = ['MASUK', 'TIDAK MASUK'];
        $selectClass = 'block mt-1.5 w-full rounded-lg border-gray-200 bg-gray-50 text-sm focus:border-brand-500 focus:bg-white focus:ring-brand-500 transition';
    @endphp

    <form method="POST"
          action="{{ $pendaftar->exists ? route('pendaftar.update', $pendaftar) : route('pendaftar.store') }}"
          class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 p-7 max-w-3xl">
        @csrf
        @if ($pendaftar->exists) @method('PUT') @endif

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="md:col-span-2">
                <x-input-label for="nama_pendaftar" value="Nama Pendaftar" />
                <x-text-input id="nama_pendaftar" name="nama_pendaftar" class="block mt-1.5 w-full"
                              :value="old('nama_pendaftar', $pendaftar->nama_pendaftar)" required />
                <x-input-error :messages="$errors->get('nama_pendaftar')" class="mt-1" />
            </div>

            <div>
                <x-input-label for="prodi" value="Program Studi" />
                <x-text-input id="prodi" name="prodi" class="block mt-1.5 w-full"
                              :value="old('prodi', $pendaftar->prodi)" />
            </div>

            <div>
                <x-input-label for="asal_kota" value="Asal Kota" />
                <x-text-input id="asal_kota" name="asal_kota" class="block mt-1.5 w-full"
                              :value="old('asal_kota', $pendaftar->asal_kota)" />
            </div>

            <div>
                <x-input-label for="no_hp" value="No. HP / WhatsApp" />
                <x-text-input id="no_hp" name="no_hp" class="block mt-1.5 w-full" placeholder="08xxxxxxxxxx"
                              :value="old('no_hp', $pendaftar->no_hp)" />
                <x-input-error :messages="$errors->get('no_hp')" class="mt-1" />
            </div>

            @foreach ([
                'kategori_jarak_asal' => 'Kategori Jarak Asal',
                'tingkat_follow_up_internal' => 'Tingkat Follow Up Internal',
                'status_test' => 'Status Test',
                'kategori_nilai_test' => 'Kategori Nilai Test',
                'kategori_penghasilan' => 'Kategori Penghasilan',
            ] as $field => $label)
                <div>
                    <x-input-label for="{{ $field }}" value="{{ $label }}" />
                    <select id="{{ $field }}" name="{{ $field }}" required class="{{ $selectClass }}">
                        <option value="">— Pilih —</option>
                        @foreach ($options[$field] as $val)
                            <option value="{{ $val }}" @selected(old($field, $pendaftar->$field) === $val)>{{ $val }}</option>
                        @endforeach
                    </select>
                    <x-input-error :messages="$errors->get($field)" class="mt-1" />
                </div>
            @endforeach

            <div>
                <x-input-label for="kategori_asal_sekolah" value="Kategori Asal Sekolah" />
                <select id="kategori_asal_sekolah" name="kategori_asal_sekolah" class="{{ $selectClass }}">
                    <option value="">— Pilih —</option>
                    @foreach ($asalSekolah as $val)
                        <option value="{{ $val }}" @selected(old('kategori_asal_sekolah', $pendaftar->kategori_asal_sekolah) === $val)>{{ $val }}</option>
                    @endforeach
                </select>
            </div>

            <div>
                <x-input-label for="waktu_pendaftaran" value="Waktu Pendaftaran" />
                <select id="waktu_pendaftaran" name="waktu_pendaftaran" class="{{ $selectClass }}">
                    <option value="">— Pilih —</option>
                    @foreach ($waktu as $val)
                        <option value="{{ $val }}" @selected(old('waktu_pendaftaran', $pendaftar->waktu_pendaftaran) === $val)>{{ $val }}</option>
                    @endforeach
                </select>
            </div>

            <div>
                <x-input-label for="status_uang_pendaftaran" value="Status Uang Pendaftaran" />
                <select id="status_uang_pendaftaran" name="status_uang_pendaftaran" class="{{ $selectClass }}">
                    <option value="">— Pilih —</option>
                    @foreach ($uangPendaftaran as $val)
                        <option value="{{ $val }}" @selected(old('status_uang_pendaftaran', $pendaftar->status_uang_pendaftaran) === $val)>{{ $val }}</option>
                    @endforeach
                </select>
            </div>

            <div>
                <x-input-label for="status_retensi_final_target" value="Status Retensi Aktual (jika sudah diketahui)" />
                <select id="status_retensi_final_target" name="status_retensi_final_target" class="{{ $selectClass }}">
                    <option value="">Belum diketahui</option>
                    @foreach ($target as $val)
                        <option value="{{ $val }}" @selected(old('status_retensi_final_target', $pendaftar->status_retensi_final_target) === $val)>{{ $val }}</option>
                    @endforeach
                </select>
                <p class="text-xs text-gray-400 mt-1.5">Diisi setelah calon mahasiswa dipastikan konfirmasi (MASUK) atau tidak (TIDAK MASUK). Data ini menjadi label training model.</p>
            </div>
        </div>

        <div class="mt-7 flex gap-3">
            <x-primary-button>Simpan</x-primary-button>
            <a href="{{ route('pendaftar.index') }}" class="px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition">
                Batal
            </a>
        </div>
    </form>
</x-app-layout>
