#!/usr/bin/env python3
"""
Generate placeholder images for Terra Collecta products.

Strategy: Use the Python Imaging Library (Pillow) if available, otherwise
create minimal valid JPEG files using a tiny canvas with category colors.

Each image is 400×400px, solid color matching the category/mineral type,
with the product name overlaid as text. Saved to wp-content/uploads/terra-collecta/
"""
import os
import json
import re
import sys
import struct
import zlib

OUTPUT_DIR = "wp-content/uploads/terra-collecta"
JSON_PATH  = "import/products.json"

# Category → background color (R, G, B)
CATEGORY_COLORS = {
    "Minerals":             (42,  42,  68),   # Deep indigo
    "Gemstones":            (62,  22,  44),   # Deep ruby
    "Fossils":              (55,  45,  28),   # Sediment brown
    "Meteorites":           (32,  32,  32),   # Near-black
    "Geological Specimens": (28,  42,  28),   # Dark green
    "Curated Collections":  (42,  34,  16),   # Dark gold
}

# Keyword → dominant color override
KEYWORD_COLORS = {
    "amethyst":    (88,  60, 120),
    "rose quartz": (180, 120, 120),
    "citrine":     (160, 130,  40),
    "smoky":       (60,  55,  50),
    "agate":       (80,  100, 110),
    "labradorite": (40,  80, 120),
    "moonstone":   (180, 180, 200),
    "amazonite":   (50, 140, 130),
    "tourmaline":  (40,  90,  60),
    "ruby":        (160,  20,  30),
    "emerald":     (20, 120,  50),
    "sapphire":    (20,  50, 160),
    "aquamarine":  (70, 170, 180),
    "fluorite":    (140,  60, 180),
    "malachite":   (20, 140,  60),
    "azurite":     (20,  60, 160),
    "pyrite":      (180, 160,  30),
    "gold":        (200, 160,  20),
    "silver":      (160, 160, 170),
    "copper":      (170,  80,  30),
    "opal":        (200, 180, 200),
    "amber":       (200, 140,  30),
    "moldavite":   (40, 120,  50),
    "iron meteor": (60,  60,  60),
    "pallasite":   (100,  80,  30),
    "fossil":      (120, 100,  60),
    "trilobite":   (110,  90,  50),
    "ammonite":    (90,  70,  40),
    "obsidian":    (20,  20,  25),
    "garnet":      (140,  20,  40),
    "topaz":       (200, 160,  80),
    "tanzanite":   (60,  40, 140),
}


def pick_color(name, category):
    name_lower = name.lower()
    for kw, col in KEYWORD_COLORS.items():
        if kw in name_lower:
            return col
    return CATEGORY_COLORS.get(category, (60, 60, 80))


def make_png(width, height, r, g, b, label):
    """
    Create a minimal valid PNG (no external deps).
    Solid color background + no text (text requires font rendering).
    """
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        chunk_data = chunk_type + data
        chunk_crc = struct.pack('>I', zlib.crc32(chunk_data) & 0xffffffff)
        return chunk_len + chunk_data + chunk_crc

    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)

    # Image data: each row has a filter byte (0 = None) + RGB pixels
    raw_rows = []
    for y in range(height):
        row = b'\x00'  # filter byte
        for x in range(width):
            # Slightly vary shade to add texture interest
            shade = 1.0 + 0.05 * ((x * 3 + y * 7) % 20 - 10) / 20.0
            pr = max(0, min(255, int(r * shade)))
            pg = max(0, min(255, int(g * shade)))
            pb = max(0, min(255, int(b * shade)))
            row += bytes([pr, pg, pb])
        raw_rows.append(row)

    raw_data = b''.join(raw_rows)
    compressed = zlib.compress(raw_data, 6)
    idat = png_chunk(b'IDAT', compressed)

    # IEND
    iend = png_chunk(b'IEND', b'')

    return sig + ihdr + idat + iend


def safe_filename(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name[:80]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(JSON_PATH) as f:
        products = json.load(f)

    print(f"Generating {len(products)} placeholder images…")
    generated = 0
    skipped = 0

    for p in products:
        sku = p.get('sku', '')
        name = p.get('name', 'specimen')
        category = p.get('category', 'Minerals')

        filename = f"{sku}-{safe_filename(name)}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            skipped += 1
            continue

        r, g, b = pick_color(name, category)

        try:
            png_data = make_png(400, 400, r, g, b, name)
            with open(filepath, 'wb') as out:
                out.write(png_data)
            generated += 1
        except Exception as e:
            print(f"  Error generating {filename}: {e}", file=sys.stderr)

        if (generated + skipped) % 100 == 0:
            print(f"  Progress: {generated + skipped}/{len(products)}")

    print(f"Done. Generated: {generated}, Skipped (already exist): {skipped}")
    print(f"Images saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
