import sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

shutil.copy('SUSUN-SKRIPSI-ARIF.docx', 'SUSUN-SKRIPSI-ARIF_BACKUP.docx')
doc = Document('SUSUN-SKRIPSI-ARIF.docx')

# Hapus paragraf 514-516
for idx in [516, 515, 514]:
    el = doc.paragraphs[idx]._element
    el.getparent().remove(el)

cur = doc.paragraphs[513]._element
TNR = 'Times New Roman'

def p(text, bold=False, italic=False, center=False, size=12, after=None, ind=0):
    new_p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    s = OxmlElement('w:pStyle')
    s.set(qn('w:val'), 'ListParagraph')
    pPr.append(s)
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center' if center else 'both')
    pPr.append(jc)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), '0')
    sp.set(qn('w:after'), '0')
    sp.set(qn('w:line'), '480')
    sp.set(qn('w:lineRule'), 'auto')
    pPr.append(sp)
    if ind > 0:
        i2 = OxmlElement('w:ind')
        i2.set(qn('w:left'), str(int(ind * 567)))
        pPr.append(i2)
    new_p.append(pPr)
    if text:
        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:ascii'), TNR)
        rf.set(qn('w:hAnsi'), TNR)
        rPr.append(rf)
        if bold:
            rPr.append(OxmlElement('w:b'))
        if italic:
            rPr.append(OxmlElement('w:i'))
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(size * 2))
        rPr.append(sz)
        szcs = OxmlElement('w:szCs')
        szcs.set(qn('w:val'), str(size * 2))
        rPr.append(szcs)
        r.append(rPr)
        t = OxmlElement('w:t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
        r.append(t)
        new_p.append(r)
    ref = after if after is not None else cur
    ref.addnext(new_p)
    return new_p


def make_tbl(rows_data, hdr_rows=1):
    nc = max(len(r) for r in rows_data)
    tbl = doc.add_table(rows=len(rows_data), cols=nc)
    tbl.style = 'Table Grid'
    for ri, row in enumerate(rows_data):
        for ci, cell_info in enumerate(row):
            if isinstance(cell_info, dict):
                txt = cell_info.get('t', '')
                bold = cell_info.get('b', ri < hdr_rows)
                left = cell_info.get('l', False)
            else:
                txt = str(cell_info)
                bold = ri < hdr_rows
                left = False
            cell = tbl.cell(ri, ci)
            cell.text = ''
            pp = cell.paragraphs[0]
            pp.alignment = WD_ALIGN_PARAGRAPH.LEFT if left else WD_ALIGN_PARAGRAPH.CENTER
            run = pp.add_run(txt)
            run.bold = bold
            run.font.name = TNR
            run.font.size = Pt(10)
            if ri < hdr_rows:
                tc = cell._element
                tcPr = tc.find(qn('w:tcPr'))
                if tcPr is None:
                    tcPr = OxmlElement('w:tcPr')
                    tc.insert(0, tcPr)
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), 'D9D9D9')
                tcPr.append(shd)
    el = tbl._element
    el.getparent().remove(el)
    return el


def ins_tbl(after_el, rows_data, caption, source='Hasil Pengolahan Data (2025)', hdr_rows=1):
    c = p(caption, bold=True, center=True, after=after_el)
    tbl_el = make_tbl(rows_data, hdr_rows)
    c.addnext(tbl_el)
    s = p('Sumber: ' + source, italic=True, center=True, after=tbl_el)
    e = p('', after=s)
    return e


def tbl_cond(rows, caption):
    HDR = ['Nilai', 'Jml MASUK', 'Jml TDK MSK', 'P(X|MASUK)', 'P(X|TDK MSK)', 'Hasil MASUK', 'Hasil TDK MSK']
    d = [HDR]
    for r in rows:
        d.append([{'t': r[0], 'l': True}, r[1], r[2], r[3], r[4], r[5], r[6]])
    return d, caption


# ===========================================================================
# ISI KONTEN
# ===========================================================================

cur = p('Metode yang diterapkan dalam proses penelitian ini menggunakan algoritma Naive Bayes. Metode ini diharapkan dapat menghasilkan rekomendasi tindak lanjut konfirmasi pendaftaran mahasiswa baru secara efektif dan akurat. Berikut adalah beberapa langkah dengan pendekatan algoritma Naive Bayes:', after=cur)

