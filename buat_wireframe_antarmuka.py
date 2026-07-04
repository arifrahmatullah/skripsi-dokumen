"""
Wireframe rancangan antarmuka (low-fidelity mockup) untuk Bab 4
"3. Perancangan Desain Antarmuka" - Sistem Rekomendasi Tindak Lanjut
Konfirmasi Pendaftaran Mahasiswa Baru.

Gaya visual disamakan dengan Activity/Sequence Diagram yang sudah ada
(palet warna biru-abu).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle

C_HEADER   = '#D0D8E8'
C_SIDEBAR  = '#F7F9FC'
C_ACTIVE   = '#DDEEFF'
C_ACCENT   = '#2255AA'
C_BORDER   = '#555555'
C_TEXT     = '#111111'
C_MUTED    = '#8892A0'
C_ROWALT   = '#F7F9FC'
C_CHROME   = '#E8E8E8'
C_GREEN    = '#2E9E5B'
C_GRAY     = '#9AA3AF'

MENU_ITEMS = ['Dashboard', 'Data Pendaftar', 'Hasil Klasifikasi',
              'Rekomendasi', 'Laporan', 'Logout']

W, H = 10.0, 7.2


def browser_chrome(ax):
    ax.add_patch(Rectangle((0, H - 0.35), W, 0.35, facecolor=C_CHROME,
                            edgecolor=C_BORDER, lw=1.2, zorder=1))
    for i, cx in enumerate([0.28, 0.52, 0.76]):
        ax.add_patch(Circle((cx, H - 0.175), 0.075, facecolor=C_GRAY,
                             edgecolor='none', zorder=2))
    ax.add_patch(FancyBboxPatch((1.3, H - 0.29), 5.0, 0.23,
                                 boxstyle='round,pad=0.02', lw=0.8,
                                 edgecolor=C_MUTED, facecolor='white', zorder=2))
    ax.text(1.5, H - 0.175, 'sipmb-tazkia.ac.id', ha='left', va='center',
            fontsize=6.5, color=C_MUTED, zorder=3)
    ax.add_patch(Rectangle((0, 0), W, H, facecolor='none',
                            edgecolor=C_BORDER, lw=1.4, zorder=10))


def app_header(ax, y_top):
    ax.add_patch(Rectangle((0, y_top - 0.6), W, 0.6, facecolor=C_HEADER,
                            edgecolor=C_BORDER, lw=1.0, zorder=2))
    ax.text(0.35, y_top - 0.3, 'SI-PMB  |  Rekomendasi Tindak Lanjut',
            ha='left', va='center', fontsize=10, fontweight='bold',
            color=C_TEXT, zorder=3)
    ax.add_patch(Circle((W - 0.85, y_top - 0.3), 0.16, facecolor='white',
                         edgecolor=C_ACCENT, lw=1.2, zorder=3))
    ax.text(W - 0.55, y_top - 0.3, 'Tim Marketing', ha='left', va='center',
            fontsize=7.5, color=C_TEXT, zorder=3)
    return y_top - 0.6


def sidebar(ax, y_top, y_bot, active):
    x0, x1 = 0, 2.3
    ax.add_patch(Rectangle((x0, y_bot), x1 - x0, y_top - y_bot,
                            facecolor=C_SIDEBAR, edgecolor=C_BORDER, lw=1.0, zorder=2))
    n = len(MENU_ITEMS)
    row_h = (y_top - y_bot) / (n + 0.5)
    for i, item in enumerate(MENU_ITEMS):
        cy = y_top - 0.35 - i * row_h
        if item == active:
            ax.add_patch(Rectangle((x0, cy - row_h / 2 + 0.05), x1 - x0,
                                    row_h - 0.1, facecolor=C_ACTIVE, edgecolor='none', zorder=3))
            ax.add_patch(Rectangle((x0, cy - row_h / 2 + 0.05), 0.06,
                                    row_h - 0.1, facecolor=C_ACCENT, edgecolor='none', zorder=4))
        ax.add_patch(Rectangle((x0 + 0.25, cy - 0.09), 0.18, 0.18,
                                facecolor=C_GRAY if item != active else C_ACCENT,
                                edgecolor='none', zorder=4))
        ax.text(x0 + 0.55, cy, item, ha='left', va='center', fontsize=8,
                fontweight='bold' if item == active else 'normal',
                color=C_ACCENT if item == active else C_TEXT, zorder=4)
    return x1


def page_title(ax, x0, y_top, text):
    ax.text(x0 + 0.35, y_top - 0.35, text, ha='left', va='center',
            fontsize=11, fontweight='bold', color=C_TEXT, zorder=3)
    ax.plot([x0 + 0.35, W - 0.35], [y_top - 0.55, y_top - 0.55],
            color=C_BORDER, lw=0.8, zorder=3)


def button(ax, cx, cy, w, h, label, filled=True):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                 boxstyle='round,pad=0.05', lw=1.3,
                                 edgecolor=C_ACCENT,
                                 facecolor=C_ACCENT if filled else 'white', zorder=5))
    ax.text(cx, cy, label, ha='center', va='center', fontsize=7.8,
            fontweight='bold', color='white' if filled else C_ACCENT, zorder=6)


def input_field(ax, x, y, w, label, h=0.32):
    ax.text(x, y + 0.24, label, ha='left', va='bottom', fontsize=7.3,
            color=C_TEXT, zorder=4)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle='round,pad=0.02',
                                 lw=1.0, edgecolor=C_MUTED, facecolor='white', zorder=4))


def table(ax, x0, y_top, x1, headers, rows, row_h=0.34, badge_col=None):
    n_cols = len(headers)
    col_w = (x1 - x0) / n_cols
    ax.add_patch(Rectangle((x0, y_top - row_h), x1 - x0, row_h,
                            facecolor=C_HEADER, edgecolor=C_BORDER, lw=0.9, zorder=3))
    for c, htext in enumerate(headers):
        ax.text(x0 + c * col_w + 0.08, y_top - row_h / 2, htext, ha='left',
                va='center', fontsize=6.6, fontweight='bold', color=C_TEXT, zorder=4)
    for r, row in enumerate(rows):
        ry = y_top - row_h - (r + 1) * row_h
        if r % 2 == 1:
            ax.add_patch(Rectangle((x0, ry), x1 - x0, row_h, facecolor=C_ROWALT,
                                    edgecolor='none', zorder=2))
        ax.plot([x0, x1], [ry, ry], color='#D8DCE3', lw=0.6, zorder=3)
        for c, val in enumerate(row):
            if badge_col is not None and c == badge_col:
                is_masuk = 'TIDAK' not in val.upper()
                bg = C_GREEN if is_masuk else C_GRAY
                bw = col_w * 0.65
                ax.add_patch(FancyBboxPatch((x0 + c * col_w + 0.05, ry + row_h * 0.18),
                                             bw, row_h * 0.64, boxstyle='round,pad=0.02',
                                             lw=0, facecolor=bg, zorder=4))
                ax.text(x0 + c * col_w + 0.05 + bw / 2, ry + row_h / 2, val,
                        ha='center', va='center', fontsize=6.2, color='white',
                        fontweight='bold', zorder=5)
            else:
                ax.text(x0 + c * col_w + 0.08, ry + row_h / 2, val, ha='left',
                        va='center', fontsize=6.5, color=C_TEXT, zorder=4)
    return y_top - row_h - len(rows) * row_h


def card(ax, cx, cy, w, h, big, label, color=C_ACCENT):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                 boxstyle='round,pad=0.04', lw=1.2,
                                 edgecolor=color, facecolor='white', zorder=4))
    ax.add_patch(Rectangle((cx - w / 2, cy + h / 2 - 0.08), w, 0.08,
                            facecolor=color, edgecolor='none', zorder=5))
    ax.text(cx, cy + 0.12, big, ha='center', va='center', fontsize=13,
            fontweight='bold', color=color, zorder=5)
    ax.text(cx, cy - 0.22, label, ha='center', va='center', fontsize=7,
            color=C_TEXT, zorder=5)


def prob_bar(ax, x, y, w, frac, label, color=C_ACCENT):
    ax.text(x, y + 0.16, label, ha='left', va='bottom', fontsize=6.8, color=C_TEXT, zorder=4)
    ax.add_patch(FancyBboxPatch((x, y - 0.1), w, 0.18, boxstyle='round,pad=0.01',
                                 lw=0.6, edgecolor=C_MUTED, facecolor='#EDEFF3', zorder=3))
    ax.add_patch(FancyBboxPatch((x, y - 0.1), w * frac, 0.18, boxstyle='round,pad=0.01',
                                 lw=0, facecolor=color, zorder=4))
    ax.text(x + w + 0.1, y - 0.01, f'{frac:.2%}', ha='left', va='center',
            fontsize=6.8, color=C_TEXT, zorder=4)


def base_fig(title, active_menu=None):
    fig, ax = plt.subplots(figsize=(10, 7.2))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')
    browser_chrome(ax)
    y_after_header = app_header(ax, H - 0.35)
    if active_menu:
        sidebar(ax, y_after_header, 0, active_menu)
        content_x0 = 2.3
    else:
        content_x0 = 0
    page_title(ax, content_x0, y_after_header, title)
    return fig, ax, content_x0, y_after_header


def save(fig, name):
    fig.savefig(name, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {name}')


# ══════════════════════════════════════════════════════════════════════════
# 1) Interface Login
# ══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 7.2))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
fig.patch.set_facecolor('white')
browser_chrome(ax)
ax.add_patch(Rectangle((0, 0), W, H - 0.35, facecolor='#EAF0FB', edgecolor='none', zorder=1))
cx, cy = W / 2, (H - 0.35) / 2
ax.add_patch(FancyBboxPatch((cx - 2.1, cy - 2.3), 4.2, 4.6, boxstyle='round,pad=0.06',
                             lw=1.4, edgecolor=C_ACCENT, facecolor='white', zorder=3))
ax.add_patch(Circle((cx, cy + 1.75), 0.42, facecolor=C_HEADER, edgecolor=C_ACCENT, lw=1.3, zorder=4))
ax.text(cx, cy + 1.75, 'LOGO', ha='center', va='center', fontsize=7.5,
        fontweight='bold', color=C_ACCENT, zorder=5)
ax.text(cx, cy + 1.15, 'SI-PMB Tazkia', ha='center', va='center', fontsize=11,
        fontweight='bold', color=C_TEXT, zorder=4)
ax.text(cx, cy + 0.85, 'Rekomendasi Tindak Lanjut Konfirmasi Pendaftaran',
        ha='center', va='center', fontsize=6.8, color=C_MUTED, zorder=4)
input_field(ax, cx - 1.7, cy + 0.25, 3.4, 'Username')
input_field(ax, cx - 1.7, cy - 0.45, 3.4, 'Password')
button(ax, cx, cy - 1.15, 2.0, 0.4, 'LOGIN')
ax.text(cx, cy - 1.85, '© 2026 Universitas Tazkia', ha='center', va='center',
        fontsize=6, color=C_MUTED, zorder=4)
save(fig, 'Interface Login.png')

# ══════════════════════════════════════════════════════════════════════════
# 2) Interface Menu Utama / Dashboard
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Dashboard', active_menu='Dashboard')
cards = [('1.285', 'Total Pendaftar', C_ACCENT), ('241', 'Prediksi MASUK', C_GREEN),
         ('787', 'Prediksi TIDAK MASUK', C_GRAY), ('93,77%', 'Akurasi Model', C_ACCENT)]
cw = (W - x0 - 0.7) / 4
for i, (big, label, col) in enumerate(cards):
    ccx = x0 + 0.35 + cw * i + cw / 2 - 0.1
    card(ax, ccx, yh - 1.15, cw - 0.25, 1.2, big, label, color=col)
ax.text(x0 + 0.35, yh - 2.05, 'Ringkasan Prediksi Terbaru', ha='left', va='center',
        fontsize=8.5, fontweight='bold', color=C_TEXT, zorder=4)
headers = ['No', 'Nama Pendaftar', 'Status Test', 'Nilai Test', 'Prediksi']
rows = [
    ['1', 'Sandy Akbar H.', 'Belum Tes', 'Tidak Ada Nilai', 'TIDAK MASUK'],
    ['2', 'Nazwa Nur Ali...', 'Sudah Tes', 'Nilai Tinggi', 'MASUK'],
    ['3', 'Harri Firmansyah', 'Sudah Tes', 'Nilai Tinggi', 'MASUK'],
    ['4', 'Amaliyah M.', 'Belum Tes', 'Tidak Ada Nilai', 'TIDAK MASUK'],
]
table(ax, x0 + 0.35, yh - 2.25, W - 0.35, headers, rows, badge_col=4)
save(fig, 'Interface Menu Utama.png')

# ══════════════════════════════════════════════════════════════════════════
# 3) Interface Data Pendaftar (List)
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Data Pendaftar', active_menu='Data Pendaftar')
input_field(ax, x0 + 0.35, yh - 0.55, 3.0, '', h=0.32)
ax.text(x0 + 0.5, yh - 0.7, 'Cari nama pendaftar...', ha='left', va='center',
        fontsize=6.8, color=C_MUTED, zorder=5)
button(ax, W - 1.2, yh - 0.7, 1.7, 0.34, '+ Tambah Data')
headers = ['No', 'Nama', 'Jarak', 'Follow Up', 'Status Test', 'Nilai Test', 'Aksi']
rows = [
    ['1', 'Sandy Akbar H.', 'Dekat', 'Belum Dihubungi', 'Belum Tes', 'Tidak Ada Nilai', 'Edit | Hapus'],
    ['2', 'Amaliyah M.', 'Sedang', 'Belum Dihubungi', 'Belum Tes', 'Tidak Ada Nilai', 'Edit | Hapus'],
    ['3', 'TB Fathurrahman', 'Jauh', 'Belum Dihubungi', 'Belum Tes', 'Tidak Ada Nilai', 'Edit | Hapus'],
    ['4', 'Widia wati', 'Dekat', 'Follow Up Intensif', 'Belum Tes', 'Tidak Ada Nilai', 'Edit | Hapus'],
    ['5', 'Nazwa Nur Ali...', 'Dekat', 'Belum Dihubungi', 'Sudah Tes', 'Nilai Tinggi', 'Edit | Hapus'],
]
y_end = table(ax, x0 + 0.35, yh - 1.05, W - 0.35, headers, rows)
ax.text(x0 + 0.35, y_end - 0.25, 'Menampilkan 1-5 dari 1.285 data', fontsize=6.5,
        color=C_MUTED, ha='left', va='center', zorder=4)
for i, lbl in enumerate(['<', '1', '2', '3', '>']):
    button(ax, W - 1.6 + i * 0.4, y_end - 0.25, 0.32, 0.28, lbl, filled=(lbl == '1'))
save(fig, 'Interface Data Pendaftar.png')

# ══════════════════════════════════════════════════════════════════════════
# 4) Interface Tambah / Edit Data Pendaftar (Form)
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Tambah Data Pendaftar', active_menu='Data Pendaftar')
fields = ['Nama Pendaftar', 'Kategori Jarak Asal', 'Tingkat Follow Up Internal',
          'Status Test', 'Kategori Nilai Test', 'Kategori Penghasilan']
fx = x0 + 0.4
fw = (W - x0 - 0.8 - 0.3) / 2
for i, f in enumerate(fields):
    col = i % 2
    row = i // 2
    fxx = fx + col * (fw + 0.3)
    fyy = yh - 0.95 - row * 0.75
    input_field(ax, fxx, fyy, fw, f)
button(ax, fx + fw / 2, yh - 0.95 - 3 * 0.75 - 0.15, 1.6, 0.36, 'Simpan', filled=True)
button(ax, fx + fw + 0.3 + fw / 2, yh - 0.95 - 3 * 0.75 - 0.15, 1.6, 0.36, 'Batal', filled=False)
save(fig, 'Interface Tambah Edit Data Pendaftar.png')

# ══════════════════════════════════════════════════════════════════════════
# 5) Interface Hasil Klasifikasi Naive Bayes
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Hasil Klasifikasi Naive Bayes', active_menu='Hasil Klasifikasi')
headers = ['No', 'Nama', 'P(MASUK|X)', 'P(TDK MSK|X)', 'Prediksi']
rows = [
    ['1', 'Nazwa Nur Ali...', '1.000000', '0.000000', 'MASUK'],
    ['2', 'Harri Firmansyah', '0.938000', '0.062000', 'MASUK'],
    ['3', 'Zahrotul Mufida...', '1.000000', '0.000000', 'MASUK'],
    ['4', 'Nurul Sadira M.', '0.000000', '1.000000', 'TIDAK MASUK'],
    ['5', 'Antoni', '0.000000', '1.000000', 'TIDAK MASUK'],
]
y_end = table(ax, x0 + 0.35, yh - 0.55, W - 0.35, headers, rows, badge_col=4)
button(ax, W - 1.2, yh - 0.35, 1.6, 0.32, 'Proses Ulang')
ax.text(x0 + 0.35, y_end - 0.3, 'Akurasi Model: 93,77%   |   Presisi: 78,95%   |   Recall: 100,00%',
        fontsize=7, color=C_ACCENT, fontweight='bold', ha='left', va='center', zorder=4)
save(fig, 'Interface Hasil Klasifikasi.png')

# ══════════════════════════════════════════════════════════════════════════
# 6) Interface Rekomendasi Tindak Lanjut
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Rekomendasi Tindak Lanjut', active_menu='Rekomendasi')
recs = [
    ('Nazwa Nur Ali...', 'MASUK', 'Prioritas Tinggi - Segera hubungi', C_GREEN),
    ('Harri Firmansyah', 'MASUK', 'Prioritas Tinggi - Segera hubungi', C_GREEN),
    ('Sandy Akbar H.', 'TIDAK MASUK', 'Prioritas Rendah - Follow up lanjutan', C_GRAY),
    ('Amaliyah M.', 'TIDAK MASUK', 'Prioritas Rendah - Follow up lanjutan', C_GRAY),
]
ry = yh - 0.5
for nama, pred, rec, col in recs:
    ax.add_patch(FancyBboxPatch((x0 + 0.35, ry - 0.55), W - 0.7, 0.5,
                                 boxstyle='round,pad=0.03', lw=1.0,
                                 edgecolor='#D8DCE3', facecolor='white', zorder=3))
    ax.add_patch(Rectangle((x0 + 0.35, ry - 0.55), 0.08, 0.5, facecolor=col,
                            edgecolor='none', zorder=4))
    ax.text(x0 + 0.6, ry - 0.2, nama, ha='left', va='center', fontsize=8,
            fontweight='bold', color=C_TEXT, zorder=4)
    ax.text(x0 + 0.6, ry - 0.42, rec, ha='left', va='center', fontsize=6.8,
            color=C_MUTED, zorder=4)
    ax.add_patch(FancyBboxPatch((W - 2.1, ry - 0.4), 1.5, 0.28, boxstyle='round,pad=0.02',
                                 lw=0, facecolor=col, zorder=4))
    ax.text(W - 1.35, ry - 0.26, pred, ha='center', va='center', fontsize=6.8,
            color='white', fontweight='bold', zorder=5)
    ry -= 0.7
save(fig, 'Interface Rekomendasi.png')

# ══════════════════════════════════════════════════════════════════════════
# 7) Interface Detail Prediksi
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('', active_menu='Hasil Klasifikasi')
button(ax, x0 + 0.85, yh - 0.35, 1.1, 0.32, '< Kembali', filled=False)
ax.text(x0 + 1.65, yh - 0.35, 'Detail Prediksi - Nazwa Nur Ali...', ha='left', va='center',
        fontsize=11, fontweight='bold', color=C_TEXT, zorder=3)
attrs = ['Kategori Jarak Asal : Dekat', 'Tingkat Follow Up : Belum Dihubungi',
         'Status Test : Sudah Tes', 'Kategori Nilai Test : Nilai Tinggi',
         'Kategori Penghasilan : Diatas Rp.6.000.000']
ay = yh - 0.85
for a in attrs:
    ax.text(x0 + 0.35, ay, '•  ' + a, ha='left', va='center', fontsize=7, color=C_TEXT, zorder=4)
    ay -= 0.28
ax.text(x0 + 0.35, ay - 0.15, 'Rincian Probabilitas', fontsize=8, fontweight='bold',
        color=C_TEXT, ha='left', va='center', zorder=4)
by = ay - 0.5
prob_bar(ax, x0 + 0.35, by, 3.0, 0.2344, 'Prior P(MASUK)')
prob_bar(ax, x0 + 0.35, by - 0.4, 3.0, 0.30, 'P(Jarak=Dekat | MASUK)')
prob_bar(ax, x0 + 0.35, by - 0.8, 3.0, 0.45, 'P(Status Test=Sudah Tes | MASUK)')
prob_bar(ax, x0 + 0.35, by - 1.2, 3.0, 1.00, 'Posterior P(MASUK|X)', color=C_GREEN)
ax.add_patch(FancyBboxPatch((W - 2.6, by + 0.25), 2.0, 0.5, boxstyle='round,pad=0.03',
                             lw=0, facecolor=C_GREEN, zorder=4))
ax.text(W - 1.6, by + 0.5, 'PREDIKSI: MASUK', ha='center', va='center', fontsize=8.5,
        fontweight='bold', color='white', zorder=5)
save(fig, 'Interface Detail Prediksi.png')

# ══════════════════════════════════════════════════════════════════════════
# 8) Interface Cetak / Export Laporan
# ══════════════════════════════════════════════════════════════════════════
fig, ax, x0, yh = base_fig('Cetak / Export Laporan', active_menu='Laporan')
input_field(ax, x0 + 0.4, yh - 0.95, 2.0, 'Tanggal Dari')
input_field(ax, x0 + 2.6, yh - 0.95, 2.0, 'Tanggal Sampai')
input_field(ax, x0 + 4.8, yh - 0.95, 2.0, 'Status Prediksi')
button(ax, W - 2.85, yh - 1.65, 1.5, 0.34, 'Export PDF')
button(ax, W - 1.15, yh - 1.65, 1.6, 0.34, 'Export Excel')
headers = ['No', 'Nama', 'Prediksi', 'Tgl. Follow Up']
rows = [
    ['1', 'Nazwa Nur Ali...', 'MASUK', '02-07-2026'],
    ['2', 'Harri Firmansyah', 'MASUK', '02-07-2026'],
    ['3', 'Sandy Akbar H.', 'TIDAK MASUK', '01-07-2026'],
]
table(ax, x0 + 0.35, yh - 2.05, W - 0.35, headers, rows, badge_col=2)
save(fig, 'Interface Cetak Export Laporan.png')

print('\nSemua 8 wireframe berhasil dibuat.')
