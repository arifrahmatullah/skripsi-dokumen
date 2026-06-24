from PIL import Image, ImageDraw
import math

img = Image.open('Proses Bisnis Baru.jpg')
draw = ImageDraw.Draw(img)

# 1. Perbaiki start circle - bagian bawah kepotong rectangle putih sebelumnya
# Dari scan pixel: center ~(164, 171), radius ~18, warna pink (252,197,194)
cx, cy, r = 164, 171, 18
# Hapus dulu area yang terkena white rect
draw.rectangle([cx-r-3, cy-r-3, cx+r+3, cy+r+25], fill=(255,255,255))
# Gambar ulang full circle
draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(252, 197, 194), outline=(160, 100, 90), width=2)

# 2. Tambah end event circle (BPEL = filled dark circle) di lane Calon Mahasiswa
# MASUK box right edge: x=840, center y=373
# TIDAK MASUK box right edge: x=840, center y=463
# End event di tengah, di kanan: (975, 418)
end_cx, end_cy, end_r = 975, 418, 18
draw.ellipse([end_cx-end_r, end_cy-end_r, end_cx+end_r, end_cy+end_r],
             fill=(40, 40, 40), outline=(10, 10, 10), width=3)
# Inner dot (bullseye style)
draw.ellipse([end_cx-8, end_cy-8, end_cx+8, end_cy+8], fill=(10, 10, 10))

# Helper fungsi gambar panah
def draw_arrow(draw, start, end, color=(80, 80, 80), width=2, arrow_size=9):
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    dx /= length
    dy /= length
    tip = end
    left  = (int(tip[0] - arrow_size*dx + arrow_size*0.45*dy),
             int(tip[1] - arrow_size*dy - arrow_size*0.45*dx))
    right = (int(tip[0] - arrow_size*dx - arrow_size*0.45*dy),
             int(tip[1] - arrow_size*dy + arrow_size*0.45*dx))
    draw.polygon([tip, left, right], fill=color)

# 3. Panah dari MASUK box (right edge x=840, center y=373) ke end circle left (957, 418)
draw_arrow(draw, (840, 373), (end_cx - end_r, end_cy - 4))

# 4. Panah dari TIDAK MASUK box (right edge x=840, center y=463) ke end circle left (957, 418)
draw_arrow(draw, (840, 463), (end_cx - end_r, end_cy + 4))

img.save('Proses Bisnis Baru.jpg', quality=95)
print("Done")
