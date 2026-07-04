import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

C_LANE_HDR = '#D0D8E8'
C_LANE_BG1 = '#F7F9FC'
C_LANE_BG2 = '#FFFFFF'
C_ACTION   = '#DDEEFF'
C_ACTION_BD= '#2255AA'
C_ARROW    = '#333333'
C_TEXT     = '#111111'

lane1_x, lane2_x, lane_end = 0.3, 4.8, 9.7
L1 = (lane1_x + lane2_x) / 2   # 2.55
L2 = (lane2_x + lane_end) / 2  # 7.25

def make_fig(title, height=10):
    fig, ax = plt.subplots(figsize=(10, height))
    ax.set_xlim(0, 10); ax.set_ylim(0, height)
    ax.axis('off'); fig.patch.set_facecolor('white')
    lane_top = height - 1.0
    lane_bot = 0.5
    ax.text(5, height - 0.45, title, ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_TEXT)
    ax.add_patch(mpatches.FancyBboxPatch((lane1_x, lane_bot),
        lane_end-lane1_x, lane_top-lane_bot,
        boxstyle='square,pad=0', lw=1.8, edgecolor='#555555', facecolor='none', zorder=2))
    ax.plot([lane2_x, lane2_x], [lane_bot, lane_top], color='#555555', lw=1.2, zorder=2)
    ax.plot([lane1_x, lane_end], [lane_top-0.55, lane_top-0.55], color='#555555', lw=1.2, zorder=2)
    for (x, w) in [(lane1_x, lane2_x-lane1_x), (lane2_x, lane_end-lane2_x)]:
        ax.add_patch(mpatches.FancyBboxPatch((x, lane_top-0.55), w, 0.55,
            boxstyle='square,pad=0', lw=0, facecolor=C_LANE_HDR, zorder=1))
    ax.add_patch(mpatches.FancyBboxPatch((lane1_x, lane_bot),
        lane2_x-lane1_x, lane_top-lane_bot-0.55,
        boxstyle='square,pad=0', lw=0, facecolor=C_LANE_BG1, zorder=1))
    ax.add_patch(mpatches.FancyBboxPatch((lane2_x, lane_bot),
        lane_end-lane2_x, lane_top-lane_bot-0.55,
        boxstyle='square,pad=0', lw=0, facecolor=C_LANE_BG2, zorder=1))
    ax.text(L1, lane_top-0.275, 'Tim Marketing', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_TEXT)
    ax.text(L2, lane_top-0.275, 'Sistem', ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_TEXT)
    y_start = lane_top - 0.55 - 0.45   # posisi aman di bawah header
    return fig, ax, lane_bot, y_start

def action(ax, cx, cy, text, w=3.4, h=0.55):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0.08', lw=1.5, edgecolor=C_ACTION_BD, facecolor=C_ACTION, zorder=4))
    lines = text.split('\n')
    off = 0.10 if len(lines) > 1 else 0
    for i, ln in enumerate(lines):
        ax.text(cx, cy+off-i*0.21, ln, ha='center', va='center',
                fontsize=9.5, color=C_TEXT, zorder=5)

def decision(ax, cx, cy, text, w=2.4, h=0.80):
    ax.add_patch(plt.Polygon([(cx, cy+h/2),(cx+w/2, cy),(cx, cy-h/2),(cx-w/2, cy)],
        closed=True, lw=1.5, edgecolor=C_ACTION_BD, facecolor='#FFF8CC', zorder=4))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=9.5, color=C_TEXT, zorder=5)

def start_node(ax, cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.22, color='#222222', zorder=6))

def end_node(ax, cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.30, color='#222222', fill=False, lw=2.8, zorder=6))
    ax.add_patch(plt.Circle((cx, cy), 0.20, color='#222222', zorder=6))

def arr(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=C_ARROW, lw=1.5), zorder=3)

def lbl(ax, x, y, txt, ha='left'):
    ax.text(x, y, txt, ha=ha, va='center', fontsize=8.5,
            color='#555555', style='italic', zorder=5)

def hline(ax, x1, x2, y):
    ax.plot([x1, x2], [y, y], color=C_ARROW, lw=1.5, zorder=3)

def vline(ax, x, y1, y2):
    ax.plot([x, x], [y1, y2], color=C_ARROW, lw=1.5, zorder=3)

def cross_r(ax, x_from, y_from, x_to, y_to):
    """Panah patah: horizontal dulu ke x_to, lalu vertikal ke y_to."""
    hline(ax, x_from, x_to, y_from)
    arr(ax, x_to, y_from, x_to, y_to)

def save(fig, filename):
    plt.tight_layout(pad=0.2)
    fig.savefig(filename, dpi=180, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f'Saved: {filename}')

