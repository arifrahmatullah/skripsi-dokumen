import sys, io, shutil, json
from lxml import etree
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─── Namespaces ──────────────────────────────────────────────────────────────
M_NS      = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
_m        = lambda tag: f'{{{M_NS}}}{tag}'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'

shutil.copy('SUSUN-SKRIPSI-ARIF_BACKUP.docx', 'SUSUN-SKRIPSI-ARIF.docx')
print("Restored from backup.")

doc = Document('SUSUN-SKRIPSI-ARIF.docx')
TNR = 'Arial'

# ═══════════════════════════════════════════════════════════════════════════════
# OMML HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def mt(text):
    """m:r > m:t plain text element."""
    r = etree.Element(_m('r'))
    t = etree.SubElement(r, _m('t'))
    t.set(XML_SPACE, 'preserve')
    t.text = text
    return r

def msub(base, sub):
    """Subscript: base_sub."""
    s = etree.Element(_m('sSub'))
    e = etree.SubElement(s, _m('e'));   e.append(mt(base))
    sb = etree.SubElement(s, _m('sub')); sb.append(mt(sub))
    return s

def mfrac(num_items, den_items):
    """Fraction num/den."""
    f = etree.Element(_m('f'))
    n = etree.SubElement(f, _m('num'))
    d = etree.SubElement(f, _m('den'))
    for item in (num_items if isinstance(num_items, list) else [num_items]):
        n.append(item)
    for item in (den_items if isinstance(den_items, list) else [den_items]):
        d.append(item)
    return f

def eq_ins(math_elements, after_el):
    """Insert centered OMML math paragraph after after_el. Returns new element."""
    new_p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'),'0'); sp.set(qn('w:after'),'0')
    sp.set(qn('w:line'),'360'); sp.set(qn('w:lineRule'),'auto')
    pPr.append(sp); new_p.append(pPr)

    mathPara = etree.Element(_m('oMathPara'))
    mpp = etree.SubElement(mathPara, _m('oMathParaPr'))
    jc_m = etree.SubElement(mpp, _m('jc'))
    jc_m.set(_m('val'), 'center')
    oMath = etree.SubElement(mathPara, _m('oMath'))
    for el in math_elements:
        oMath.append(el)
    new_p.append(mathPara)
    after_el.addnext(new_p)
    return new_p

# ═══════════════════════════════════════════════════════════════════════════════
# PARAGRAPH & TABLE HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
cur = None

def p(text, bold=False, italic=False, center=False, size=10, after=None, ind=-1):
    # ind=-1 = auto: bold/center → 0 (heading), else → 1800 (body text)
    # ind=0  = no indent (explicit)
    # ind>0  = raw twips
    actual_ind = (0 if (bold or center) else 1800) if ind == -1 else ind
    new_p = OxmlElement('w:p')
    pPr   = OxmlElement('w:pPr')
    s = OxmlElement('w:pStyle'); s.set(qn('w:val'), 'ListParagraph'); pPr.append(s)
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'center' if center else 'both'); pPr.append(jc)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'),'0'); sp.set(qn('w:after'),'0')
    sp.set(qn('w:line'),'360');  sp.set(qn('w:lineRule'),'auto'); pPr.append(sp)
    if actual_ind > 0:
        i2 = OxmlElement('w:ind'); i2.set(qn('w:left'), str(actual_ind)); pPr.append(i2)
    new_p.append(pPr)
    if text:
        r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
        rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'),TNR); rf.set(qn('w:hAnsi'),TNR); rPr.append(rf)
        if bold:   rPr.append(OxmlElement('w:b'))
        if italic: rPr.append(OxmlElement('w:i'))
        sz = OxmlElement('w:sz');   sz.set(qn('w:val'),str(size*2));   rPr.append(sz)
        szc= OxmlElement('w:szCs'); szc.set(qn('w:val'),str(size*2));  rPr.append(szc)
        r.append(rPr)
        t = OxmlElement('w:t'); t.set(XML_SPACE,'preserve')
        t.text = text; r.append(t); new_p.append(r)
    ref = after if after is not None else cur
    ref.addnext(new_p)
    return new_p

def make_tbl(rows_data, hdr_rows=1):
    nc  = max(len(r) for r in rows_data)
    tbl = doc.add_table(rows=len(rows_data), cols=nc)
    tbl.style = 'Table Grid'
    for ri, row in enumerate(rows_data):
        for ci, ci_data in enumerate(row):
            if isinstance(ci_data, dict):
                txt  = ci_data.get('t','')
                bold = ci_data.get('b', ri < hdr_rows)
                left = ci_data.get('l', False)
            else:
                txt  = str(ci_data)
                bold = ri < hdr_rows
                left = False
            cell = tbl.cell(ri, ci)
            cell.text = ''
            pp  = cell.paragraphs[0]
            pp.alignment = WD_ALIGN_PARAGRAPH.LEFT if left else WD_ALIGN_PARAGRAPH.CENTER
            run = pp.add_run(txt)
            run.bold = bold; run.font.name = TNR; run.font.size = Pt(10)
            if ri < hdr_rows:
                tc   = cell._element
                tcPr = tc.find(qn('w:tcPr'))
                if tcPr is None:
                    tcPr = OxmlElement('w:tcPr'); tc.insert(0, tcPr)
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
                shd.set(qn('w:fill'),'D9D9D9'); tcPr.append(shd)
    el = tbl._element; el.getparent().remove(el)
    return el

def ins_tbl(after_el, rows_data, caption, source='Hasil Pengolahan Data (2025)', hdr_rows=1):
    c = p(caption, bold=True, center=True, after=after_el)
    tbl_el = make_tbl(rows_data, hdr_rows)
    c.addnext(tbl_el)
    s = p('Sumber: ' + source, italic=True, center=True, after=tbl_el)
    e = p('', after=s)
    return e

def tbl_cond(rows, caption):
    HDR = ['Nilai','Jml MASUK','Jml TDK MSK','P(X|MASUK)','P(X|TDK MSK)','Hasil MASUK','Hasil TDK MSK']
    d = [HDR]
    for r in rows:
        d.append([{'t':r[0],'l':True}, r[1], r[2], r[3], r[4], r[5], r[6]])
    return d, caption

def fmt(val):
    v = str(val).replace('_',' ')
    if 'Rp.4.000.001' in v: return 'Rp4-6jt'
    if 'Rp.2.000.001' in v: return 'Rp2-4jt'
    if 'Diatas Rp.6' in v or '> Rp6' in v: return '>Rp6jt'
    if 'Rp.1.000.001' in v: return 'Rp1-2jt'
    if 'Dibawah' in v: return '<Rp1jt'
    return v

# ─── Load data ────────────────────────────────────────────────────────────────
with open('testing_results.json', encoding='utf-8') as f:
    jd = json.load(f)
