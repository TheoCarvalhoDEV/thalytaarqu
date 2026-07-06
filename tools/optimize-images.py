#!/usr/bin/env python3
"""Gera versões WebP responsivas das imagens do site.

Uso:  python tools/optimize-images.py
Saída: assets/images/webp/<basename>-<largura>.webp
Idempotente: pula arquivos já gerados mais novos que a origem.
Em julho (fotos profissionais): adicionar as fotos novas ao CONFIG e rodar de novo.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "webp")

# (caminho relativo à raiz, [larguras alvo]) — larguras maiores que a origem são ignoradas
CONFIG = [
    ("assets/images/hero-cozinha.jpg",              [768, 1280, 1440]),
    ("assets/images/hero-lavabo.jpg",               [768, 1280, 1440]),
    ("assets/images/hero-lounge.jpg",               [768, 1280, 1920]),
    ("assets/images/hero-quarto.jpg",               [768, 1280]),
    ("assets/images/portrait.jpg",                  [686]),
    ("assets/images/pattern.png",                   [799]),
    ("assets/pinterest/cozinha-marmore.jpg",        [800, 1200]),
    ("assets/pinterest/cozinha-office.jpg",         [800, 1200]),
    ("assets/pinterest/quarto-infantil-floral.jpg", [800, 1200]),
    ("assets/pinterest/bercario.jpg",               [800, 1200]),
    ("assets/pinterest/lavabo-toucador.jpg",        [800, 1200]),
    ("assets/pinterest/quarto-casal.jpg",           [800, 1200]),
    ("assets/pinterest/banheiro-terrazzo.jpg",      [800]),
    ("assets/pinterest/lounge-verde.jpg",           [800, 1200]),
    ("assets/pinterest/marias-kids-fachada.jpg",    [800, 1200]),
    ("assets/pinterest/marias-kids-logo.jpg",       [707]),
    ("assets/pinterest/escritorio-orion.jpg",       [720]),
]
QUALITY = 80

def main():
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    for rel, widths in CONFIG:
        src = os.path.join(ROOT, rel)
        im = Image.open(src)
        base = os.path.splitext(os.path.basename(rel))[0]
        for w in widths:
            if w > im.width:
                continue
            dst = os.path.join(OUT, f"{base}-{w}.webp")
            if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
                print(f"  pulado (atual): {os.path.basename(dst)}")
                continue
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).convert("RGB").save(
                dst, "WEBP", quality=QUALITY, method=6)
            print(f"  {rel} -> {os.path.basename(dst)}  {os.path.getsize(dst)//1024}KB")
        total_in += os.path.getsize(src)
    for f in os.listdir(OUT):
        total_out += os.path.getsize(os.path.join(OUT, f))
    print(f"\norigem: {total_in//1024}KB | webp gerados (total): {total_out//1024}KB")

if __name__ == "__main__":
    main()