# =============================================================================
# 2. LOGOUT
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Logout', height=9)
ya1 = ys - 0.85   # Klik Tombol Logout (Tim Marketing)
ya2 = ya1 - 1.25  # Hapus Sesi (Sistem)
ya3 = ya2 - 1.25  # Tampilkan Halaman Login (Sistem)
ya4 = ya3 - 1.25  # Diarahkan ke Halaman Login (Tim Marketing)
ye  = ya4 - 1.20  # End (Tim Marketing)

start_node(ax, L1, ys)

# Tim Marketing: Klik Tombol Logout
action(ax, L1, ya1, 'Klik Tombol Logout')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

# → Sistem: Hapus Sesi (patah)
cross_r(ax, L1+1.7, ya1, L2, ya2+0.275)
action(ax, L2, ya2, 'Hapus Sesi\nPengguna')

# Sistem: Tampilkan Halaman Login
action(ax, L2, ya3, 'Tampilkan\nHalaman Login')
arr(ax, L2, ya2-0.275, L2, ya3+0.275)

# Balik ke Tim Marketing: diarahkan ke halaman login
action(ax, L1, ya4, 'Diarahkan ke\nHalaman Login')
vline(ax, L2, ya3-0.275, ya4)
arr(ax, L2, ya4, L1+1.7, ya4)

# End
end_node(ax, L1, ye)
arr(ax, L1, ya4-0.275, L1, ye+0.30)

save(fig, 'Activity Diagram Logout.png')

# =============================================================================
# 3. KELOLA DATA PENDAFTAR
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Kelola Data Pendaftar', height=14)
# ys ≈ 12.45
gap = 1.05
ya1 = ys - 0.80
ya2 = ya1 - gap
ya3 = ya2 - gap
ya4 = ya3 - gap
ya5 = ya4 - gap
yd  = ya5 - gap        # decision
cx_ya=6.2; cx_no=8.7
yb  = yd - gap*1.1    # branch actions
ye  = yb - gap*1.1

start_node(ax, L1, ys)
action(ax, L1, ya1, 'Buka Halaman\nData Pendaftar')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

action(ax, L2, ya1, 'Tampilkan Daftar\nData Pendaftar')
hline(ax, L1+1.7, L2-1.7, ya1)
arr(ax, L1+1.7, ya1, L2-1.7, ya1)

action(ax, L1, ya2, 'Klik Tambah\nData Pendaftar')
vline(ax, L2, ya1-0.275, ya2)
arr(ax, L2, ya2, L1+1.7, ya2)

action(ax, L2, ya2, 'Tampilkan Form\nTambah Data')
hline(ax, L1+1.7, L2-1.7, ya2)
arr(ax, L1+1.7, ya2, L2-1.7, ya2)

action(ax, L1, ya3, 'Isi Form\nData Pendaftar')
vline(ax, L2, ya2-0.275, ya3)
arr(ax, L2, ya3, L1+1.7, ya3)

action(ax, L1, ya4, 'Klik Simpan Data')
arr(ax, L1, ya3-0.275, L1, ya4+0.275)

# cross ke Sistem → Decision (patah)
cross_r(ax, L1+1.7, ya4, yd, yd+0.40)
decision(ax, yd, yd, 'Data\nValid?')

# Ya → Simpan & notifikasi
action(ax, cx_ya, yb, 'Simpan Data &\nTampilkan Notifikasi', w=2.8)
vline(ax, yd, yd-0.40, yb+0.275)
hline(ax, yd, cx_ya, yb+0.275)
arr(ax, yd, yb+0.275, cx_ya, yb+0.275)
lbl(ax, yd+0.08, (yd-0.40+yb+0.275)/2, 'Ya')
end_node(ax, cx_ya, ye)
arr(ax, cx_ya, yb-0.275, cx_ya, ye+0.30)

# Tidak → Pesan Error
action(ax, cx_no, yb, 'Tampilkan\nPesan Error', w=1.8)
hline(ax, yd+1.2, cx_no, yd)
vline(ax, cx_no, yd, yb+0.275)
arr(ax, cx_no, yd, cx_no, yb+0.275)
lbl(ax, yd+1.25, yd+0.18, 'Tidak')

# Loop back
vline(ax, cx_no, yb-0.275, lb+0.25)
hline(ax, cx_no, lane1_x+0.18, lb+0.25)
vline(ax, lane1_x+0.18, lb+0.25, ya3)
arr(ax, lane1_x+0.18, ya3, L1-1.7, ya3)

save(fig, 'Activity Diagram Kelola Data Pendaftar.png')

# =============================================================================
# 4. LIHAT HASIL KLASIFIKASI NAIVE BAYES
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Lihat Hasil Klasifikasi Naive Bayes', height=8)
gap = 1.40
ya1 = ys - 0.80; ya2 = ya1-gap; ya4 = ya2; ye = ya2-gap

start_node(ax, L1, ys)
action(ax, L1, ya1, 'Buka Menu Hasil\nKlasifikasi')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

