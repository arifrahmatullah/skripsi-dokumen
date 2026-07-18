<?php

namespace App\Services;

use App\Models\Pendaftar;
use Illuminate\Support\Collection;

class NaiveBayesService
{
    public const KELAS = ['MASUK', 'TIDAK MASUK'];

    /**
     * Syarat minimal data training agar estimasi probabilitas Naive Bayes
     * layak dihitung: jumlah data berlabel dan keterwakilan kedua kelas.
     */
    public const MIN_DATA_TRAINING = 10;

    public const NILAI_ATRIBUT = [
        'kategori_jarak_asal' => ['Dekat', 'Sedang', 'Jauh'],
        'tingkat_follow_up_internal' => ['Belum Dihubungi', 'Kontak Awal', 'Follow Up', 'Follow Up Intensif'],
        'status_test' => ['Belum Tes', 'Sudah Tes'],
        'kategori_nilai_test' => ['Tidak Ada Nilai', 'Nilai Sedang', 'Nilai Tinggi'],
        'kategori_penghasilan' => [
            'Tidak Diketahui', 'Dibawah Rp.1.000.000', 'Rp.1.000.000 - Rp.2.000.000',
            'Rp.2.000.001 - Rp.4.000.000', 'Rp.4.000.001 - Rp.6.000.000', 'Diatas Rp.6.000.000',
        ],
    ];

    /**
     * Periksa apakah data berlabel sudah memenuhi karakteristik yang
     * dibutuhkan algoritma Naive Bayes: jumlah minimal terpenuhi dan
     * kedua kelas terwakili. Jika belum, probabilitas tidak dihitung.
     */
    public function statusKesiapan(): array
    {
        $labeled = Pendaftar::whereNotNull('status_retensi_final_target');
        $nMasuk = (clone $labeled)->where('status_retensi_final_target', 'MASUK')->count();
        $nTidakMasuk = (clone $labeled)->where('status_retensi_final_target', 'TIDAK MASUK')->count();
        $n = $nMasuk + $nTidakMasuk;

        $alasan = null;
        if ($n < self::MIN_DATA_TRAINING) {
            $alasan = 'Jumlah data training berlabel baru '.$n.' dari minimal '.self::MIN_DATA_TRAINING.' data.';
        } elseif ($nMasuk === 0 || $nTidakMasuk === 0) {
            $alasan = 'Data training hanya memuat satu kelas ('.($nMasuk === 0 ? 'TIDAK MASUK' : 'MASUK').' saja), padahal Naive Bayes membutuhkan contoh dari kedua kelas.';
        }

        return [
            'siap' => $alasan === null,
            'alasan' => $alasan,
            'n_berlabel' => $n,
            'n_masuk' => $nMasuk,
            'n_tidak_masuk' => $nTidakMasuk,
            'minimal' => self::MIN_DATA_TRAINING,
        ];
    }

    /**
     * Pastikan seluruh atribut fitur terisi dengan nilai kategori yang
     * dikenal model sebelum baris data ikut diprediksi.
     */
    public function fiturLengkap(Pendaftar $row): bool
    {
        foreach (Pendaftar::FITUR as $f) {
            if (! in_array($row->{$f}, self::NILAI_ATRIBUT[$f], true)) {
                return false;
            }
        }

        return true;
    }

    /**
     * Hitung prior probability & conditional probability (Laplace smoothing)
     * dari kumpulan data training berlabel.
     */
    public function train(Collection $rows): array
    {
        $nTrain = $rows->count();

        $prior = [];
        foreach (self::KELAS as $k) {
            $prior[$k] = $rows->where('status_retensi_final_target', $k)->count();
        }

        $cond = [];
        foreach (Pendaftar::FITUR as $f) {
            $uniqueVals = self::NILAI_ATRIBUT[$f];
            $K = count($uniqueVals);
            $cond[$f] = [];
            foreach (self::KELAS as $k) {
                $sub = $rows->where('status_retensi_final_target', $k);
                $nK = $sub->count();
                $cond[$f][$k] = [];
                foreach ($uniqueVals as $v) {
                    $ni = $sub->where($f, $v)->count();
                    $cond[$f][$k][$v] = ($ni + 1) / ($nK + $K);
                }
            }
        }

        return ['n_train' => $nTrain, 'prior' => $prior, 'cond' => $cond];
    }