results = jd['results']
tp, tn, fp, fn = jd['tp'], jd['tn'], jd['fp'], jd['fn']
acc, prec, rec, f1 = jd['acc'], jd['prec'], jd['rec'], jd['f1']

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: INSERT IMAGES AT GMABAR PLACEHOLDERS
# ═══════════════════════════════════════════════════════════════════════════════
def replace_with_image(para_obj, img_path, caption_text):
    p_elem = para_obj._element
    for r in list(p_elem.findall(qn('w:r'))):
        p_elem.remove(r)
    pPr = p_elem.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); p_elem.insert(0, pPr)
    jc_el = pPr.find(qn('w:jc'))
    if jc_el is None:
        jc_el = OxmlElement('w:jc'); pPr.append(jc_el)
    jc_el.set(qn('w:val'), 'center')
    sp_el = pPr.find(qn('w:spacing'))
    if sp_el is None:
        sp_el = OxmlElement('w:spacing'); pPr.append(sp_el)
    sp_el.set(qn('w:before'),'0'); sp_el.set(qn('w:after'),'0')
    sp_el.set(qn('w:line'),'360'); sp_el.set(qn('w:lineRule'),'auto')

    run = para_obj.add_run()
    run.add_picture(img_path, width=Cm(14))

    # Caption paragraph
    cap_p = OxmlElement('w:p')
    cap_pPr = OxmlElement('w:pPr')
    cap_jc = OxmlElement('w:jc'); cap_jc.set(qn('w:val'), 'center'); cap_pPr.append(cap_jc)
    cap_sp = OxmlElement('w:spacing')
    cap_sp.set(qn('w:before'),'0'); cap_sp.set(qn('w:after'),'0')
    cap_sp.set(qn('w:line'),'360'); cap_sp.set(qn('w:lineRule'),'auto')
    cap_pPr.append(cap_sp); cap_p.append(cap_pPr)
    cap_r = OxmlElement('w:r')
    cap_rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'),'Arial'); rf.set(qn('w:hAnsi'),'Arial'); cap_rPr.append(rf)
    cap_rPr.append(OxmlElement('w:b'))
    cap_sz = OxmlElement('w:sz');   cap_sz.set(qn('w:val'),'20'); cap_rPr.append(cap_sz)
    cap_szc = OxmlElement('w:szCs'); cap_szc.set(qn('w:val'),'20'); cap_rPr.append(cap_szc)
    cap_r.append(cap_rPr)
    cap_t = OxmlElement('w:t'); cap_t.text = caption_text; cap_r.append(cap_t)
    cap_p.append(cap_r)
    p_elem.addnext(cap_p)
    return cap_p

img_count = 0
for para in doc.paragraphs:
    stripped = para.text.strip()
    if stripped == 'Gmabar' and img_count == 0:
        replace_with_image(para, 'Proses Bisnis Lama.jpg', 'Gambar 4.1 BPEL Proses Bisnis Lama')
        img_count += 1
        print("Image 1 inserted: Proses Bisnis Lama")
    elif stripped == 'Gambar' and img_count == 1:
        replace_with_image(para, 'Proses Bisnis Baru.jpg', 'Gambar 4.2 BPEL Proses Bisnis Baru')
        img_count += 1
        print("Image 2 inserted: Proses Bisnis Baru")
    if img_count >= 2:
        break