action(ax, L2, ya1, 'Proses Klasifikasi\nNaive Bayes')
hline(ax, L1+1.7, L2-1.7, ya1); arr(ax, L1+1.7, ya1, L2-1.7, ya1)

action(ax, L2, ya2, 'Tampilkan Hasil\nKlasifikasi')
arr(ax, L2, ya1-0.275, L2, ya2+0.275)

action(ax, L1, ya2, 'Lihat Hasil\nKlasifikasi')
vline(ax, L2, ya2-0.275, ya2); arr(ax, L2, ya2, L1+1.7, ya2)

end_node(ax, L1, ye)
arr(ax, L1, ya2-0.275, L1, ye+0.30)

save(fig, 'Activity Diagram Lihat Hasil Klasifikasi.png')

# =============================================================================
# 5. LIHAT REKOMENDASI TINDAK LANJUT
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Lihat Rekomendasi Tindak Lanjut', height=8)
gap = 1.40
ya1 = ys-0.80; ya2 = ya1-gap; ya3 = ya2-gap; ye = ya3-gap

start_node(ax, L1, ys)
action(ax, L1, ya1, 'Buka Menu\nRekomendasi')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

action(ax, L2, ya1, 'Generate Rekomendasi\nTindak Lanjut')
hline(ax, L1+1.7, L2-1.7, ya1); arr(ax, L1+1.7, ya1, L2-1.7, ya1)

action(ax, L2, ya2, 'Tampilkan Rekomendasi\nTindak Lanjut')
arr(ax, L2, ya1-0.275, L2, ya2+0.275)

action(ax, L1, ya2, 'Lihat Rekomendasi\nTindak Lanjut')
vline(ax, L2, ya2-0.275, ya2); arr(ax, L2, ya2, L1+1.7, ya2)

end_node(ax, L1, ye)
arr(ax, L1, ya2-0.275, L1, ye+0.30)

save(fig, 'Activity Diagram Lihat Rekomendasi.png')

# =============================================================================
# 6. LIHAT DETAIL HASIL PREDIKSI
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Lihat Detail Hasil Prediksi', height=8)
gap = 1.40
ya1 = ys-0.80; ya2 = ya1-gap; ya3 = ya2-gap; ye = ya3-gap

start_node(ax, L1, ys)
action(ax, L1, ya1, 'Pilih Data\nPendaftar')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

action(ax, L2, ya1, 'Ambil Detail\nHasil Prediksi')
hline(ax, L1+1.7, L2-1.7, ya1); arr(ax, L1+1.7, ya1, L2-1.7, ya1)

action(ax, L2, ya2, 'Tampilkan Detail\nHasil Prediksi')
arr(ax, L2, ya1-0.275, L2, ya2+0.275)

action(ax, L1, ya2, 'Lihat Detail\nHasil Prediksi')
vline(ax, L2, ya2-0.275, ya2); arr(ax, L2, ya2, L1+1.7, ya2)

end_node(ax, L1, ye)
arr(ax, L1, ya2-0.275, L1, ye+0.30)

save(fig, 'Activity Diagram Lihat Detail Prediksi.png')

# =============================================================================
# 7. CETAK / EXPORT LAPORAN
# =============================================================================
fig, ax, lb, ys = make_fig('Activity Diagram Cetak / Export Laporan', height=10)
gap = 1.10
ya1 = ys-0.80; ya2 = ya1-gap; ya3 = ya2-gap; ya4 = ya3-gap; ya5 = ya4-gap; ye = ya5-1.10

start_node(ax, L1, ys)
action(ax, L1, ya1, 'Buka Menu\nLaporan')
arr(ax, L1, ys-0.22, L1, ya1+0.275)

action(ax, L2, ya1, 'Tampilkan Halaman\nLaporan')
hline(ax, L1+1.7, L2-1.7, ya1); arr(ax, L1+1.7, ya1, L2-1.7, ya1)

action(ax, L1, ya2, 'Pilih Rentang\nData Laporan')
vline(ax, L2, ya1-0.275, ya2); arr(ax, L2, ya2, L1+1.7, ya2)

action(ax, L1, ya3, 'Klik Cetak /\nExport Laporan')
arr(ax, L1, ya2-0.275, L1, ya3+0.275)

action(ax, L2, ya3, 'Generate File\nLaporan (PDF/Excel)')
hline(ax, L1+1.7, L2-1.7, ya3); arr(ax, L1+1.7, ya3, L2-1.7, ya3)

action(ax, L2, ya4, 'Unduh File\nLaporan')
arr(ax, L2, ya3-0.275, L2, ya4+0.275)

action(ax, L1, ya4, 'File Laporan\nTerunduh')
vline(ax, L2, ya4-0.275, ya4); arr(ax, L2, ya4, L1+1.7, ya4)

end_node(ax, L1, ye)
arr(ax, L1, ya4-0.275, L1, ye+0.30)

save(fig, 'Activity Diagram Cetak Export Laporan.png')

print('\nSemua activity diagram selesai!')
