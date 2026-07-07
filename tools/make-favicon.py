#!/usr/bin/env python3
"""Gera favicon.ico (16/32/48) e apple-touch-icon.png (180, fundo creme) do selo oficial."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "COMUNICACAO_VISUAL", "IDENTIDADE VISUAL THALYTA MAIA",
                   "MARCA D´ÁGUA", "MARCA D´AGUA 3.png")
CREAM = (246, 241, 233, 255)

im = Image.open(SRC).convert("RGBA")
# bbox do conteúdo (não transparente e não branco)
px, (w, h) = im.load(), im.size
xs, ys = [], []
for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b, a = px[x, y]
        if a > 20 and not (r > 245 and g > 245 and b > 245):
            xs.append(x); ys.append(y)
m = 14
box = (max(0, min(xs)-m), max(0, min(ys)-m), min(w, max(xs)+m), min(h, max(ys)+m))
seal = im.crop(box)
# quadrado com padding transparente
side = max(seal.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(seal, ((side-seal.width)//2, (side-seal.height)//2), seal)

sq.resize((48, 48), Image.LANCZOS).save(
    os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
touch = Image.new("RGBA", (side, side), CREAM)
touch.alpha_composite(sq)
touch.convert("RGB").resize((180, 180), Image.LANCZOS).save(
    os.path.join(ROOT, "assets", "images", "apple-touch-icon.png"))
print("ok: favicon.ico + apple-touch-icon.png")