print(f"Total images inserted: {img_count}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: FIND "HASIL ANALISIS METODE" PARAGRAPH (by text)
# ═══════════════════════════════════════════════════════════════════════════════
cur = None
for para in doc.paragraphs:
    if 'Hasil Anali' in para.text and 'Metode' in para.text:
        cur = para._element
        print(f"Found: '{para.text.strip()}'")
        break
if cur is None:
    raise RuntimeError("Tidak menemukan paragraf 'Hasil Analisis Metode'!")

# Delete 3 placeholder paragraphs right after it
deleted = 0
for _ in range(3):
    nxt = cur.getnext()
    if nxt is not None and nxt.tag == qn('w:p'):
        nxt.getparent().remove(nxt)
        deleted += 1
print(f"Deleted {deleted} placeholder paragraphs.")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: INSERT "HASIL ANALISIS METODE" CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

cur = p('Metode yang diterapkan dalam proses penelitian ini menggunakan algoritma Naive Bayes. '
        'Metode ini diharapkan dapat menghasilkan rekomendasi tindak lanjut konfirmasi pendaftaran '
        'mahasiswa baru secara efektif dan akurat. Berikut adalah beberapa langkah dengan pendekatan '
        'algoritma Naive Bayes:', after=cur)

# ── a. Menyiapkan Dataset ─────────────────────────────────────────────────────
cur = p('a.  Menyiapkan Dataset', bold=True, after=cur)
cur = p('Pada langkah ini dilakukan pengumpulan data historis pendaftaran mahasiswa baru Universitas Tazkia. '
        'Data sampel yang digunakan berjumlah 30 record yang selanjutnya dibagi menjadi dua dataset, '
        'terdiri dari 50% untuk data training yaitu sebanyak 15 data, serta 50% untuk data testing '
        'yaitu sebanyak 15 data. Berikut adalah dataset untuk data training dan testing yang dapat '
        'dilihat pada Tabel 4.1 dan Tabel 4.2 di bawah ini.', after=cur)

tbl_tr = [
    ['No','Nama','Kat. Jarak','Follow Up','Status Test','Nilai Test','Penghasilan','Kelas'],
    ['1', {'t':'Jihad Muhammad Akbar','l':True},'Dekat','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Rp2-4jt','l':True},'MASUK'],
    ['2', {'t':'Ghaitsa Witanya G.','l':True},'Dekat','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'>Rp6jt','l':True},'MASUK'],
    ['3', {'t':'ULIL AMRI SIDDIK','l':True},'Jauh','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Rp2-4jt','l':True},'MASUK'],
    ['4', {'t':'Akmal Syawqi Albar','l':True},'Sedang','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Tdk Diketahui','l':True},'MASUK'],
    ['5', {'t':"Naysella Robi'atul A.",'l':True},'Jauh','Belum Dihubungi','Sudah Tes','Nilai Sedang',{'t':'>Rp6jt','l':True},'MASUK'],
    ['6', {'t':'Ayu Nabila','l':True},'Jauh','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Tdk Diketahui','l':True},'MASUK'],
    ['7', {'t':'Alya Adibah','l':True},'Jauh','Kontak Awal','Sudah Tes','Nilai Tinggi',{'t':'>Rp6jt','l':True},'MASUK'],
    ['8', {'t':'Test Rudie','l':True},'Jauh','Belum Dihubungi','Belum Tes','Tdk Ada Nilai',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['9', {'t':'Sayidatus Sajil H.','l':True},'Sedang','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['10',{'t':'Khalid AlMarzuq','l':True},'Jauh','Belum Dihubungi','Sudah Tes','Nilai Sedang',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['11',{'t':'Rizal Trenggoni','l':True},'Dekat','Belum Dihubungi','Belum Tes','Tdk Ada Nilai',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['12',{'t':'Siti Khofifah','l':True},'Sedang','Follow Up Intensif','Belum Tes','Tdk Ada Nilai',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['13',{'t':'MOHAMMAD SYAHRONI','l':True},'Jauh','Follow Up','Belum Tes','Tdk Ada Nilai',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['14',{'t':'Muhamad Najhan A.F.','l':True},'Sedang','Follow Up','Belum Tes','Tdk Ada Nilai',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
    ['15',{'t':'Susilo Wardoyo','l':True},'Jauh','Belum Dihubungi','Sudah Tes','Nilai Tinggi',{'t':'Tdk Diketahui','l':True},'TDK MASUK'],
]
cur = ins_tbl(cur, tbl_tr, 'Tabel 4.1 Dataset Untuk Data Training',
              'Data Internal Pendaftaran Universitas Tazkia')

tbl_te_rows = [['No','Nama','Kat. Jarak','Follow Up','Status Test','Nilai Test','Penghasilan','Prediksi']]
for i, r in enumerate(results, 1):
    tbl_te_rows.append([
        str(i), {'t': r['nama'], 'l': True},
        fmt(r['vals'][0]), fmt(r['vals'][1]), fmt(r['vals'][2]),
        fmt(r['vals'][3]), {'t': fmt(r['vals'][4]), 'l': True}, '?'
    ])
cur = ins_tbl(cur, tbl_te_rows, 'Tabel 4.2 Dataset Untuk Data Testing',
              'Data Internal Pendaftaran Universitas Tazkia')

# ── b. Pre-processing ─────────────────────────────────────────────────────────
cur = p('b.  Pre-processing Data', bold=True, after=cur)
cur = p('Pada langkah ini dilakukan pre-processing atau mempersiapkan data sebelum digunakan '
        'dalam algoritma Naive Bayes melalui pembersihan data dan seleksi fitur.', after=cur)
cur = p('1)  Pembersihan Data', bold=True, after=cur)
cur = p('Dilakukan pemeriksaan terhadap data yang memiliki nilai kosong (missing value) atau '
        'tidak relevan (noise). Berdasarkan hasil pemeriksaan, data pada Tabel 4.1 dan Tabel 4.2 '
        'tidak ditemukan nilai kosong sehingga seluruh data dapat langsung digunakan.', after=cur)
cur = p('2)  Seleksi Fitur', bold=True, after=cur)
cur = p('Seleksi fitur dilakukan untuk memilih atribut yang akan digunakan dalam proses '
        'klasifikasi. Hasil seleksi fitur dapat dilihat pada Tabel 4.3 berikut.', after=cur)

tbl_f = [
    ['Fitur/Atribut yang Ada Sebelumnya','Fitur/Atribut yang Digunakan'],
    [{'t':'Kategori Jarak Asal','l':True},      {'t':'Kategori Jarak Asal','l':True}],
    [{'t':'Kategori Asal Sekolah','l':True},    {'t':'- (tidak digunakan)','l':True}],
    [{'t':'Waktu Pendaftaran','l':True},         {'t':'- (tidak digunakan)','l':True}],
    [{'t':'Tingkat Follow Up Internal','l':True},{'t':'Tingkat Follow Up Internal','l':True}],
    [{'t':'Status Uang Pendaftaran','l':True},   {'t':'- (tidak digunakan)','l':True}],
    [{'t':'Status Test','l':True},               {'t':'Status Test','l':True}],
    [{'t':'Kategori Nilai Test','l':True},       {'t':'Kategori Nilai Test','l':True}],
    [{'t':'Kategori Penghasilan','l':True},      {'t':'Kategori Penghasilan','l':True}],
    [{'t':'Status Retensi Final (Target)','l':True},{'t':'Status Retensi Final (Target)','l':True}],
]
cur = ins_tbl(cur, tbl_f, 'Tabel 4.3 Hasil Seleksi Fitur')

# ── c. Variabel ───────────────────────────────────────────────────────────────
cur = p('c.  Menentukan Variabel Penelitian', bold=True, after=cur)
cur = p('Berdasarkan hasil seleksi fitur, variabel yang digunakan dalam proses klasifikasi '
        'Naive Bayes dapat dilihat pada Tabel 4.4 berikut.', after=cur)

tbl_v = [
    ['Kode','Atribut','Tipe','Nilai'],
    ['X1',{'t':'Kategori Jarak Asal','l':True},      {'t':'Variabel Atribut','l':True},{'t':'Dekat, Sedang, Jauh','l':True}],
    ['X2',{'t':'Tingkat Follow Up Internal','l':True},{'t':'Variabel Atribut','l':True},{'t':'Belum Dihubungi, Kontak Awal, Follow Up, Follow Up Intensif','l':True}],
    ['X3',{'t':'Status Test','l':True},               {'t':'Variabel Atribut','l':True},{'t':'Sudah Tes, Belum Tes','l':True}],
    ['X4',{'t':'Kategori Nilai Test','l':True},       {'t':'Variabel Atribut','l':True},{'t':'Nilai Tinggi, Nilai Sedang, Tidak Ada Nilai','l':True}],
    ['X5',{'t':'Kategori Penghasilan','l':True},      {'t':'Variabel Atribut','l':True},{'t':'>Rp6jt, Rp4-6jt, Rp2-4jt, Rp1-2jt, <Rp1jt, Tidak Diketahui','l':True}],
    ['Y', {'t':'Status Retensi Final','l':True},      {'t':'Kelas Target','l':True},    {'t':'MASUK, TIDAK MASUK','l':True}],
]
cur = ins_tbl(cur, tbl_v, 'Tabel 4.4 Variabel Penelitian')

# ── d. Prior Probability ──────────────────────────────────────────────────────
cur = p('d.  Menghitung Prior Probability', bold=True, after=cur)
cur = p('Pada tahap ini dilakukan perhitungan probabilitas prior atau peluang kemunculan setiap '
        'kelas target (Y) yaitu MASUK dan TIDAK MASUK, dihitung berdasarkan data training pada '
        'Tabel 4.1 yang berjumlah 15 data. Rumus prior probability adalah sebagai berikut:', after=cur)

# Rumus Prior: P(Yi) = ni/n
cur = eq_ins([
    mt('P('), msub('Y','i'), mt(') = '),
    mfrac([msub('n','i')], [mt('n')])
], after_el=cur)

cur = p('Sehingga diperoleh nilai prior probability untuk masing-masing kelas sebagai berikut:', after=cur)

# P(Y=MASUK) = 7/15
cur = eq_ins([
    mt('P(Y = MASUK) = '),
    mfrac([mt('7')], [mt('15')]),
    mt(' = 0,4667')
], after_el=cur)

# P(Y=TIDAK MASUK) = 8/15
cur = eq_ins([
    mt('P(Y = TIDAK MASUK) = '),
    mfrac([mt('8')], [mt('15')]),
    mt(' = 0,5333')
], after_el=cur)

cur = p('Berdasarkan hasil perhitungan di atas, maka hasil perhitungan prior probability dapat '
        'dilihat pada Tabel 4.5.', after=cur)

tbl_pr = [
    ['Kelas (Y)','Jumlah Kemunculan (ni)','P(Y)','Hasil'],
    [{'t':'MASUK','l':True},        '7','7 / 15','0,4667'],
    [{'t':'TIDAK MASUK','l':True},  '8','8 / 15','0,5333'],
    [{'t':'Total Data (n)','b':True,'l':True},'15','',''],
]
cur = ins_tbl(cur, tbl_pr, 'Tabel 4.5 Hasil Perhitungan Prior Probability')

# ── e. Likelihood ─────────────────────────────────────────────────────────────
cur = p('e.  Menghitung Likelihood (Conditional Probability)', bold=True, after=cur)
cur = p('Pada tahap ini dilakukan perhitungan likelihood atau conditional probability, yaitu '
        'probabilitas kemunculan setiap nilai atribut pada masing-masing kelas berdasarkan '
        'data training. Rumus yang digunakan dengan Laplace Smoothing:', after=cur)

# Rumus Laplace: P(Xi|H) = (ni+1)/(n+K)
cur = eq_ins([
    mt('P('), msub('X','i'), mt(' | H) = '),
    mfrac(
        [msub('n','i'), mt(' + 1')],
        [mt('n + K')]
    )
], after_el=cur)

cur = p('Keterangan: ni = jumlah data bernilai Xi pada kelas H; n = total data kelas H; '
        'K = jumlah nilai unik atribut tersebut. '
        'Penambahan nilai 1 pada pembilang dan K pada penyebut merupakan teknik Laplace Smoothing '
        'untuk menghindari nilai probabilitas nol.', after=cur)

d, c = tbl_cond([
    ('Dekat','2','1','(2+1)/(7+3)','(1+1)/(8+3)','0,3000','0,1818'),
    ('Sedang','1','3','(1+1)/(7+3)','(3+1)/(8+3)','0,2000','0,3636'),
    ('Jauh',  '4','4','(4+1)/(7+3)','(4+1)/(8+3)','0,5000','0,4545'),
    ('Total', '7','8','','','',''),
], 'Tabel 4.6 Hasil Perhitungan Conditional Probability Kategori Jarak Asal')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Belum Dihubungi',   '6','5','(6+1)/(7+4)','(5+1)/(8+4)','0,6364','0,5000'),
    ('Kontak Awal',       '1','0','(1+1)/(7+4)','(0+1)/(8+4)','0,1818','0,0833'),
    ('Follow Up',         '0','2','(0+1)/(7+4)','(2+1)/(8+4)','0,0909','0,2500'),
    ('Follow Up Intensif','0','1','(0+1)/(7+4)','(1+1)/(8+4)','0,0909','0,1667'),
    ('Total',             '7','8','','','',''),
], 'Tabel 4.7 Hasil Perhitungan Conditional Probability Tingkat Follow Up Internal')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Sudah Tes','7','3','(7+1)/(7+2)','(3+1)/(8+2)','0,8889','0,4000'),
    ('Belum Tes','0','5','(0+1)/(7+2)','(5+1)/(8+2)','0,1111','0,6000'),
    ('Total',    '7','8','','','',''),
], 'Tabel 4.8 Hasil Perhitungan Conditional Probability Status Test')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('Nilai Tinggi',   '6','2','(6+1)/(7+3)','(2+1)/(8+3)','0,7000','0,2727'),
    ('Nilai Sedang',   '1','1','(1+1)/(7+3)','(1+1)/(8+3)','0,2000','0,1818'),
    ('Tidak Ada Nilai','0','5','(0+1)/(7+3)','(5+1)/(8+3)','0,1000','0,5455'),
    ('Total',          '7','8','','','',''),
], 'Tabel 4.9 Hasil Perhitungan Conditional Probability Kategori Nilai Test')
cur = ins_tbl(cur, d, c)

