from PIL import Image, ImageDraw

img = Image.open('Proses Bisnis Baru.jpg')
draw = ImageDraw.Draw(img)

# Hapus label "StartEvent1" - koordinat di bawah lingkaran start (kiri atas, lane Tim Marketing)
# Gambar 1055x593, StartEvent1 ada sekitar x=95-215, y=185-205
draw.rectangle([90, 182, 220, 210], fill='white')

img.save('Proses Bisnis Baru.jpg', quality=95)
print("Done. Size:", img.size)