# --- a. Menyiapkan Dataset ---
cur = p('a.  Menyiapkan Dataset', bold=True, after=cur)
cur = p('Pada langkah ini dilakukan pengumpulan data historis pendaftaran mahasiswa baru Universitas Tazkia. Data sampel dibagi menjadi 70% untuk data training (15 data) dan 30% untuk data testing (1 data). Berikut adalah dataset untuk data training dan testing pada Tabel 4.1 dan Tabel 4.2.', after=cur)

tbl_tr = [
    ['No', 'Nama', 'Kat. Jarak', 'Follow Up', 'Status Test', 'Nilai Test', 'Penghasilan', 'Kelas'],
    ['1', {'t': 'Jihad Muhammad Akbar', 'l': True}, 'Dekat', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Rp2jt-Rp4jt', 'l': True}, 'MASUK'],
    ['2', {'t': 'Ghaitsa Witanya G.', 'l': True}, 'Dekat', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': '> Rp6jt', 'l': True}, 'MASUK'],
    ['3', {'t': 'ULIL AMRI SIDDIK', 'l': True}, 'Jauh', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Rp2jt-Rp4jt', 'l': True}, 'MASUK'],
    ['4', {'t': 'Akmal Syawqi Albar', 'l': True}, 'Sedang', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Tdk Diketahui', 'l': True}, 'MASUK'],
    ['5', {'t': "Naysella Robi'atul A.", 'l': True}, 'Jauh', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Sedang', {'t': '> Rp6jt', 'l': True}, 'MASUK'],
    ['6', {'t': 'Ayu Nabila', 'l': True}, 'Jauh', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Tdk Diketahui', 'l': True}, 'MASUK'],
    ['7', {'t': 'Alya Adibah', 'l': True}, 'Jauh', 'Kontak Awal', 'Sudah Tes', 'Nilai Tinggi', {'t': '> Rp6jt', 'l': True}, 'MASUK'],
    ['8', {'t': 'Test Rudie', 'l': True}, 'Jauh', 'Belum Dihubungi', 'Belum Tes', 'Tdk Ada Nilai', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['9', {'t': 'Sayidatus Sajil H.', 'l': True}, 'Sedang', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['10', {'t': 'Khalid AlMarzuq', 'l': True}, 'Jauh', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Sedang', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['11', {'t': 'Rizal Trenggoni', 'l': True}, 'Dekat', 'Belum Dihubungi', 'Belum Tes', 'Tdk Ada Nilai', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['12', {'t': 'Siti Khofifah', 'l': True}, 'Sedang', 'Follow Up Intensif', 'Belum Tes', 'Tdk Ada Nilai', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['13', {'t': 'MOHAMMAD SYAHRONI', 'l': True}, 'Jauh', 'Follow Up', 'Belum Tes', 'Tdk Ada Nilai', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['14', {'t': 'Muhamad Najhan A.F.', 'l': True}, 'Sedang', 'Follow Up', 'Belum Tes', 'Tdk Ada Nilai', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
    ['15', {'t': 'Susilo Wardoyo', 'l': True}, 'Jauh', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': 'Tdk Diketahui', 'l': True}, 'TDK MASUK'],
]
cur = ins_tbl(cur, tbl_tr, 'Tabel 4.1 Dataset Untuk Data Training', 'Data Internal Pendaftaran Universitas Tazkia')

tbl_te = [
    ['No', 'Nama', 'Kat. Jarak', 'Follow Up', 'Status Test', 'Nilai Test', 'Penghasilan', 'Prediksi'],
    ['1', {'t': 'Kaisa Qomaru Zayyan', 'l': True}, 'Dekat', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', {'t': '> Rp6jt', 'l': True}, '?'],
]
cur = ins_tbl(cur, tbl_te, 'Tabel 4.2 Dataset Untuk Data Testing', 'Data Internal Pendaftaran Universitas Tazkia')

# --- b. Pre-processing ---
cur = p('b.  Pre-processing Data', bold=True, after=cur)
cur = p('Pada langkah ini dilakukan pre-processing atau mempersiapkan data sebelum digunakan dalam algoritma Naive Bayes melalui pembersihan data dan seleksi fitur.', after=cur)
cur = p('1)  Pembersihan Data', bold=True, after=cur, ind=1)
cur = p('Dilakukan pemeriksaan terhadap data yang memiliki nilai kosong (missing value) atau tidak relevan (noise). Berdasarkan hasil pemeriksaan, data pada Tabel 4.1 dan Tabel 4.2 tidak ditemukan nilai kosong sehingga seluruh data dapat langsung digunakan.', after=cur)
cur = p('2)  Seleksi Fitur', bold=True, after=cur, ind=1)
cur = p('Seleksi fitur dilakukan untuk memilih atribut yang akan digunakan dalam proses klasifikasi. Hasil seleksi fitur dapat dilihat pada tabel berikut.', after=cur)

tbl_f = [
    ['Fitur/Atribut yang Ada Sebelumnya', 'Fitur/Atribut yang Digunakan'],
    [{'t': 'Kategori Jarak Asal', 'l': True}, {'t': 'Kategori Jarak Asal', 'l': True}],
    [{'t': 'Kategori Asal Sekolah', 'l': True}, {'t': '- (tidak digunakan)', 'l': True}],
    [{'t': 'Waktu Pendaftaran', 'l': True}, {'t': '- (tidak digunakan)', 'l': True}],
    [{'t': 'Tingkat Follow Up Internal', 'l': True}, {'t': 'Tingkat Follow Up Internal', 'l': True}],
    [{'t': 'Status Uang Pendaftaran', 'l': True}, {'t': '- (tidak digunakan)', 'l': True}],
    [{'t': 'Status Test', 'l': True}, {'t': 'Status Test', 'l': True}],
    [{'t': 'Kategori Nilai Test', 'l': True}, {'t': 'Kategori Nilai Test', 'l': True}],
    [{'t': 'Kategori Penghasilan', 'l': True}, {'t': 'Kategori Penghasilan', 'l': True}],
    [{'t': 'Status Retensi Final (Target)', 'l': True}, {'t': 'Status Retensi Final (Target)', 'l': True}],
]
cur = ins_tbl(cur, tbl_f, 'Tabel 4.3 Hasil Seleksi Fitur')

# --- c. Variabel ---
cur = p('c.  Menentukan Variabel Penelitian', bold=True, after=cur)
cur = p('Berdasarkan hasil seleksi fitur, variabel yang digunakan dalam proses klasifikasi Naive Bayes dapat dilihat pada Tabel 4.4.', after=cur)

tbl_v = [
    ['Kode', 'Atribut', 'Tipe', 'Nilai'],
    ['X1', {'t': 'Kategori Jarak Asal', 'l': True}, {'t': 'Variabel Atribut', 'l': True}, {'t': 'Dekat, Sedang, Jauh', 'l': True}],
    ['X2', {'t': 'Tingkat Follow Up Internal', 'l': True}, {'t': 'Variabel Atribut', 'l': True}, {'t': 'Belum Dihubungi, Kontak Awal, Follow Up, Follow Up Intensif', 'l': True}],
    ['X3', {'t': 'Status Test', 'l': True}, {'t': 'Variabel Atribut', 'l': True}, {'t': 'Sudah Tes, Belum Tes', 'l': True}],
    ['X4', {'t': 'Kategori Nilai Test', 'l': True}, {'t': 'Variabel Atribut', 'l': True}, {'t': 'Nilai Tinggi, Nilai Sedang, Tidak Ada Nilai', 'l': True}],
    ['X5', {'t': 'Kategori Penghasilan', 'l': True}, {'t': 'Variabel Atribut', 'l': True}, {'t': 'Di atas Rp6jt, Rp2jt-Rp4jt, Tidak Diketahui', 'l': True}],
    ['Y', {'t': 'Status Retensi Final', 'l': True}, {'t': 'Kelas Target', 'l': True}, {'t': 'MASUK, TIDAK MASUK', 'l': True}],
]
cur = ins_tbl(cur, tbl_v, 'Tabel 4.4 Variabel Penelitian')

# --- d. Prior ---
cur = p('d.  Menghitung Prior Probability', bold=True, after=cur)
cur = p('Pada tahap ini dilakukan perhitungan probabilitas prior atau peluang kemunculan setiap kelas target (Y) yaitu MASUK dan TIDAK MASUK, dihitung berdasarkan data training pada Tabel 4.1 yang berjumlah 15 data.', after=cur)
cur = p('P(Yi) = ni / n', italic=True, center=True, after=cur)
cur = p('P(Y = MASUK)       = 7 / 15 = 0,4667', center=True, after=cur)
cur = p('P(Y = TIDAK MASUK) = 8 / 15 = 0,5333', center=True, after=cur)
cur = p('Berdasarkan hasil perhitungan di atas, hasil perhitungan prior probability dapat dilihat pada Tabel 4.5.', after=cur)

tbl_pr = [
    ['Kelas (Y)', 'Jumlah Kemunculan (ni)', 'P(Y)', 'Hasil'],
    [{'t': 'MASUK', 'l': True}, '7', '7 / 15', '0,4667'],
    [{'t': 'TIDAK MASUK', 'l': True}, '8', '8 / 15', '0,5333'],
    [{'t': 'Total Data (n)', 'b': True, 'l': True}, '15', '', ''],
]
cur = ins_tbl(cur, tbl_pr, 'Tabel 4.5 Hasil Perhitungan Prior Probability')

# --- e. Likelihood ---
cur = p('e.  Menghitung Likelihood (Conditional Probability)', bold=True, after=cur)
cur = p('Pada tahap ini dilakukan perhitungan likelihood atau conditional probability, yaitu probabilitas kemunculan setiap nilai atribut pada masing-masing kelas berdasarkan data training.', after=cur)
cur = p('P(Xi | H) = Jumlah data Xi pada kelas H / Total data kelas H', italic=True, center=True, after=cur)

d, c = tbl_cond([
    ('Dekat', '2', '1', '2/7', '1/8', '0,2857', '0,1250'),
    ('Sedang', '1', '3', '1/7', '3/8', '0,1429', '0,3750'),
    ('Jauh', '4', '4', '4/7', '4/8', '0,5714', '0,5000'),
    ('Total', '7', '8', '', '', '', ''),
], 'Tabel 4.6 Conditional Probability Kategori Jarak Asal')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Belum Dihubungi', '6', '5', '6/7', '5/8', '0,8571', '0,6250'),
    ('Kontak Awal', '1', '0', '1/7', '0/8', '0,1429', '0,0000'),
    ('Follow Up', '0', '2', '0/7', '2/8', '0,0000', '0,2500'),
    ('Follow Up Intensif', '0', '1', '0/7', '1/8', '0,0000', '0,1250'),
    ('Total', '7', '8', '', '', '', ''),
], 'Tabel 4.7 Conditional Probability Tingkat Follow Up Internal')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Sudah Tes', '7', '3', '7/7', '3/8', '1,0000', '0,3750'),
    ('Belum Tes', '0', '5', '0/7', '5/8', '0,0000', '0,6250'),
    ('Total', '7', '8', '', '', '', ''),
], 'Tabel 4.8 Conditional Probability Status Test')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Nilai Tinggi', '6', '2', '6/7', '2/8', '0,8571', '0,2500'),
    ('Nilai Sedang', '1', '1', '1/7', '1/8', '0,1429', '0,1250'),
    ('Tidak Ada Nilai', '0', '5', '0/7', '5/8', '0,0000', '0,6250'),
    ('Total', '7', '8', '', '', '', ''),
], 'Tabel 4.9 Conditional Probability Kategori Nilai Test')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Rp2jt-Rp4jt', '2', '0', '2/7', '0/8', '0,2857', '0,0000'),
    ('Di atas Rp6jt', '3', '0', '3/7', '0/8', '0,4286', '0,0000'),
    ('Tidak Diketahui', '2', '8', '2/7', '8/8', '0,2857', '1,0000'),
    ('Total', '7', '8', '', '', '', ''),
], 'Tabel 4.10 Conditional Probability Kategori Penghasilan')
cur = ins_tbl(cur, d, c)

# --- f. Posterior ---
cur = p('f.  Menghitung Posterior Probability', bold=True, after=cur)
cur = p('Pada tahapan ini dilakukan perhitungan posterior probability untuk memprediksi kelas Y berdasarkan data testing pada Tabel 4.2. Rumus: P(Yi|X) = P(Xi|Yi) x P(Yi).', after=cur)
cur = p('Data Testing No. 1 - Kaisa Qomaru Zayyan', bold=True, after=cur)
cur = p('Data: Jarak=Dekat, Follow Up=Belum Dihubungi, Status Test=Sudah Tes, Nilai=Nilai Tinggi, Penghasilan=Di atas Rp6jt.', after=cur)
cur = p('Perhitungan kelas MASUK:', bold=True, after=cur)
cur = p('P(MASUK|X) = 7/15 x 2/7 x 6/7 x 7/7 x 6/7 x 3/7', center=True, after=cur)
cur = p('= 0,4667 x 0,2857 x 0,8571 x 1,0000 x 0,8571 x 0,4286 = 0,0420', bold=True, center=True, after=cur)
cur = p('Perhitungan kelas TIDAK MASUK:', bold=True, after=cur)
cur = p('P(TIDAK MASUK|X) = 8/15 x 1/8 x 5/8 x 3/8 x 2/8 x 0/8', center=True, after=cur)
cur = p('= 0,5333 x 0,1250 x 0,6250 x 0,3750 x 0,2500 x 0,0000 = 0,0000', bold=True, center=True, after=cur)
cur = p('Karena P(MASUK|X) = 0,0420 > P(TIDAK MASUK|X) = 0,0000, maka Kaisa Qomaru Zayyan diprediksi kelas MASUK. Hasil ini sesuai dengan status aktual pada data historis.', after=cur)

tbl_cmp = [
    ['No', 'Nama', 'Status Aktual', 'Hasil Prediksi'],
    ['1', {'t': 'Kaisa Qomaru Zayyan', 'l': True}, 'MASUK', 'MASUK'],
]
cur = ins_tbl(cur, tbl_cmp, 'Tabel 4.11 Hasil Perbandingan Data Prediksi dan Aktual')

# --- 6. Uji Hasil ---
cur = p('6.  Uji Hasil', bold=True, after=cur)
cur = p('Tahapan ini dilakukan untuk mengevaluasi kinerja model menggunakan Confusion Matrix terhadap 257 data testing yang diproses menggunakan model Naive Bayes dari 1.028 data training.', after=cur)

tbl_cm = [
    ['', '', 'Prediksi MASUK', 'Prediksi TIDAK MASUK'],
    ['Aktual', 'MASUK', '74 (TP)', '0 (FN)'],
    ['', 'TIDAK MASUK', '16 (FP)', '167 (TN)'],
]
cur = ins_tbl(cur, tbl_cm, 'Tabel 4.12 Confusion Matrix')

cur = p('Berdasarkan Tabel 4.12, berikut hasil evaluasi model:', after=cur)
cur = p('Akurasi  = (74+167) / (74+16+167+0) = 241/257 x 100% = 93,77%', center=True, after=cur)
cur = p('Presisi  = 74 / (74+16) = 74/90 x 100% = 82,22%', center=True, after=cur)
cur = p('Recall   = 74 / (74+0) = 74/74 x 100% = 100,00%', center=True, after=cur)
cur = p('F1-Score = (2 x 82,22 x 100) / (82,22 + 100) = 90,24%', center=True, after=cur)

tbl_ev = [
    ['Metrik', 'Rumus', 'Hasil'],
    [{'t': 'Akurasi', 'l': True}, {'t': '(TP+TN)/(TP+FP+TN+FN)', 'l': True}, '93,77%'],
    [{'t': 'Presisi', 'l': True}, {'t': 'TP/(TP+FP)', 'l': True}, '82,22%'],
    [{'t': 'Recall', 'l': True}, {'t': 'TP/(TP+FN)', 'l': True}, '100,00%'],
    [{'t': 'F1-Score', 'l': True}, {'t': '2xPresisixRecall/(Presisi+Recall)', 'l': True}, '90,24%'],
]
cur = ins_tbl(cur, tbl_ev, 'Tabel 4.13 Hasil Evaluasi Model Naive Bayes')

cur = p('Berdasarkan hasil evaluasi, model Naive Bayes menghasilkan akurasi sebesar 93,77%. Dapat disimpulkan bahwa tingkat keakuratan dalam memberikan rekomendasi tindak lanjut konfirmasi pendaftaran mahasiswa baru dengan pendekatan algoritma Naive Bayes adalah sangat akurat.', after=cur)

doc.save('SUSUN-SKRIPSI-ARIF.docx')
print('SELESAI - File berhasil disimpan.')
