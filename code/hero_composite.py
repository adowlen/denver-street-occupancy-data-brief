"""Composite the headline figure over the generated hero illustration.
Text sits on the illustration's clean dark top field, with a light
gradient scrim as insurance; headline text is the exact text specified
in hero_source/hero-brief.md."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parent.parent
cands = sorted((root / "hero_source").glob("*.webp")) + \
        sorted((root / "hero_source").glob("*.png")) + \
        sorted((root / "hero_source").glob("*.jpg"))
if not cands:
    raise SystemExit("no hero illustration in hero_source/ - hero stays pending")
img = Image.open(cands[0]).convert("RGB")
W, H = img.size

band = int(H * 0.40)
overlay = Image.new("L", (1, band))
for yy in range(band):
    t = yy / band
    overlay.putpixel((0, yy), int(150 * (1 - t) ** 1.4))
overlay = overlay.resize((W, band))
scrim = Image.new("RGB", (W, band), (13, 17, 20))
img.paste(scrim, (0, 0), overlay)
d = ImageDraw.Draw(img)


def font(size, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, size)


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


MAXW = W - 124
headline = "34.6%"
d.text((60, 30), headline, font=font(int(H * 0.092)), fill=(245, 168, 0))
sub_f = font(int(H * 0.031), bold=False)
y = 30 + int(H * 0.118)
sub = ("of Denver's 2,595,960 street-occupancy segment-days come from the 1.8% "
       "of segment permits that run over 90 days - the median permit runs 3 days")
for line in wrap(sub, sub_f, MAXW):
    d.text((62, y), line, font=sub_f, fill=(242, 242, 242))
    y += int(H * 0.046)
src_f = font(int(H * 0.022), bold=False)
srcline = ("Machine Readable - Denver street occupancy permits layer (DOTI / Accela), "
           "pulled Oct 30, 2026 - 259,284 duration-valid segment records")
for line in wrap(srcline, src_f, MAXW):
    d.text((62, y + 6), line, font=src_f, fill=(150, 210, 200))
    y += int(H * 0.034)
img.save(root / "hero.png")
print("hero", img.size, "from", cands[0].name)
