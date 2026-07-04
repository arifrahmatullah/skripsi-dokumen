import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.lines as mlines

C_TXT    = '#111111'
C_ARR    = '#333333'
C_BOX_BD = '#333333'
C_ACT    = '#C5E3D6'   # activation bar fill (mint)
C_ACT_BD = '#4A9A7A'   # activation bar border
C_ALT_BD = '#555555'
C_FRAME  = '#333333'

# ── Drawing helpers ───────────────────────────────────────────────────────────

def draw_actor(ax, x, y_top, name):
    """UML stick figure; returns bottom-of-legs y."""
    hr = 0.20
    hy = y_top - hr
    ax.add_patch(plt.Circle((x, hy), hr, color='none', ec=C_BOX_BD, lw=1.5, zorder=5))
    by1 = hy - hr
    by2 = by1 - 0.42
    ax.plot([x, x], [by1, by2], color=C_BOX_BD, lw=1.5, zorder=5)
    arm_y = by1 - 0.16
    ax.plot([x-0.24, x+0.24], [arm_y, arm_y], color=C_BOX_BD, lw=1.5, zorder=5)
    ax.plot([x, x-0.20], [by2, by2-0.28], color=C_BOX_BD, lw=1.5, zorder=5)
    ax.plot([x, x+0.20], [by2, by2-0.28], color=C_BOX_BD, lw=1.5, zorder=5)
    ax.text(x, by2-0.34, name, ha='center', va='top',
            fontsize=8, color=C_TXT, zorder=5)
    return by2 - 0.28


def draw_box(ax, x, y_top, name, bw=1.9, bh=0.55):
    """Rectangular participant box; returns bottom y."""
    ax.add_patch(FancyBboxPatch((x-bw/2, y_top-bh), bw, bh,
        boxstyle='square,pad=0', lw=1.5,
        edgecolor=C_BOX_BD, facecolor='white', zorder=4))
    lines = name.split('\n')
    nl = len(lines)
    for li, ln in enumerate(lines):
        off = (0.5-li)*0.17 if nl > 1 else 0
        ax.text(x, y_top-bh/2+off, ln, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=C_TXT, zorder=5)
    return y_top - bh


def act_bar(ax, x, y_top, y_bot, w=0.18):
    """Draw activation bar on lifeline."""
    ax.add_patch(mpatches.FancyBboxPatch(
        (x-w/2, y_bot), w, y_top-y_bot,
        boxstyle='square,pad=0', lw=1.0,
        edgecolor=C_ACT_BD, facecolor=C_ACT, zorder=3))


def arrow_msg(ax, x1, y, x2, dashed=False, label='', lbl_above=True):
    """Draw horizontal message arrow with optional label."""
    if dashed:
        d = 1 if x2 > x1 else -1
        ax.plot([x1, x2 - d*0.16], [y, y],
                color=C_ARR, lw=1.2, linestyle='--', zorder=3)
        ax.annotate('', xy=(x2, y), xytext=(x2-d*0.16, y),
                    arrowprops=dict(arrowstyle='->', color=C_ARR, lw=1.2), zorder=3)
    else:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=C_ARR, lw=1.2), zorder=3)
    if label:
        xm = (x1+x2)/2
        dy = 0.10 if lbl_above else -0.12
        ax.text(xm, y+dy, label, ha='center',
                va='bottom' if lbl_above else 'top',
                fontsize=8, color=C_TXT, zorder=5,
                style='italic' if dashed else 'normal')


# ── Main draw function ────────────────────────────────────────────────────────

