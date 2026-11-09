"""grid.py <out.jpg> <файл1> … — макет сетки профиля Instagram: 3 колонки, плитка 3:4 из центра 9:16,
значок Reels/закрепа справа сверху, глаз и просмотры слева снизу (как на скриншоте пользователя)."""
import sys
from PIL import Image, ImageDraw, ImageFont
VIEWS = ['31K', '320K', '44.4K', '42.8K', '6,116', '12.7K', '2,533', '7,630', '3,582']
TW, TH, G = 360, 480, 3
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
out, files = sys.argv[1], sys.argv[2:]
S = Image.new('RGB', (TW * 3 + G * 2, (TH + G) * ((len(files) + 2) // 3) - G), 'white')
for i, p in enumerate(files):
    im = Image.open(p).convert('RGB'); s = TW / im.width
    im = im.resize((TW, round(im.height * s)), Image.LANCZOS); y0 = (im.height - TH) // 2
    t = im.crop((0, y0, TW, y0 + TH)); d = ImageDraw.Draw(t, 'RGBA')
    # значок справа сверху: закреп у первых трёх, Reels у остальных
    if i < 3: d.polygon([(318, 16), (340, 38), (328, 42), (316, 54), (312, 50), (322, 38), (314, 30)], fill=(255, 255, 255, 235))
    else: d.rounded_rectangle([314, 14, 344, 44], 8, outline=(255, 255, 255, 235), width=3); d.polygon([(325, 22), (325, 36), (337, 29)], fill=(255, 255, 255, 235))
    d.ellipse([14, TH - 38, 40, TH - 22], outline=(255, 255, 255, 240), width=3); d.ellipse([23, TH - 34, 31, TH - 26], fill=(255, 255, 255, 240))
    d.text((48, TH - 44), VIEWS[i % 9], font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 120))
    S.paste(t, ((i % 3) * (TW + G), (i // 3) * (TH + G)))
S.save(out, quality=88); print(out, S.size)
