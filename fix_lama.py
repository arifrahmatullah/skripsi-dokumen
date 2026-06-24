from PIL import Image, ImageDraw
import math

img = Image.open('Proses Bisnis Lama.jpg')
draw = ImageDraw.Draw(img)

# End circle lama ada di x≈1308-1341, y≈416-449 → center (1324, 432), radius 17
end_cx, end_cy, end_r = 1324, 432, 17

# 1. Hapus pink circle dan ganti jadi end event (hitam)
draw.ellipse([end_cx-end_r-3, end_cy-end_r-3, end_cx+end_r+3, end_cy+end_r+3], fill=(255,255,255))
draw.ellipse([end_cx-end_r, end_cy-end_r, end_cx+end_r, end_cy+end_r],
             fill=(40, 40, 40), outline=(10, 10, 10), width=3)
draw.ellipse([end_cx-8, end_cy-8, end_cx+8, end_cy+8], fill=(10, 10, 10))

# Helper panah
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

# 2. Panah dari MASUK box right (≈x=840, center y=387) ke end circle left
draw_arrow(draw, (840, 387), (end_cx - end_r, end_cy - 4))

# 3. Panah dari TIDAK MASUK box right (≈x=840, center y=485) ke end circle left
draw_arrow(draw, (840, 487), (end_cx - end_r, end_cy + 4))

img.save('Proses Bisnis Lama.jpg', quality=95)
print("Done")