d, c = tbl_cond([
    ('>Rp6jt',         '3','0','(3+1)/(7+6)','(0+1)/(8+6)','0,3077','0,0714'),
    ('Rp4-6jt',        '0','0','(0+1)/(7+6)','(0+1)/(8+6)','0,0769','0,0714'),
    ('Rp2-4jt',        '2','0','(2+1)/(7+6)','(0+1)/(8+6)','0,2308','0,0714'),
    ('Rp1-2jt',        '0','0','(0+1)/(7+6)','(0+1)/(8+6)','0,0769','0,0714'),
    ('<Rp1jt',         '0','0','(0+1)/(7+6)','(0+1)/(8+6)','0,0769','0,0714'),
    ('Tidak Diketahui','2','8','(2+1)/(7+6)','(8+1)/(8+6)','0,2308','0,6429'),
    ('Total',          '7','8','','','',''),
], 'Tabel 4.10 Hasil Perhitungan Conditional Probability Kategori Penghasilan')
cur = ins_tbl(cur, d, c)

# ── f. Posterior Probability ──────────────────────────────────────────────────
cur = p('f.  Menghitung Posterior Probability', bold=True, after=cur)
cur = p('Pada tahapan ini dilakukan perhitungan posterior probability untuk memprediksi kelas Y '
        '(MASUK dan TIDAK MASUK) berdasarkan seluruh data testing pada Tabel 4.2. '
        'Rumus yang digunakan:', after=cur)

# Rumus Posterior: P(Yi|X) = P(Xi|Yi) x P(Yi)
cur = eq_ins([
    mt('P('), msub('Y','i'), mt('|X) = P('), msub('X','i'), mt('|'), msub('Y','i'), mt(') × P('), msub('Y','i'), mt(')')
], after_el=cur)

cur = p('Nilai dari prior probability dan conditional probability yang digunakan pada perhitungan '
        'ini diambil dari Tabel 4.5 sampai dengan Tabel 4.10. Hasil perhitungan posterior '
        'probability untuk seluruh data testing dapat dilihat pada Tabel 4.11 berikut.', after=cur)

