import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 13))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13)
ax.axis('off')
fig.patch.set_facecolor('white')

C_LANE_HDR = '#D0D8E8'
C_LANE_BG1 = '#F7F9FC'
C_LANE_BG2 = '#FFFFFF'
C_ACTION   = '#DDEEFF'
C_ACTION_BD= '#2255AA'
C_ARROW    = '#333333'
C_TEXT     = '#111111'

ax.text(5, 12.65, 'Activity Diagram Login',
        ha='center', va='center', fontsize=13, fontweight='bold', color=C_TEXT)

lane1_x, lane2_x, lane_end = 0.3, 4.8, 9.7
lane_top, lane_bot = 12.3, 0.5

ax.add_patch(mpatches.FancyBboxPatch((lane1_x, lane_bot),
    lane_end-lane1_x, lane_top-lane_bot,
    boxstyle='square,pad=0', lw=1.8, edgecolor='#555555', facecolor='none', zorder=2))
ax.plot([lane2_x, lane2_x], [lane_bot, lane_top], color='#555555', lw=1.2, zorder=2)
ax.plot([lane1_x, lane_end], [lane_top-0.55, lane_top-0.55], color='#555555', lw=1.2, zorder=2)

for (x, w) in [(lane1_x, lane2_x-lane1_x), (lane2_x, lane_end-lane2_x)]:
    ax.add_patch(mpatches.FancyBboxPatch((x, lane_top-0.55), w, 0.55,
        boxstyle='square,pad=0', lw=0, facecolor=C_LANE_HDR, zorder=1))
ax.add_patch(mpatches.FancyBboxPatch((lane1_x, lane_bot),
    lane2_x-lane1_x, lane_top-lane_bot-0.55, boxstyle='square,pad=0', lw=0, facecolor=C_LANE_BG1, zorder=1))
ax.add_patch(mpatches.FancyBboxPatch((lane2_x, lane_bot),
    lane_end-lane2_x, lane_top-lane_bot-0.55, boxstyle='square,pad=0', lw=0, facecolor=C_LANE_BG2, zorder=1))

L1 = (lane1_x + lane2_x) / 2   # 2.55

ax.text(L1, lane_top-0.275, 'Tim Marketing', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_TEXT)
ax.text((lane2_x+lane_end)/2, lane_top-0.275, 'Sistem', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_TEXT)

# ── Helpers ──────────────────────────────────────────────────────────────────
def action(cx, cy, text, w=3.4, h=0.55):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0.08', lw=1.5,
        edgecolor=C_ACTION_BD, facecolor=C_ACTION, zorder=4))
    lines = text.split('\n')
    off = 0.10 if len(lines) > 1 else 0
    for i, ln in enumerate(lines):
        ax.text(cx, cy+off-i*0.21, ln, ha='center', va='center',
                fontsize=9.5, color=C_TEXT, zorder=5)

def decision(cx, cy, text, w=2.4, h=0.80):
    ax.add_patch(plt.Polygon([
        (cx, cy+h/2), (cx+w/2, cy), (cx, cy-h/2), (cx-w/2, cy)
    ], closed=True, lw=1.5, edgecolor=C_ACTION_BD, facecolor='#FFF8CC', zorder=4))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=9.5, color=C_TEXT, zorder=5)

def start_node(cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.22, color='#222222', zorder=6))

def end_node(cx, cy):
    ax.add_patch(plt.Circle((cx, cy), 0.30, color='#222222', fill=False, lw=2.8, zorder=6))
    ax.add_patch(plt.Circle((cx, cy), 0.20, color='#222222', zorder=6))

def arr(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=C_ARROW, lw=1.5), zorder=3)

def lbl(x, y, txt, ha='left'):
    ax.text(x, y, txt, ha=ha, va='center', fontsize=8.5,
            color='#555555', style='italic', zorder=5)

def hline(x1, x2, y):
    ax.plot([x1, x2], [y, y], color=C_ARROW, lw=1.5, zorder=3)

def vline(x, y1, y2):
    ax.plot([x, x], [y1, y2], color=C_ARROW, lw=1.5, zorder=3)

