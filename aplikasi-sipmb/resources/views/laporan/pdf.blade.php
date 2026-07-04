<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: sans-serif; font-size: 11px; color: #111; }
        h2 { margin-bottom: 2px; }
        p.sub { margin-top: 0; color: #555; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { border: 1px solid #999; padding: 5px 7px; text-align: left; }
        th { background: #D0D8E8; }
        tr.alt { background: #F7F9FC; }
        .badge { padding: 2px 6px; border-radius: 3px; color: #fff; font-weight: bold; font-size: 10px; }
        .masuk { background: #2E9E5B; }
        .tidak { background: #9AA3AF; }
    </style>
</head>
<body>
    <h2>Laporan Rekomendasi Tindak Lanjut Konfirmasi Pendaftaran</h2>
    <p class="sub">
        SI-PMB Universitas Tazkia &mdash; dicetak {{ now()->format('d-m-Y H:i') }}
        @if ($totalTersedia > $pendaftar->count())
            &mdash; menampilkan {{ $pendaftar->count() }} dari {{ $totalTersedia }} data (gunakan filter atau Export Excel untuk data lengkap)
        @endif
    </p>

    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Nama Pendaftar</th>
                <th>Kategori Jarak</th>
                <th>Status Test</th>
                <th>Nilai Test</th>
                <th>P(MASUK|X)</th>
                <th>Prediksi</th>
                <th>Rekomendasi</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($pendaftar as $i => $row)
                <tr class="{{ $i % 2 ? 'alt' : '' }}">
                    <td>{{ $i + 1 }}</td>
                    <td>{{ $row->nama_pendaftar }}</td>
                    <td>{{ $row->kategori_jarak_asal }}</td>
                    <td>{{ $row->status_test }}</td>
                    <td>{{ $row->kategori_nilai_test }}</td>
                    <td>{{ number_format($row->prob_masuk, 6) }}</td>
                    <td><span class="badge {{ $row->prediksi === 'MASUK' ? 'masuk' : 'tidak' }}">{{ $row->prediksi }}</span></td>
                    <td>{{ $row->rekomendasiTindakLanjut() }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