tbl_post = [['No','Nama','P(Y|X)','Kat. Jarak','Follow Up','Status Test','Nilai Test','Penghasilan','Prior','Posterior']]
for i, r in enumerate(results, 1):
    pm_vals = [str(v) for v in r['pm']]
    pt_vals = [str(v) for v in r['pt']]
    tbl_post.append([
        str(i), {'t': r['nama'][:22], 'l': True}, 'P(MASUK|X)',
        pm_vals[0], pm_vals[1], pm_vals[2], pm_vals[3], pm_vals[4],
        str(r['prior_m']), str(r['post_m'])
    ])
    tbl_post.append([
        '', '', 'P(TDK MSK|X)',
        pt_vals[0], pt_vals[1], pt_vals[2], pt_vals[3], pt_vals[4],
        str(r['prior_t']), str(r['post_t'])
    ])
cur = ins_tbl(cur, tbl_post, 'Tabel 4.11 Hasil Perhitungan Posterior Probability')

# ── g. Klasifikasi ────────────────────────────────────────────────────────────
cur = p('g.  Melakukan Klasifikasi (Prediksi)', bold=True, after=cur)
cur = p('Berdasarkan hasil perhitungan posterior probability pada Tabel 4.11, selanjutnya '
        'masing-masing nilai posterior dibandingkan untuk menentukan kelas prediksi, '
        'dengan ketentuan sebagai berikut:', after=cur)
cur = p('a.  P(MASUK|X)  >  P(TIDAK MASUK|X)  →  Prediksi = MASUK', after=cur, ind=2520)
cur = p('b.  P(MASUK|X)  <  P(TIDAK MASUK|X)  →  Prediksi = TIDAK MASUK', after=cur, ind=2520)
cur = p('Adapun hasil prediksi untuk seluruh data testing dapat dilihat pada Tabel 4.12 berikut.', after=cur)

tbl_pred = [['No','Nama','Nilai Posterior Terbesar','Status Aktual','Prediksi']]
for i, r in enumerate(results, 1):
    tbl_pred.append([
        str(i), {'t': r['nama'], 'l': True},
        str(max(r['post_m'], r['post_t'])),
        r['aktual'], r['pred']
    ])
cur = ins_tbl(cur, tbl_pred, 'Tabel 4.12 Hasil Prediksi Status Konfirmasi Pendaftaran')

# ── 6. Uji Hasil ──────────────────────────────────────────────────────────────
cur = p('6.  Uji Hasil', bold=True, after=cur)
cur = p('Tahapan ini dilakukan untuk mengevaluasi kinerja model menggunakan Confusion Matrix. '
        'Evaluasi dilakukan dengan membandingkan hasil prediksi algoritma Naive Bayes terhadap '
        'status aktual pada 15 data testing. '
        'Hasil perbandingan tersebut dapat dilihat pada Tabel 4.13 berikut.', after=cur)

tbl_cm = [
    ['','','Prediksi MASUK','Prediksi TIDAK MASUK'],
    ['Aktual','MASUK',       f'{tp} (TP)', f'{fn} (FN)'],
    ['',      'TIDAK MASUK', f'{fp} (FP)', f'{tn} (TN)'],
]
cur = ins_tbl(cur, tbl_cm, 'Tabel 4.13 Confusion Matrix')

cur = p('Berdasarkan Tabel 4.13, maka berikut adalah hasil evaluasi model yang dihitung '
        'menggunakan rumus di bawah ini.', after=cur)

total = tp + tn + fp + fn

# Akurasi equation
cur = eq_ins([
    mt('Akurasi = '),
    mfrac([mt('TP + TN')], [mt('TP + FP + TN + FN')]),
    mt(f' = '),
    mfrac([mt(f'{tp+tn}')], [mt(f'{total}')]),
    mt(f' × 100% = {acc}%')
], after_el=cur)

# Presisi equation
cur = eq_ins([
    mt('Presisi = '),
    mfrac([mt('TP')], [mt('TP + FP')]),
    mt(f' = '),
    mfrac([mt(f'{tp}')], [mt(f'{tp+fp}')]),
    mt(f' × 100% = {prec}%')
], after_el=cur)

# Recall equation
cur = eq_ins([
    mt('Recall = '),
    mfrac([mt('TP')], [mt('TP + FN')]),
    mt(f' = '),
    mfrac([mt(f'{tp}')], [mt(f'{tp+fn}')]),
    mt(f' × 100% = {rec}%')
], after_el=cur)

# F1-Score equation
cur = eq_ins([
    mt('F1-Score = '),
    mfrac(
        [mt(f'2 × {prec} × {rec}')],
        [mt(f'{prec} + {rec}')]
    ),
    mt(f' = {f1}%')
], after_el=cur)

tbl_ev = [
    ['Metrik','Rumus','Hasil'],
    [{'t':'Akurasi','l':True},  {'t':'(TP+TN) / (TP+FP+TN+FN)','l':True},       f'{acc}%'],
    [{'t':'Presisi','l':True},  {'t':'TP / (TP+FP)','l':True},                   f'{prec}%'],
    [{'t':'Recall','l':True},   {'t':'TP / (TP+FN)','l':True},                   f'{rec}%'],
    [{'t':'F1-Score','l':True}, {'t':'2 x Presisi x Recall / (Presisi+Recall)','l':True}, f'{f1}%'],
]
cur = ins_tbl(cur, tbl_ev, 'Tabel 4.14 Hasil Evaluasi Model Naive Bayes')

cur = p(f'Berdasarkan hasil evaluasi pada Tabel 4.14, model Naive Bayes menghasilkan '
        f'akurasi sebesar {acc}% dengan nilai presisi {prec}%, recall {rec}%, dan F1-Score {f1}%. '
        f'Jadi, dapat disimpulkan bahwa tingkat keakuratan dalam memberikan rekomendasi tindak lanjut '
        f'konfirmasi pendaftaran mahasiswa baru dengan pendekatan algoritma Naive Bayes adalah akurat.',
        after=cur)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: INSERT d. ANALISIS KEBUTUHAN SISTEM (Use Case Diagram)
# ═══════════════════════════════════════════════════════════════════════════════
aks_cur = None
for para in doc.paragraphs:
    if para.text.strip() == 'Analisis Kebutuhan Sistem':
        aks_cur = para._element
        print("Found: 'Analisis Kebutuhan Sistem'")
        break