# ── Posisi X yang jelas terpisah ─────────────────────────────────────────────
# Sistem lane: x = 4.8 sampai 9.7 (lebar 4.9)
# Ya path  → cx_ya  = 6.2  (kiri dalam Sistem lane), box w=2.5 → span 4.95–7.45
# Tidak path → cx_no = 8.7  (kanan dalam Sistem lane), box w=1.8 → span 7.8–9.6
# Gap antara dua box: 7.45 ke 7.8 = 0.35 ✓
cx_ya = 6.2
cx_no = 8.7
DEC_X = 7.0   # posisi X decision (antara dua path)

# ── Y positions ───────────────────────────────────────────────────────────────
y_start = 11.50
y_a1    = 10.70
y_a2    = 9.65
y_a3    = 8.60
y_dec   = 7.30
y_branch= 5.90   # Ya (cx_ya) dan Tidak (cx_no) pada Y yang sama
y_end   = 4.50

# ── Nodes ────────────────────────────────────────────────────────────────────
start_node(L1, y_start)

action(L1, y_a1, 'Buka Aplikasi')
arr(L1, y_start-0.22, L1, y_a1+0.275)

L2_login = (lane2_x+lane_end)/2   # cx box Tampilkan Halaman Login = 7.25
action(L2_login, y_a1, 'Tampilkan\nHalaman Login')
# Panah dari Buka Aplikasi → kanan ke kiri box Tampilkan Halaman Login (horizontal)
arr(L1+1.7, y_a1, L2_login-1.7, y_a1)

action(L1, y_a2, 'Masukkan Username\n& Password')
# Panah dari bawah Tampilkan Halaman Login → turun → kiri → masuk Masukkan Username
vline(L2_login, y_a1-0.275, y_a2)
arr(L2_login, y_a2, L1+1.7, y_a2)

action(L1, y_a3, 'Klik Tombol Login')
arr(L1, y_a2-0.275, L1, y_a3+0.275)

# Klik Login → Decision (patah: horizontal dulu ke DEC_X, lalu turun ke diamond)
hline(L1+1.7, DEC_X, y_a3)
arr(DEC_X, y_a3, DEC_X, y_dec+0.40)
decision(DEC_X, y_dec, 'Valid?')

# ══ YA: bawah diamond → cx_ya ════════════════════════════════════════════════
# Dari bawah diamond turun ke level y_branch dan bergeser ke cx_ya
vline(DEC_X, y_dec-0.40, y_branch+0.275)
hline(DEC_X, cx_ya, y_branch+0.275)
arr(DEC_X, y_branch+0.275, cx_ya, y_branch+0.275)
action(cx_ya, y_branch, 'Tampilkan\nHalaman Utama', w=2.5)
lbl(DEC_X+0.08, (y_dec-0.40+y_branch+0.275)/2, 'Ya')

end_node(cx_ya, y_end)
arr(cx_ya, y_branch-0.275, cx_ya, y_end+0.30)

# ══ TIDAK: kanan diamond → cx_no ══════════════════════════════════════════════
hline(DEC_X+1.2, cx_no, y_dec)       # horizontal dari tip kanan ke cx_no
vline(cx_no, y_dec, y_branch+0.275)  # turun ke level y_branch
arr(cx_no, y_dec, cx_no, y_branch+0.275)
action(cx_no, y_branch, 'Tampilkan\nPesan Error', w=1.8)
lbl(DEC_X+1.25, y_dec+0.18, 'Tidak')

# ══ Loop back: Pesan Error → bawah lane → kiri → atas → Masukkan Username ════
loop_bot = lane_bot + 0.25
vline(cx_no, y_branch-0.275, loop_bot)          # turun ke bawah lane
hline(cx_no, lane1_x+0.18, loop_bot)            # ke kiri melewati lane divider
vline(lane1_x+0.18, loop_bot, y_a2)             # naik ke level A2
arr(lane1_x+0.18, y_a2, L1-1.7, y_a2)          # panah masuk ke kiri A2

plt.tight_layout(pad=0.3)
plt.savefig('Activity Diagram Login.png', dpi=180, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Saved: Activity Diagram Login.png')
plt.close()