def draw_seq(title, parts, msgs,
             alt_blocks=None, activations=None,
             height=12, width=14, fname=None):
    """
    parts   : list of dicts  {'name': str, 'type': 'actor'|'box'}
    msgs    : list of dicts  {'from': int, 'to': int, 'text': str, 'ret': bool}
    alt_blocks : list {'label':str, 'start':int, 'end':int, 'dividers':[int],
                        'sub_labels':[str]}
    activations: list {'part': int, 'start': int, 'end': int}
                 (msg indices; bar spans from start-arrow to end-arrow)
    """
    n = len(parts)
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # ── SD outer frame ────────────────────────────────────────────────────────
    frame_m = 0.15
    ax.add_patch(mpatches.FancyBboxPatch(
        (frame_m, frame_m), width-2*frame_m, height-2*frame_m,
        boxstyle='square,pad=0', lw=1.5,
        edgecolor=C_FRAME, facecolor='none', zorder=1))
    sd_lbl = f'sd  {title}'
    sd_tw = len(sd_lbl)*0.085 + 0.25
    ax.add_patch(mpatches.FancyBboxPatch(
        (frame_m, height-frame_m-0.40), sd_tw, 0.40,
        boxstyle='square,pad=0', lw=1.5,
        edgecolor=C_FRAME, facecolor='white', zorder=2))
    ax.text(frame_m+0.12, height-frame_m-0.20, sd_lbl, ha='left', va='center',
            fontsize=8.5, color=C_TXT, zorder=3)

    # ── Participant x-positions ───────────────────────────────────────────────
    margin_x = 1.1
    spacing  = (width - 2*margin_x) / (n-1) if n > 1 else 0
    xs = [margin_x + i*spacing for i in range(n)]

    part_top = height - 0.75    # top y for participant headers

    # ── Draw participant headers & record lifeline start ──────────────────────
    ll_starts = []
    for i, (x, p) in enumerate(zip(xs, parts)):
        if p.get('type') == 'actor':
            ll_y = draw_actor(ax, x, part_top, p['name'])
        else:
            ll_y = draw_box(ax, x, part_top, p['name'])
        ll_starts.append(ll_y)

    ll_top = min(ll_starts)
    ll_bot = 0.55

    # Lifelines
    for x in xs:
        ax.plot([x, x], [ll_top, ll_bot], color='#888888', lw=1.0,
                linestyle=(0, (6, 4)), zorder=2)

    # ── Y positions for messages ──────────────────────────────────────────────
    n_msg   = len(msgs)
    total_h = ll_top - 0.35 - ll_bot
    step    = total_h / (n_msg + 0.5)
    y0      = ll_top - 0.30
    ys      = [y0 - i*step for i in range(n_msg)]

    # ── Alt / opt frames ──────────────────────────────────────────────────────
    if alt_blocks:
        for blk in alt_blocks:
            si, ei = blk['start'], blk['end']
            yt = ys[si] + step*0.55
            yb = ys[ei] - step*0.45
            fw = width - 2*frame_m - 0.1
            fx = frame_m + 0.05

            ax.add_patch(mpatches.FancyBboxPatch(
                (fx, yb), fw, yt-yb,
                boxstyle='square,pad=0', lw=1.2,
                edgecolor=C_ALT_BD, facecolor='none', zorder=2))

            tlbl = blk.get('label', 'alt')
            tw = max(len(tlbl)*0.12+0.25, 0.75)
            ax.add_patch(mpatches.FancyBboxPatch(
                (fx, yt-0.30), tw, 0.30,
                boxstyle='square,pad=0', lw=1.2,
                edgecolor=C_ALT_BD, facecolor='white', zorder=3))
            ax.text(fx+tw/2, yt-0.15, tlbl, ha='center', va='center',
                    fontsize=8, color='#333333', fontweight='bold', zorder=4)

            divs = blk.get('dividers', [])
            section_tops = [yt] + [(ys[d-1]+ys[d])/2 for d in divs]

            for d in divs:
                ydiv = (ys[d-1]+ys[d])/2
                ax.plot([fx, fx+fw], [ydiv, ydiv],
                        color=C_ALT_BD, lw=0.8, linestyle='--', zorder=3)

            for j, sublbl in enumerate(blk.get('sub_labels', [])):
                if j < len(section_tops):
                    sy = section_tops[j] - 0.35
                    ax.text(fx+0.15, sy, sublbl, ha='left', va='center',
                            fontsize=7.5, color='#666666', style='italic', zorder=4)

    # ── Activation bars ───────────────────────────────────────────────────────
    if activations:
        for act in activations:
            pi = act['part']
            s, e = act['start'], act['end']
            yt_a = ys[s] + step*0.20
            yb_a = ys[e] - step*0.20
            act_bar(ax, xs[pi], yt_a, yb_a)

    # ── Messages ──────────────────────────────────────────────────────────────
    for msg, y in zip(msgs, ys):
        fi = msg['from']
        ti = msg['to']
        text = msg.get('text', '')
        is_ret = msg.get('ret', False)

        if fi == ti:
            # Self-loop
            x = xs[fi]
            r = 0.50
            ax.plot([x+0.09, x+r, x+r, x+0.09],
                    [y+0.18, y+0.18, y-0.12, y-0.12],
                    color=C_ARR, lw=1.2, zorder=3)
            ax.annotate('', xy=(x+0.09, y-0.12), xytext=(x+0.22, y-0.12),
                        arrowprops=dict(arrowstyle='->', color=C_ARR, lw=1.2), zorder=3)
            ax.text(x+r+0.12, y+0.03, text, ha='left', va='center',
                    fontsize=8, color=C_TXT, style='italic', zorder=5)
        else:
            arrow_msg(ax, xs[fi], y, xs[ti], dashed=is_ret, label=text)

    plt.tight_layout(pad=0)
    if fname:
        plt.savefig(fname, dpi=180, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f'Saved: {fname}')
    plt.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Login
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Login',
    parts=[
        {'name': 'Tim Marketing',   'type': 'actor'},
        {'name': 'Form Login',      'type': 'box'},
        {'name': 'Controller\nLogin','type': 'box'},
        {'name': 'Database',        'type': 'box'},
        {'name': 'Halaman\nUtama',  'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'view_FormLogin()'},
        {'from':0,'to':1,'text':'input_username()'},
        {'from':0,'to':1,'text':'input_password()'},
        {'from':1,'to':2,'text':'proses_login()'},
        {'from':2,'to':3,'text':'cek_data_login()'},
        {'from':3,'to':2,'text':'invalid()','ret':True},
        {'from':2,'to':1,'text':'notifikasi_login_gagal()','ret':True},
        {'from':3,'to':2,'text':'valid()','ret':True},
        {'from':2,'to':1,'text':'notifikasi_login_berhasil()','ret':True},
        {'from':1,'to':4,'text':'menampilkan()'},
    ],
    alt_blocks=[{
        'label':'alt Berhasil',
        'start':7,'end':9,
        'sub_labels':['[valid]'],
    }],
    activations=[
        {'part':1,'start':0,'end':6},
        {'part':2,'start':3,'end':6},
        {'part':3,'start':4,'end':5},
        {'part':2,'start':7,'end':9},
        {'part':1,'start':7,'end':9},
        {'part':4,'start':9,'end':9},
    ],
    height=13, width=15,
    fname='Sequence Diagram Login.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Logout
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Logout',
    parts=[
        {'name': 'Tim Marketing',     'type': 'actor'},
        {'name': 'Halaman Utama',     'type': 'box'},
        {'name': 'Controller\nLogout','type': 'box'},
        {'name': 'Database',          'type': 'box'},
        {'name': 'Form Login',        'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'klik_tombol_logout()'},
        {'from':1,'to':2,'text':'proses_logout()'},
        {'from':2,'to':3,'text':'hapus_sesi()'},
        {'from':3,'to':2,'text':'konfirmasi_hapus()','ret':True},
        {'from':2,'to':1,'text':'sesi_dihapus()','ret':True},
        {'from':1,'to':4,'text':'redirect_login()'},
        {'from':4,'to':0,'text':'tampilkan_form_login()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':5},
        {'part':2,'start':1,'end':4},
        {'part':3,'start':2,'end':3},
        {'part':4,'start':5,'end':6},
    ],
    height=11, width=15,
    fname='Sequence Diagram Logout.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Kelola Data Pendaftar
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Kelola Data Pendaftar',
    parts=[
        {'name': 'Tim Marketing',          'type': 'actor'},
        {'name': 'Halaman Data\nPendaftar','type': 'box'},
        {'name': 'Controller\nPendaftar',  'type': 'box'},
        {'name': 'Database',               'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'buka_menu_pendaftar()'},
        {'from':1,'to':2,'text':'get_data_pendaftar()'},
        {'from':2,'to':3,'text':'query_pendaftar()'},
        {'from':3,'to':2,'text':'return_data()','ret':True},
        {'from':2,'to':1,'text':'tampilkan_daftar()','ret':True},
        {'from':0,'to':1,'text':'tambah/edit/hapus_data()'},
        {'from':1,'to':2,'text':'proses_perubahan()'},
        {'from':2,'to':3,'text':'simpan_data()'},
        {'from':3,'to':2,'text':'konfirmasi_berhasil()','ret':True},
        {'from':2,'to':1,'text':'notifikasi_sukses()','ret':True},
        {'from':1,'to':0,'text':'tampilkan_pesan_sukses()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':4},
        {'part':2,'start':1,'end':3},
        {'part':3,'start':2,'end':3},
        {'part':1,'start':5,'end':10},
        {'part':2,'start':6,'end':9},
        {'part':3,'start':7,'end':8},
    ],
    height=13, width=13,
    fname='Sequence Diagram Kelola Data Pendaftar.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Lihat Hasil Klasifikasi
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Lihat Hasil Klasifikasi',
    parts=[
        {'name': 'Tim Marketing',             'type': 'actor'},
        {'name': 'Halaman\nKlasifikasi',      'type': 'box'},
        {'name': 'Controller\nKlasifikasi',   'type': 'box'},
        {'name': 'Database',                  'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'pilih_pendaftar()'},
        {'from':1,'to':2,'text':'get_data_pendaftar()'},
        {'from':2,'to':3,'text':'query_data()'},
        {'from':3,'to':2,'text':'return_data()','ret':True},
        {'from':2,'to':2,'text':'klasifikasi_naive_bayes()'},
        {'from':2,'to':3,'text':'simpan_hasil()'},
        {'from':3,'to':2,'text':'konfirmasi_simpan()','ret':True},
        {'from':2,'to':1,'text':'return_hasil_klasifikasi()','ret':True},
        {'from':1,'to':0,'text':'tampilkan_hasil()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':8},
        {'part':2,'start':1,'end':7},
        {'part':3,'start':2,'end':3},
        {'part':3,'start':5,'end':6},
    ],
    height=12, width=13,
    fname='Sequence Diagram Lihat Hasil Klasifikasi.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Lihat Rekomendasi
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Lihat Rekomendasi',
    parts=[
        {'name': 'Tim Marketing',          'type': 'actor'},
        {'name': 'Halaman\nRekomendasi',   'type': 'box'},
        {'name': 'Controller\nRekomendasi','type': 'box'},
        {'name': 'Database',               'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'buka_rekomendasi()'},
        {'from':1,'to':2,'text':'get_data_klasifikasi()'},
        {'from':2,'to':3,'text':'query_data()'},
        {'from':3,'to':2,'text':'return_data()','ret':True},
        {'from':2,'to':2,'text':'generate_rekomendasi()'},
        {'from':2,'to':1,'text':'return_rekomendasi()','ret':True},
        {'from':1,'to':0,'text':'tampilkan_rekomendasi()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':6},
        {'part':2,'start':1,'end':5},
        {'part':3,'start':2,'end':3},
    ],
    height=11, width=13,
    fname='Sequence Diagram Lihat Rekomendasi.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Lihat Detail Prediksi
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Lihat Detail Prediksi',
    parts=[
        {'name': 'Tim Marketing',       'type': 'actor'},
        {'name': 'Halaman\nDetail',     'type': 'box'},
        {'name': 'Controller\nDetail',  'type': 'box'},
        {'name': 'Database',            'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'pilih_detail_prediksi()'},
        {'from':1,'to':2,'text':'get_detail_pendaftar()'},
        {'from':2,'to':3,'text':'query_detail()'},
        {'from':3,'to':2,'text':'return_detail()','ret':True},
        {'from':2,'to':1,'text':'return_data_detail()','ret':True},
        {'from':1,'to':0,'text':'tampilkan_detail()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':5},
        {'part':2,'start':1,'end':4},
        {'part':3,'start':2,'end':3},
    ],
    height=10, width=13,
    fname='Sequence Diagram Lihat Detail Prediksi.png'
)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. Cetak / Export Laporan
# ═══════════════════════════════════════════════════════════════════════════════
draw_seq(
    title='Sequence Diagram Cetak Export Laporan',
    parts=[
        {'name': 'Tim Marketing',        'type': 'actor'},
        {'name': 'Halaman\nLaporan',     'type': 'box'},
        {'name': 'Controller\nLaporan',  'type': 'box'},
        {'name': 'Database',             'type': 'box'},
    ],
    msgs=[
        {'from':0,'to':1,'text':'pilih_format_laporan()'},
        {'from':1,'to':2,'text':'proses_laporan()'},
        {'from':2,'to':3,'text':'get_data_laporan()'},
        {'from':3,'to':2,'text':'return_data()','ret':True},
        {'from':2,'to':2,'text':'generate_dokumen()'},
        {'from':2,'to':1,'text':'return_dokumen()','ret':True},
        {'from':1,'to':0,'text':'unduh_cetak_dokumen()','ret':True},
    ],
    activations=[
        {'part':1,'start':0,'end':6},
        {'part':2,'start':1,'end':5},
        {'part':3,'start':2,'end':3},
    ],
    height=11, width=13,
    fname='Sequence Diagram Cetak Export Laporan.png'
)