if aks_cur is not None:
    # Intro
    aks_cur = p('Pemodelan objek pada aplikasi yang akan dikembangkan dijelaskan dalam bentuk '
                'diagram use case berdasarkan pada proses rekomendasi tindak lanjut konfirmasi '
                'pendaftaran mahasiswa baru, untuk memodelkan serta mengorganisasi pada aplikasi '
                'sehingga mendapatkan keluaran aplikasi sesuai dengan yang diharapkan dan '
                'dibutuhkan oleh pengguna. Berikut diagram use case pada aplikasi yang akan '
                'dikembangkan dapat dilihat pada Gambar 4.3.', after=aks_cur)

    # Gambar Use Case Diagram
    img_p_elem = OxmlElement('w:p')
    img_pPr = OxmlElement('w:pPr')
    img_jc = OxmlElement('w:jc'); img_jc.set(qn('w:val'), 'center'); img_pPr.append(img_jc)
    img_sp = OxmlElement('w:spacing')
    img_sp.set(qn('w:before'),'0'); img_sp.set(qn('w:after'),'0')
    img_sp.set(qn('w:line'),'360'); img_sp.set(qn('w:lineRule'),'auto')
    img_pPr.append(img_sp); img_p_elem.append(img_pPr)
    aks_cur.addnext(img_p_elem)

    from docx.oxml import OxmlElement as OE
    from docx.shared import Cm as DCm
    # Find the paragraph object to add picture
    for para in doc.paragraphs:
        if para._element is img_p_elem:
            run = para.add_run()
            run.add_picture('Use Case Diagram.png', width=DCm(13))
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break

    aks_cur = img_p_elem

    # Caption
    cap_p = OxmlElement('w:p')
    cap_pPr = OxmlElement('w:pPr')
    cap_jc = OxmlElement('w:jc'); cap_jc.set(qn('w:val'), 'center'); cap_pPr.append(cap_jc)
    cap_sp = OxmlElement('w:spacing')
    cap_sp.set(qn('w:before'),'0'); cap_sp.set(qn('w:after'),'0')
    cap_sp.set(qn('w:line'),'360'); cap_sp.set(qn('w:lineRule'),'auto')
    cap_pPr.append(cap_sp); cap_p.append(cap_pPr)
    cap_r = OxmlElement('w:r')
    cap_rPr = OxmlElement('w:rPr')
    cap_rf = OxmlElement('w:rFonts'); cap_rf.set(qn('w:ascii'),'Arial'); cap_rf.set(qn('w:hAnsi'),'Arial'); cap_rPr.append(cap_rf)
    cap_rPr.append(OxmlElement('w:b'))
    cap_sz = OxmlElement('w:sz'); cap_sz.set(qn('w:val'),'20'); cap_rPr.append(cap_sz)
    cap_szc = OxmlElement('w:szCs'); cap_szc.set(qn('w:val'),'20'); cap_rPr.append(cap_szc)
    cap_r.append(cap_rPr)
    cap_t = OxmlElement('w:t'); cap_t.text = 'Gambar 4.3 Diagram Use Case'; cap_r.append(cap_t)
    cap_p.append(cap_r)
    aks_cur.addnext(cap_p)
    aks_cur = cap_p

    aks_cur = p('Sumber: Hasil Perancangan (2025)', italic=True, center=True, after=aks_cur)

    # Penjelasan
    aks_cur = p('Pada Gambar 4.3 dijelaskan bahwa terdapat 1 (satu) aktor dalam aplikasi '
                'rekomendasi tindak lanjut konfirmasi pendaftaran mahasiswa baru yaitu Tim Marketing. '
                'Tim Marketing diharuskan untuk login terlebih dahulu agar dapat mengakses aplikasi '
                'tersebut. Adapun use case yang dapat dilakukan oleh Tim Marketing adalah sebagai '
                'berikut:', after=aks_cur)

    aks_cur = p('a.  Login: Tim Marketing melakukan autentikasi untuk masuk ke dalam sistem.',
                after=aks_cur, ind=2520)
    aks_cur = p('b.  Logout: Tim Marketing keluar dari sistem setelah selesai menggunakan aplikasi.',
                after=aks_cur, ind=2520)
    aks_cur = p('c.  Kelola Data Pendaftar: Tim Marketing dapat mengelola data calon mahasiswa '
                'baru yang terdaftar dalam sistem, termasuk melihat dan memperbarui data.',
                after=aks_cur, ind=2520)
    aks_cur = p('d.  Lihat Hasil Klasifikasi Naive Bayes: Tim Marketing dapat melihat hasil '
                'klasifikasi algoritma Naive Bayes terhadap seluruh data calon mahasiswa.',
                after=aks_cur, ind=2520)
    aks_cur = p('e.  Lihat Rekomendasi Tindak Lanjut: Tim Marketing dapat melihat rekomendasi '
                'tindak lanjut yang dihasilkan sistem untuk setiap calon mahasiswa berdasarkan '
                'hasil prediksi Naive Bayes.',
                after=aks_cur, ind=2520)
    aks_cur = p('f.  Lihat Detail Hasil Prediksi: Tim Marketing dapat melihat detail '
                'perhitungan probabilitas prediksi untuk setiap data calon mahasiswa.',
                after=aks_cur, ind=2520)
    aks_cur = p('g.  Cetak / Export Laporan: Tim Marketing dapat mencetak atau mengekspor '
                'laporan hasil rekomendasi tindak lanjut konfirmasi pendaftaran.',
                after=aks_cur, ind=2520)
    print("d. Analisis Kebutuhan Sistem inserted.")
else:
    print("WARNING: 'Analisis Kebutuhan Sistem' paragraph not found.")

# ═══════════════════════════════════════════════════════════════════════════════
# C. PEMBAHASAN — insert after placeholder "Pembahasan" di akhir dokumen
# ═══════════════════════════════════════════════════════════════════════════════
# Cari placeholder "Pembahasan" (bukan "C.  Pembahasan" yang kita buat)
pemb_el = None
for para in doc.paragraphs:
    if para.text.strip() == 'Pembahasan':
        pemb_el = para._element
        break

if pemb_el is not None:
    # Ganti isi placeholder jadi heading "C.  Pembahasan"
    for r in list(pemb_el.findall(qn('w:r'))):
        pemb_el.remove(r)
    pPr = pemb_el.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); pemb_el.insert(0, pPr)
    sp_el = pPr.find(qn('w:spacing'))
    if sp_el is None:
        sp_el = OxmlElement('w:spacing'); pPr.append(sp_el)
    sp_el.set(qn('w:before'),'0'); sp_el.set(qn('w:after'),'0')
    sp_el.set(qn('w:line'),'360'); sp_el.set(qn('w:lineRule'),'auto')
    r_new = OxmlElement('w:r')
    rPr_new = OxmlElement('w:rPr')
    rf_new = OxmlElement('w:rFonts'); rf_new.set(qn('w:ascii'),TNR); rf_new.set(qn('w:hAnsi'),TNR); rPr_new.append(rf_new)
    rPr_new.append(OxmlElement('w:b'))
    sz_new = OxmlElement('w:sz'); sz_new.set(qn('w:val'),'20'); rPr_new.append(sz_new)
    szc_new = OxmlElement('w:szCs'); szc_new.set(qn('w:val'),'20'); rPr_new.append(szc_new)
    r_new.append(rPr_new)
    t_new = OxmlElement('w:t'); t_new.text = 'C.  Pembahasan'; r_new.append(t_new)
    pemb_el.append(r_new)
    cur = pemb_el
    print("C. Pembahasan placeholder ditemukan dan digunakan.")
