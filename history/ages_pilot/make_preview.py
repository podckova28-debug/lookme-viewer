import sys; sys.path.insert(0, "/home/user/lookme-viewer/history")
from chapter_card import _cover, draw_text
from PIL import Image, ImageDraw, ImageFont
W, H = 1280, 720
T = {"TA1": [("THEY ALL FELL", 150, 110, None)],
     "TA2": [("IT ALWAYS", 150, 250, 330), ("ENDS", 190, 430, 330)],
     "TB1": [("WHO'S NEXT?", 150, 95, None)],
     "TB2": [("1177 BC", 190, 300, 290)]}
for k, lines in T.items():
    im = _cover(f"raw/{k}.png", W, H)
    for text, size, cy, cx in lines:
        im = draw_text(im, text, size, cy, cx=cx, maxw=0.9 if cx is None else 0.45)
    im.convert("RGB").save(f"thumb_{k}.jpg", quality=92)
# side-by-side sheets
def sheet(names, out, cols=2, w=960, h=540, labels=None):
    rows = (len(names) + cols - 1) // cols; S = Image.new("RGB", (cols * w, rows * h), (20, 20, 20)); d = ImageDraw.Draw(S)
    f = ImageFont.truetype("/home/user/lookme-viewer/history/fonts/BebasNeue-Regular.ttf", 44)
    for i, n in enumerate(names):
        x, y = (i % cols) * w, (i // cols) * h
        if n: S.paste(Image.open(n).convert("RGB").resize((w, h)), (x, y))
        if labels and labels[i]:
            d.rectangle([x, y, x + 20 + f.getlength(labels[i]), y + 54], fill=(0, 0, 0)); d.text((x + 10, y + 4), labels[i], font=f, fill=(255, 230, 0))
    S.save(out, quality=90)
sheet(["raw/A1.png", "raw/B1.png", "raw/A2.png", "raw/B2.png", "raw/A3.png", "raw/B3.png", None, "raw/B4.png"], "frames_compare.jpg",
      labels=["A KINO 1177 BC", "B KOMIKS 1177 BC", "A ROME 600 AD", "B ROME 600 AD", "A 1453", "B 1453", "A FLORENCE (BLOCKED)", "B FLORENCE 1497"])
sheet(["thumb_TA1.jpg", "thumb_TA2.jpg", "thumb_TB1.jpg", "thumb_TB2.jpg"], "thumbs_compare.jpg",
      labels=["A1", "A2", "B1", "B2"])
