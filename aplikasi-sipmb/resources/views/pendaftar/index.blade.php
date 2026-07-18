<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Data Pendaftar</h2>
    </x-slot>

    @if ($errors->has('file'))
        <div class="mb-5 px-4 py-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm font-medium">
            {{ $errors->first('file') }}
        </div>
    @endif

    @if (session('import_gagal'))
        <div class="mb-5 px-4 py-3 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm">
            <p class="font-semibold mb-1">Baris yang dilewati saat import:</p>
            <ul class="list-disc ms-5 space-y-0.5">
                @foreach (session('import_gagal') as $pesan)
                    <li>{{ $pesan }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <div class="flex items-center justify-between mb-5 gap-4">
        <form method="GET" class="flex-1 max-w-md">
            <div class="relative">
                <input type="text" name="q" value="{{ request('q') }}" placeholder="Cari nama pendaftar..."
                       class="w-full rounded-lg border-gray-200 bg-white shadow-sm text-sm focus:border-brand-500 focus:ring-brand-500">
            </div>
        </form>
        <div class="shrink-0 flex items-center gap-2">
            <details class="relative">
                <summary class="cursor-pointer list-none px-4 py-2.5 bg-white ring-1 ring-gray-200 text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm">
                    Import Excel/CSV
                </summary>
                <div class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg ring-1 ring-gray-100 p-4 z-10">
                    <form method="POST" action="{{ route('pendaftar.import') }}" enctype="multipart/form-data" class="space-y-3">
                        @csrf
                        <input type="file" name="file" required accept=".xlsx,.xls,.csv"
                               class="block w-full text-sm text-gray-600 file:mr-3 file:px-3 file:py-2 file:rounded-lg file:border-0 file:bg-brand-50 file:text-brand-700 file:text-sm file:font-semibold hover:file:bg-brand-100 file:cursor-pointer">
                        <button type="submit"
                                class="w-full px-4 py-2 bg-brand-600 text-white text-sm font-semibold rounded-lg hover:bg-brand-700 transition">
                            Upload &amp; Import
                        </button>
                        <p class="text-xs text-gray-400 leading-relaxed">
                            Format .xlsx, .xls, atau .csv — baris pertama berisi judul kolom.
                            <a href="{{ route('pendaftar.import.template') }}" class="text-brand-600 hover:underline font-medium">Unduh template</a>
                        </p>
                    </form>
                </div>
            </details>
            <a href="{{ route('pendaftar.create') }}"
               class="px-4 py-2.5 bg-accent-500 text-white text-sm font-semibold rounded-lg hover:bg-accent-600 transition shadow-sm shadow-accent-500/20">
                + Tambah Data
            </a>
        </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm ring-1 ring-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-sm">
                <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-400">
                    <tr>
                        <th class="px-5 py-3 font-semibold">No</th>
                        <th class="px-5 py-3 font-semibold">Nama</th>
                        <th class="px-5 py-3 font-semibold">Jarak</th>
                        <th class="px-5 py-3 font-semibold">Follow Up</th>
                        <th class="px-5 py-3 font-semibold">Status Test</th>
                        <th class="px-5 py-3 font-semibold">Nilai Test</th>
                        <th class="px-5 py-3 font-semibold">Aksi</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    @forelse ($pendaftar as $i => $row)
                        <tr class="hover:bg-gray-50/60">
                            <td class="px-5 py-3 text-gray-500">{{ $pendaftar->firstItem() + $i }}</td>
                            <td class="px-5 py-3 font-medium text-gray-800">{{ $row->nama_pendaftar }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->kategori_jarak_asal }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->tingkat_follow_up_internal }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->status_test }}</td>
                            <td class="px-5 py-3 text-gray-600">{{ $row->kategori_nilai_test }}</td>
                            <td class="px-5 py-3">
                                <div class="flex items-center gap-3">
                                    <a href="{{ route('pendaftar.edit', $row) }}" class="text-brand-600 hover:text-brand-800 font-medium">Edit</a>
                                    <form method="POST" action="{{ route('pendaftar.destroy', $row) }}"
                                          onsubmit="return confirm('Hapus data pendaftar ini?');">
                                        @csrf @method('DELETE')
                                        <button type="submit" class="text-gray-400 hover:text-accent-600 font-medium">Hapus</button>
                                    </form>
                                </div>
                            </td>
                        </tr>
                    @empty
                        <tr><td colspan="7" class="px-5 py-8 text-center text-gray-400">Belum ada data.</td></tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        <div class="px-5 py-4 border-t border-gray-100">
            {{ $pendaftar->links() }}
        </div>
    </div>
</x-app-layout>