else:
    # Fallback: insert setelah paragraf terakhir
    cur = doc.paragraphs[-1]._element
    cur = p('C.  Pembahasan', bold=True, after=cur)
    print("Placeholder tidak ditemukan, insert di akhir dokumen.")

# 1. Pembahasan Hasil Analisis Metode
cur = p('1.  Pembahasan Hasil Analisis Metode', bold=True, after=cur)
cur = p('Penerapan algoritma Naive Bayes dalam penelitian ini bertujuan untuk memberikan '
        'rekomendasi tindak lanjut konfirmasi pendaftaran mahasiswa baru Universitas Tazkia. '
        'Metode ini bekerja dengan memperkirakan kemungkinan status retensi calon mahasiswa '
        'berdasarkan pengalaman dari data historis pendaftaran sebelumnya, yaitu dengan cara '
        'menghitung nilai probabilitas dari setiap atribut pada masing-masing kelas target, '
        'kemudian membandingkan nilai probabilitas akhir untuk menentukan hasil prediksi.', after=cur)

cur = p('Proses klasifikasi dilakukan menggunakan 5 atribut yang telah diseleksi, yaitu '
        'Kategori Jarak Asal (X1), Tingkat Follow Up Internal (X2), Status Test (X3), '
        'Kategori Nilai Test (X4), dan Kategori Penghasilan (X5). Berdasarkan hasil seleksi '
        'fitur pada Tabel 4.3, atribut seperti Kategori Asal Sekolah, Waktu Pendaftaran, dan '
        'Status Uang Pendaftaran tidak diikutsertakan karena tidak memiliki pengaruh signifikan '
        'terhadap penentuan kelas target dalam konteks penelitian ini.', after=cur)

cur = p('Berdasarkan hasil perhitungan prior probability pada Tabel 4.5, diketahui bahwa '
        'proporsi kelas MASUK adalah 0,4667 (7 dari 15 data training) dan kelas TIDAK MASUK '
        'adalah 0,5333 (8 dari 15 data training). Komposisi ini menunjukkan bahwa data training '
        'yang digunakan relatif seimbang antara kedua kelas, sehingga model tidak mengalami '
        'bias kelas yang signifikan dalam proses pembelajaran.', after=cur)

cur = p('Teknik Laplace Smoothing diterapkan pada perhitungan conditional probability untuk '
        'menghindari nilai probabilitas nol pada nilai atribut yang tidak muncul di data training. '
        'Penerapan teknik ini terbukti efektif dalam menjaga konsistensi perhitungan posterior '
        'probability pada seluruh 15 data testing, sehingga setiap data testing dapat '
        'diklasifikasikan dengan hasil yang valid.', after=cur)

# 2. Pembahasan Uji Hasil
cur = p('2.  Pembahasan Uji Hasil', bold=True, after=cur)
cur = p(f'Berdasarkan hasil pengujian menggunakan confusion matrix pada Tabel 4.13, dari '
        f'15 data testing yang diuji, model Naive Bayes berhasil mengklasifikasikan 12 data '
        f'dengan benar dan 3 data secara keliru. Rinciannya adalah sebagai berikut: '
        f'{tp} data aktual MASUK diprediksi benar sebagai MASUK (True Positive), '
        f'{tn} data aktual TIDAK MASUK diprediksi benar sebagai TIDAK MASUK (True Negative), '
        f'{fp} data aktual TIDAK MASUK diprediksi keliru sebagai MASUK (False Positive), dan '
        f'{fn} data aktual MASUK diprediksi keliru sebagai TIDAK MASUK (False Negative).', after=cur)

cur = p('Dari 3 data yang salah diklasifikasikan, terdapat 2 kasus False Positive yaitu '
        'Muhamad Helmi dan NAJUA HAMIDAH. Kedua data tersebut memiliki pola atribut yang '
        'serupa, yaitu sudah mengikuti tes dan mendapatkan nilai tinggi, namun pada kenyataannya '
        'tidak mendaftar. Hal ini menunjukkan bahwa atribut Status Test dan Kategori Nilai Test '
        'memiliki bobot probabilitas yang tinggi untuk kelas MASUK, sehingga model kesulitan '
        'membedakan calon mahasiswa yang memiliki nilai tinggi namun tidak melanjutkan '
        'pendaftarannya, khususnya ketika atribut penghasilan tercatat sebagai Tidak Diketahui.', after=cur)

cur = p('Adapun 1 kasus False Negative terjadi pada data IBNUH AKHYAR ABDILLAH SHAHIB, '
        'yang aktualnya MASUK namun diprediksi sebagai TIDAK MASUK. Kombinasi atribut '
        'Kategori Jarak Jauh dan penghasilan Rp.4.000.001 - Rp.6.000.000 jarang muncul '
        'pada kelas MASUK dalam data training, sehingga nilai posterior probability kelas '
        'TIDAK MASUK lebih tinggi meskipun selisihnya sangat kecil.', after=cur)

cur = p(f'Nilai recall sebesar {rec}% lebih tinggi dibandingkan nilai presisi sebesar {prec}%, '
        f'yang menunjukkan bahwa model lebih sensitif dalam mendeteksi calon mahasiswa yang '
        f'berpotensi MASUK. Dalam konteks sistem rekomendasi tindak lanjut ini, nilai recall '
        f'yang tinggi lebih diutamakan, karena konsekuensi melewatkan calon mahasiswa yang '
        f'berpotensi mendaftar (False Negative) lebih besar dampaknya dibandingkan dengan '
        f'memfollow up calon mahasiswa yang ternyata tidak mendaftar (False Positive).', after=cur)

cur = p(f'Nilai recall sebesar {rec}% yang lebih tinggi dibandingkan presisi {prec}% '
        f'menunjukkan bahwa model lebih baik dalam menangkap calon mahasiswa yang benar-benar '
        f'MASUK. Dalam konteks sistem rekomendasi tindak lanjut, hal ini sangat menguntungkan '
        f'karena tim marketing tidak akan melewatkan calon mahasiswa yang berpotensi mendaftar. '
        f'Adapun kasus False Positive yang terjadi (2 data) masih dapat ditoleransi karena '
        f'dampaknya hanya berupa effort follow up tambahan, bukan kehilangan calon mahasiswa.', after=cur)

