<x-app-layout>
    <x-slot name="header">
        <h2 class="font-bold text-lg text-gray-800">Data Pendaftar</h2>
    </x-slot>

    <div class="flex items-center justify-between mb-5 gap-4">
        <form method="GET" class="flex-1 max-w-md">
            <div class="relative">
                <input type="text" name="q" value="{{ request('q') }}" placeholder="Cari nama pendaftar..."
                       class="w-full rounded-lg border-gray-200 bg-white shadow-sm text-sm focus:border-brand-500 focus:ring-brand-500">
            </div>
        </form>
        <a href="{{ route('pendaftar.create') }}"
           class="shrink-0 px-4 py-2.5 bg-accent-500 text-white text-sm font-semibold rounded-lg hover:bg-accent-600 transition shadow-sm shadow-accent-500/20">
            + Tambah Data
        </a>
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
