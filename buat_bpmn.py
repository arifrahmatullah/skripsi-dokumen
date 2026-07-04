"""Buat diagram BPMN standar untuk Proses Bisnis Lama dan Baru."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

# ─── Warna ─────────────────────────────────────────────────────────────────
C_POOL   = '#1F4E79'   # header pool/lane
C_TASK   = '#D6E4F0'   # task fill
C_GW     = '#FFF2CC'   # gateway fill
C_START  = '#FFFFFF'   # start event fill
C_END    = '#1F4E79'   # end event fill
C_BD     = '#1F4E79'   # border
C_TXT    = '#1A1A1A'   # text
C_HDR    = '#FFFFFF'   # header text
C_ARR    = '#1F4E79'   # arrow


def draw_start(ax, cx, cy, r=0.22):
    circ = plt.Circle((cx, cy), r, fc=C_START, ec=C_BD, lw=2, zorder=4)
    ax.add_patch(circ)
    circ2 = plt.Circle((cx, cy), r*0.7, fc='none', ec=C_BD, lw=1.2, zorder=4)
    ax.add_patch(circ2)


def draw_end(ax, cx, cy, r=0.22):
    circ = plt.Circle((cx, cy), r, fc=C_END, ec=C_BD, lw=3, zorder=4)
    ax.add_patch(circ)
    circ2 = plt.Circle((cx, cy), r*0.65, fc='none', ec=C_HDR, lw=1.5, zorder=4)
    ax.add_patch(circ2)


def draw_task(ax, cx, cy, text, w=2.0, h=0.7):
    rect = mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.06', lw=1.5,
        edgecolor=C_BD, facecolor=C_TASK, zorder=4)
    ax.add_patch(rect)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8,
            color=C_TXT, fontweight='bold', wrap=True, zorder=5,
            multialignment='center')


def draw_gateway(ax, cx, cy, label='', size=0.36):
    diamond = plt.Polygon(
        [(cx, cy+size), (cx+size, cy), (cx, cy-size), (cx-size, cy)],
        closed=True, fc=C_GW, ec=C_BD, lw=1.5, zorder=4)
    ax.add_patch(diamond)
    # X inside (exclusive gateway)
    ax.plot([cx-size*0.45, cx+size*0.45], [cy-size*0.45, cy+size*0.45],
            color=C_BD, lw=1.2, zorder=5)
    ax.plot([cx+size*0.45, cx-size*0.45], [cy-size*0.45, cy+size*0.45],
            color=C_BD, lw=1.2, zorder=5)
    if label:
        ax.text(cx, cy - size - 0.15, label, ha='center', va='top',
                fontsize=7, color=C_TXT, zorder=5, style='italic')


def arrow(ax, x1, y1, x2, y2, label='', bend=0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=C_ARR, lw=1.4,
                    connectionstyle=f'arc3,rad={bend}'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.08, my+0.08, label, fontsize=7, color=C_ARR,
                ha='left', va='bottom', zorder=6, style='italic')


def pool_header(ax, label, x, y, w, h, lane=False):
    col = '#2E6DA4' if lane else C_POOL
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle='square,pad=0', lw=1.5,
        edgecolor=C_BD, facecolor=col, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=9, color=C_HDR, fontweight='bold', zorder=4)


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — PROSES BISNIS LAMA
# ═══════════════════════════════════════════════════════════════════════════
def buat_proses_lama():
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlim(0, 15); ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_facecolor('#F5F5F5'); fig.patch.set_facecolor('#F5F5F5')

    # Pool border
    pool = mpatches.FancyBboxPatch(
        (0.2, 0.4), 14.6, 5.0,
        boxstyle='square,pad=0', lw=2, edgecolor=C_BD, facecolor='white', zorder=1)
    ax.add_patch(pool)

    # Pool header
    pool_header(ax, 'Proses Bisnis Konfirmasi Pendaftaran Mahasiswa Baru (Lama)',
                0.2, 5.0, 14.6, 0.4)

    # Lane headers
    pool_header(ax, 'Tim Marketing', 0.2, 2.7, 1.2, 2.3, lane=True)
    pool_header(ax, 'Calon Mahasiswa', 0.2, 0.4, 1.2, 2.3, lane=True)

    # Lane divider
    ax.plot([0.2, 14.8], [2.7, 2.7], color=C_BD, lw=1, ls='--', zorder=2)

    # Lane background
    ax.add_patch(mpatches.FancyBboxPatch((1.4, 2.7), 13.4, 2.3,
        boxstyle='square,pad=0', lw=0, facecolor='#EBF5FB', zorder=1))
    ax.add_patch(mpatches.FancyBboxPatch((1.4, 0.4), 13.4, 2.3,
        boxstyle='square,pad=0', lw=0, facecolor='#FDFEFE', zorder=1))

    # ── Tim Marketing lane (y ~ 3.85) ──────────────────────────────────
    Y_TM = 3.85
    Y_CM = 1.55

    draw_start(ax, 2.0, Y_TM)
    draw_task(ax, 4.0, Y_TM, 'Terima & Catat\nData Pendaftar\nSecara Manual', w=2.2)
    draw_task(ax, 6.8, Y_TM, 'Hubungi Calon\nMahasiswa Satu\nPer Satu', w=2.2)
    draw_gateway(ax, 9.4, Y_TM, 'Merespons?')
    draw_task(ax, 11.6, Y_TM, 'Catat Status\n& Arsip Data\nManual', w=2.2)
    draw_task(ax, 13.8, Y_TM, 'Buat Laporan\nManual', w=1.8)
    draw_end(ax, 13.8, Y_CM)

    # ── Calon Mahasiswa lane ────────────────────────────────────────────
    draw_task(ax, 9.4, Y_CM, 'Merespons /\nTidak Merespons', w=2.2)

    # Arrows TM lane
    arrow(ax, 2.22, Y_TM, 3.0-0.05, Y_TM)        # start → terima
    arrow(ax, 5.1,  Y_TM, 5.7,  Y_TM)             # terima → hubungi
    arrow(ax, 7.9,  Y_TM, 9.04, Y_TM)             # hubungi → gateway
    arrow(ax, 9.76, Y_TM, 10.5, Y_TM, 'Ya')       # gw → catat
    arrow(ax, 12.7, Y_TM, 12.9, Y_TM)             # catat → laporan
    # gateway bawah → tidak merespons → catat
    arrow(ax, 9.4, Y_TM-0.36, 9.4, Y_CM+0.35)     # gw → calon mahasiswa
    arrow(ax, 9.4, Y_CM-0.35, 9.4, Y_TM-0.7, 'Tidak')  # cm → loop back
    # laporan → end
    arrow(ax, 13.8, Y_TM-0.35, 13.8, Y_CM+0.22)

    ax.text(7.5, 5.55, 'Proses Bisnis Lama — Konfirmasi Pendaftaran Mahasiswa Baru',
            ha='center', va='center', fontsize=11, fontweight='bold', color=C_POOL)

    plt.tight_layout(pad=0.3)
    plt.savefig('Proses Bisnis Lama.png', dpi=150, bbox_inches='tight',
                facecolor='#F5F5F5')
    plt.close()
    print("Saved: Proses Bisnis Lama.png")


# ═══════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — PROSES BISNIS BARU
# ═══════════════════════════════════════════════════════════════════════════
def buat_proses_baru():
    fig, ax = plt.subplots(figsize=(17, 7))
    ax.set_xlim(0, 17); ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_facecolor('#F5F5F5'); fig.patch.set_facecolor('#F5F5F5')

    # Pool border
    pool = mpatches.FancyBboxPatch(
        (0.2, 0.4), 16.6, 6.2,
        boxstyle='square,pad=0', lw=2, edgecolor=C_BD, facecolor='white', zorder=1)
    ax.add_patch(pool)

    # Pool header
    pool_header(ax, 'Proses Bisnis Konfirmasi Pendaftaran Mahasiswa Baru (Baru — dengan Sistem Naive Bayes)',
                0.2, 6.2, 16.6, 0.4)

    # Lane headers
    pool_header(ax, 'Tim Marketing', 0.2, 3.9, 1.2, 2.7, lane=True)
    pool_header(ax, 'Sistem', 0.2, 0.4, 1.2, 3.5, lane=True)

    # Lane divider
    ax.plot([0.2, 16.8], [3.9, 3.9], color=C_BD, lw=1, ls='--', zorder=2)

    # Lane backgrounds
    ax.add_patch(mpatches.FancyBboxPatch((1.4, 3.9), 15.4, 2.7,
        boxstyle='square,pad=0', lw=0, facecolor='#EBF5FB', zorder=1))
    ax.add_patch(mpatches.FancyBboxPatch((1.4, 0.4), 15.4, 3.5,
        boxstyle='square,pad=0', lw=0, facecolor='#F4F9F4', zorder=1))

    Y_TM = 5.25    # Tim Marketing
    Y_SIS = 2.1    # Sistem

    # Tim Marketing lane
    draw_start(ax, 2.0, Y_TM)
    draw_task(ax, 3.8, Y_TM, 'Input / Upload\nData Pendaftar', w=2.0)
    draw_task(ax, 6.8, Y_TM, 'Lihat Rekomendasi\nTindak Lanjut', w=2.2)
    draw_task(ax, 9.8, Y_TM, 'Lakukan Follow Up\nSesuai Rekomendasi', w=2.4)
    draw_gateway(ax, 12.5, Y_TM, 'Calon\nMasuk?')
    draw_task(ax, 14.8, Y_TM, 'Cetak / Export\nLaporan', w=2.0)
    draw_end(ax, 14.8, Y_SIS-0.5)

    # Sistem lane
    draw_task(ax, 3.8, Y_SIS, 'Validasi &\nSimpan Data', w=2.0)
    draw_task(ax, 6.8, Y_SIS, 'Jalankan Algoritma\nNaive Bayes', w=2.2)
    draw_task(ax, 9.8, Y_SIS, 'Generate Rekomendasi\nTindak Lanjut', w=2.4)
    draw_task(ax, 12.5, Y_SIS, 'Update Status\nPendaftar', w=2.0)

    # Arrows
    arrow(ax, 2.22, Y_TM, 2.8, Y_TM)                    # start → input
    arrow(ax, 3.8, Y_TM-0.35, 3.8, Y_SIS+0.35)          # input TM → validasi SIS
    arrow(ax, 4.8, Y_SIS, 5.7, Y_SIS)                    # validasi → NB
    arrow(ax, 7.9, Y_SIS, 8.6, Y_SIS)                    # NB → generate
    arrow(ax, 9.8, Y_SIS+0.35, 9.8, Y_TM-0.35)           # generate → lihat TM
    arrow(ax, 7.9, Y_TM, 8.6, Y_TM)                      # lihat → follow up
    arrow(ax, 11.0, Y_TM, 11.82, Y_TM)                   # follow up → gateway
    arrow(ax, 12.5, Y_TM-0.36, 12.5, Y_SIS+0.35, 'Ya / Tidak')  # gw → update
    arrow(ax, 13.5, Y_SIS, 13.8, Y_SIS)                  # update → laporan (sys)
    arrow(ax, 13.5, Y_TM, 13.8, Y_TM, 'Selesai')         # gw → laporan TM
    arrow(ax, 14.8, Y_TM-0.35, 14.8, Y_SIS-0.15)         # laporan → end

    ax.text(8.5, 6.75, 'Proses Bisnis Baru — Konfirmasi Pendaftaran Mahasiswa Baru dengan Sistem Rekomendasi Naive Bayes',
            ha='center', va='center', fontsize=10, fontweight='bold', color=C_POOL)

    plt.tight_layout(pad=0.3)
    plt.savefig('Proses Bisnis Baru.png', dpi=150, bbox_inches='tight',
                facecolor='#F5F5F5')
    plt.close()
    print("Saved: Proses Bisnis Baru.png")


buat_proses_lama()
buat_proses_baru()
print("SELESAI - Kedua diagram BPMN berhasil dibuat.")