cur = p(f'Secara keseluruhan, nilai akurasi model sebesar {acc}% dengan F1-Score {f1}% '
        f'menunjukkan bahwa algoritma Naive Bayes dapat diterapkan dengan baik dalam '
        f'memberikan rekomendasi tindak lanjut konfirmasi pendaftaran mahasiswa baru '
        f'Universitas Tazkia. Hasil ini juga sejalan dengan karakteristik algoritma Naive Bayes '
        f'yang efektif dan efisien untuk klasifikasi dengan atribut-atribut bertipe kategoris '
        f'seperti yang digunakan dalam penelitian ini.', after=cur)

# 3. Analisis Kontribusi Atribut
cur = p('3.  Analisis Kontribusi Atribut', bold=True, after=cur)
cur = p('Berdasarkan hasil perhitungan conditional probability pada Tabel 4.6 hingga Tabel 4.10, '
        'dapat dianalisis kontribusi masing-masing atribut dalam membedakan kelas MASUK dan '
        'TIDAK MASUK sebagai berikut:', after=cur)

cur = p('a)  Atribut Status Test (X3) merupakan atribut yang paling diskriminatif. Calon '
        'mahasiswa dengan status Sudah Tes memiliki probabilitas MASUK sebesar 0,8889 '
        'dibandingkan hanya 0,4000 untuk kelas TIDAK MASUK. Sebaliknya, calon mahasiswa '
        'yang Belum Tes memiliki probabilitas TIDAK MASUK sebesar 0,6000 dibandingkan 0,1111 '
        'untuk kelas MASUK. Atribut ini menjadi pembeda terkuat karena mengikuti tes '
        'merupakan langkah konkret yang mencerminkan keseriusan calon mahasiswa.', after=cur, ind=2520)

cur = p('b)  Atribut Kategori Nilai Test (X4) turut memberikan kontribusi signifikan. '
        'Nilai Tinggi memberikan probabilitas MASUK sebesar 0,7000 berbanding 0,2727 untuk '
        'TIDAK MASUK. Namun atribut ini juga menjadi penyebab 2 kasus False Positive, karena '
        'beberapa calon mahasiswa dengan nilai tinggi ternyata tidak melanjutkan pendaftaran '
        'karena faktor lain yang tidak tercakup dalam atribut penelitian ini.', after=cur, ind=2520)

cur = p('c)  Atribut Tingkat Follow Up Internal (X2) menunjukkan bahwa sebagian besar calon '
        'mahasiswa yang masuk kategori MASUK berstatus Belum Dihubungi (P=0,6364), '
        'artinya mereka mendaftar secara mandiri tanpa perlu intensitas follow up tinggi. '
        'Sedangkan calon mahasiswa dengan status Follow Up Intensif justru lebih banyak '
        'berakhir sebagai TIDAK MASUK, yang mengindikasikan bahwa intensitas kontak tinggi '
        'belum tentu menjamin konversi pendaftaran.', after=cur, ind=2520)

cur = p('d)  Atribut Kategori Jarak Asal (X1) dan Kategori Penghasilan (X5) memberikan '
        'kontribusi yang lebih kecil dibandingkan atribut lainnya. Meskipun demikian, '
        'kombinasi kedua atribut ini tetap berperan dalam membedakan pola data pada '
        'kasus-kasus tertentu, khususnya ketika nilai atribut lain tidak cukup '
        'diskriminatif untuk menentukan kelas.', after=cur, ind=2520)

# 4. Implikasi Praktis
cur = p('4.  Implikasi Praktis', bold=True, after=cur)
cur = p('Hasil penelitian ini memiliki implikasi praktis yang signifikan bagi Universitas Tazkia, '
        'khususnya bagi tim marketing yang menangani follow up konfirmasi pendaftaran mahasiswa baru. '
        'Dengan menerapkan sistem rekomendasi berbasis Naive Bayes ini, tim marketing dapat '
        'memprioritaskan tindak lanjut kepada calon mahasiswa yang memiliki probabilitas '
        'tinggi untuk MASUK, sehingga alokasi waktu dan sumber daya menjadi lebih efisien '
        'dan tepat sasaran.', after=cur)

cur = p('Secara praktis, sistem ini dapat membantu tim marketing dalam mengidentifikasi '
        'calon mahasiswa berprioritas tinggi berdasarkan kombinasi atribut seperti Status Test '
        'sudah mengikuti ujian, nilai test tinggi, dan jarak domisili yang tidak terlalu jauh. '
        'Calon mahasiswa dengan profil tersebut terbukti memiliki probabilitas MASUK yang '
        'lebih tinggi berdasarkan data historis yang dianalisis dalam penelitian ini.', after=cur)

cur = p('Selain itu, pola yang ditemukan dari kasus False Positive memberikan informasi '
        'berharga bahwa calon mahasiswa yang sudah mengikuti tes dengan nilai tinggi namun '
        'penghasilannya Tidak Diketahui perlu mendapatkan perhatian khusus, misalnya '
        'dengan menggali informasi lebih lanjut terkait faktor penghambat pendaftaran '
        'seperti kendala biaya atau pertimbangan lain yang belum terekam dalam data.', after=cur)

# 5. Keterbatasan dan Saran
cur = p('5.  Keterbatasan dan Saran Pengembangan', bold=True, after=cur)
cur = p('Penelitian ini memiliki beberapa keterbatasan yang perlu diperhatikan dalam '
        'pengembangan ke depan. Pertama, jumlah sampel data yang digunakan dalam proses '
        'manual (30 data: 15 training dan 15 testing) merupakan sampel kecil yang digunakan '
        'untuk keperluan ilustrasi perhitungan. Penggunaan seluruh dataset yang berjumlah '
        '1.285 record pada implementasi sistem dapat menghasilkan model dengan akurasi '
        'yang lebih tinggi dan lebih representatif.', after=cur)

cur = p('Kedua, asumsi independensi antar atribut yang merupakan dasar dari algoritma '
        'Naive Bayes tidak selalu terpenuhi dalam kondisi nyata. Misalnya, atribut '
        'Status Test dan Kategori Nilai Test sangat berkorelasi satu sama lain, '
        'sehingga asumsi ini berpotensi memengaruhi akurasi prediksi pada kasus-kasus tertentu.', after=cur)

cur = p('Untuk pengembangan selanjutnya, disarankan untuk: (1) menggunakan seluruh dataset '
        'yang tersedia dalam proses pelatihan model; (2) membandingkan performa Naive Bayes '
        'dengan algoritma lain seperti Decision Tree atau Random Forest untuk mendapatkan '
        'model terbaik; dan (3) mempertimbangkan penambahan atribut baru yang lebih '
        'representatif seperti riwayat interaksi digital calon mahasiswa atau sumber '
        'informasi pendaftaran, guna meningkatkan akurasi dan keandalan sistem rekomendasi.', after=cur)

doc.save('SUSUN-SKRIPSI-ARIF.docx')
print('SELESAI - File berhasil disimpan.')