    /**
     * Hitung posterior probability P(Y|X) untuk satu baris data.
     */
    public function predict(array $model, Pendaftar $row): array
    {
        $scores = [];
        $breakdown = [];
        foreach (self::KELAS as $k) {
            $nK = $model['prior'][$k];
            $p = $nK / max($model['n_train'], 1);
            $parts = ['prior' => $p];
            foreach (Pendaftar::FITUR as $f) {
                $v = $row->{$f};
                $K = count(self::NILAI_ATRIBUT[$f]);
                $prob = $model['cond'][$f][$k][$v] ?? (1 / ($nK + $K));
                $parts[$f] = $prob;
                $p *= $prob;
            }
            $scores[$k] = $p;
            $breakdown[$k] = $parts;
        }

        $pred = $scores['MASUK'] >= $scores['TIDAK MASUK'] ? 'MASUK' : 'TIDAK MASUK';

        return [
            'prob_masuk' => $scores['MASUK'],
            'prob_tidak_masuk' => $scores['TIDAK MASUK'],
            'prediksi' => $pred,
            'breakdown' => $breakdown,
        ];
    }

    /**
     * Latih model dari seluruh data historis berlabel, lalu terapkan
     * prediksi ke SELURUH data pendaftar (historis + baru) dan simpan hasilnya.
     */
    public function classifyAll(): array
    {
        $kesiapan = $this->statusKesiapan();

        if (! $kesiapan['siap']) {
            Pendaftar::query()->update([
                'prob_masuk' => null,
                'prob_tidak_masuk' => null,
                'prediksi' => null,
                'predicted_at' => null,
            ]);

            return ['siap' => false, 'alasan' => $kesiapan['alasan'], 'n_model' => $kesiapan['n_berlabel'], 'n_classified' => 0];
        }

        $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();
        $model = $this->train($labeled);

        $terklasifikasi = 0;
        foreach (Pendaftar::all() as $row) {
            if (! $this->fiturLengkap($row)) {
                $row->update([
                    'prob_masuk' => null,
                    'prob_tidak_masuk' => null,
                    'prediksi' => null,
                    'predicted_at' => null,
                ]);
                continue;
            }

            $result = $this->predict($model, $row);
            $row->update([
                'prob_masuk' => $result['prob_masuk'],
                'prob_tidak_masuk' => $result['prob_tidak_masuk'],
                'prediksi' => $result['prediksi'],
                'predicted_at' => now(),
            ]);
            $terklasifikasi++;
        }

        return ['siap' => true, 'alasan' => null, 'n_model' => $model['n_train'], 'n_classified' => $terklasifikasi];
    }

    /**
     * Split data historis 80/20 stratified (seeded), latih di 80%, uji di 20%,
     * lalu hitung confusion matrix & metrik evaluasi (replikasi metodologi Bab 4).
     */
    public function evaluate(float $testSize = 0.2, int $seed = 42): array
    {
        $labeled = Pendaftar::whereNotNull('status_retensi_final_target')->get();

        mt_srand($seed);
        $train = collect();
        $test = collect();

        foreach ($labeled->groupBy('status_retensi_final_target') as $rows) {
            $shuffled = $rows->values()->all();
            for ($i = count($shuffled) - 1; $i > 0; $i--) {
                $j = mt_rand(0, $i);
                [$shuffled[$i], $shuffled[$j]] = [$shuffled[$j], $shuffled[$i]];
            }
            $nTest = (int) round(count($shuffled) * $testSize);
            $test = $test->concat(array_slice($shuffled, 0, $nTest));
            $train = $train->concat(array_slice($shuffled, $nTest));
        }

        $model = $this->train($train);

        $tp = $tn = $fp = $fn = 0;
        foreach ($test as $row) {
            $pred = $this->predict($model, $row)['prediksi'];
            $actual = $row->status_retensi_final_target;
            if ($pred === 'MASUK' && $actual === 'MASUK') {
                $tp++;
            } elseif ($pred === 'TIDAK MASUK' && $actual === 'TIDAK MASUK') {
                $tn++;
            } elseif ($pred === 'MASUK' && $actual === 'TIDAK MASUK') {
                $fp++;
            } else {
                $fn++;
            }
        }

        $total = $tp + $tn + $fp + $fn;
        $acc = $total > 0 ? round(($tp + $tn) / $total * 100, 2) : 0.0;
        $prec = ($tp + $fp) > 0 ? round($tp / ($tp + $fp) * 100, 2) : 0.0;
        $rec = ($tp + $fn) > 0 ? round($tp / ($tp + $fn) * 100, 2) : 0.0;
        $f1 = ($prec + $rec) > 0 ? round(2 * $prec * $rec / ($prec + $rec), 2) : 0.0;

        return [
            'n_train' => $train->count(), 'n_test' => $test->count(),
            'tp' => $tp, 'tn' => $tn, 'fp' => $fp, 'fn' => $fn,
            'acc' => $acc, 'prec' => $prec, 'rec' => $rec, 'f1' => $f1,
        ];
    }
}
