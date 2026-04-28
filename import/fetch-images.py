#!/usr/bin/env python3
"""
Fetch real geological specimen images from Wikimedia Commons.

Downloads one image per unique base specimen name (~153 total), resizes
to max 600px, compresses to target ~35KB JPEG, and replaces the
color-coded placeholder PNGs in wp-content/uploads/terra-collecta/.

Usage: python3 import/fetch-images.py
Saves attribution data to: import/image-sources.json
"""

import json, os, re, sys, time, urllib.request, urllib.parse, urllib.error, io, hashlib
from PIL import Image

# ── Config ────────────────────────────────────────────────────────────────────
OUTPUT_DIR   = "wp-content/uploads/terra-collecta"
JSON_PATH    = "import/products.json"
SOURCES_PATH = "import/image-sources.json"
MAX_PX       = 600          # longest side
JPEG_QUALITY = 72           # starting quality; reduced if still over size limit
MAX_BYTES    = 50_000       # hard ceiling per image
API_DELAY    = 1.5          # seconds between Wikimedia API calls
MAX_RETRIES  = 5            # max retries on 429
WIKI_API     = "https://commons.wikimedia.org/w/api.php"
USER_AGENT   = "TerraCollectaDemo/1.0 (tag1.com; scolta-demo) python-urllib"

# ── Search-term overrides ─────────────────────────────────────────────────────
# Maps base product name → better Wikimedia search query
SEARCH_TERMS = {
    # Minerals
    "Amethyst Cluster":                 "amethyst geode crystal cluster",
    "Rose Quartz Sphere":               "rose quartz crystal mineral",
    "Citrine Crystal Point":            "citrine quartz crystal point",
    "Smoky Quartz Elestial":            "smoky quartz crystal",
    "Agate Slice":                      "agate slice polished botswana",
    "Labradorite Freeform":             "labradorite feldspar iridescence",
    "Moonstone with Adularescence":     "moonstone gemstone adularescence",
    "Amazonite Crystal":                "amazonite feldspar crystal",
    "Black Tourmaline Schorl Crystal":  "schorl tourmaline crystal black",
    "Rubellite Tourmaline Crystal":     "rubellite tourmaline pink crystal",
    "Indicolite Tourmaline":            "indicolite tourmaline blue crystal",
    "Emerald Crystal in Matrix":        "emerald crystal beryl colombian",
    "Aquamarine Crystal":               "aquamarine beryl crystal",
    "Heliodor Crystal":                 "heliodor golden beryl crystal",
    "Goshenite":                        "goshenite beryl white crystal",
    "Grossular Garnet":                 "tsavorite grossular garnet crystal",
    "Spessartine Garnet Crystal":       "spessartine garnet orange crystal",
    "Rhodolite Garnet Crystal":         "rhodolite garnet crystal",
    "Topaz":                            "topaz imperial crystal mineral",
    "Blue Topaz Crystal":               "blue topaz crystal",
    "Purple Fluorite Octahedron":       "fluorite octahedron purple crystal",
    "Green Fluorite Cubic Cluster":     "fluorite green cubic crystal",
    "Malachite Botryoidal Specimen":    "malachite botryoidal mineral",
    "Azurite-Malachite Crystal Cluster":"azurite malachite mineral",
    "Pyrite Cube Cluster":              "pyrite cube crystal navajun",
    "Chalcopyrite Crystal on Sphalerite":"chalcopyrite iridescent mineral",
    "Native Gold in Quartz Vein":       "native gold quartz vein mineral",
    "Stibnite Crystal Group":           "stibnite crystal antimony mineral",
    "Crocoite Crystal Cluster":         "crocoite crystal orange mineral",
    "Vanadinite on Barite":             "vanadinite crystal red hexagonal",
    "Wulfenite Crystal Plate":          "wulfenite crystal orange plate",
    "Rhodochrosite Stalactite Slice":   "rhodochrosite stalactite slice",
    "Selenite Gypsum Wand":             "selenite gypsum crystal clear",
    "Desert Rose Barite":               "desert rose barite crystal",
    "Celestite Geode":                  "celestite geode crystal blue",
    "Calcite Dog-Tooth Cluster":        "calcite dogtooth crystal cluster",
    "Iceland Spar":                     "iceland spar optical calcite",
    "Apophyllite Crystal Cluster on Stilbite":"apophyllite stilbite crystal india",
    "Rhodonite Specimen":               "rhodonite mineral pink",
    "Dioptase Crystal Cluster":         "dioptase crystal green copper",
    "Zircon Crystal in Pegmatite":      "zircon crystal mineral",
    "Pyrrhotite Crystal":               "pyrrhotite crystal magnetic iron sulfide",
    "Realgar Crystal on Orpiment":      "realgar orpiment crystal arsenic sulfide",
    "Wollastonite Spray":               "wollastonite mineral calcium silicate",
    "Staurolite Twin":                  "staurolite fairy stone twin crystal",
    "Prehnite Stalactite":              "prehnite crystal green mineral",
    "Kunzite Crystal":                  "kunzite spodumene pink crystal",
    "Hiddenite Crystal":                "hiddenite green spodumene crystal",
    "Benitoite Crystal on Natrolite":   "benitoite crystal blue natrolite",
    "Tanzanite Crystal":                "tanzanite crystal unheated zoisite",
    "Alexandrite Crystal":              "alexandrite color change chrysoberyl",
    "Painite Crystal":                  "painite mineral rare crystal",
    "Red Beryl Crystal":                "red beryl bixbite utah crystal",
    "Euclase Crystal":                  "euclase crystal beryllium mineral",
    "Fluorapatite Crystal":             "fluorapatite crystal hexagonal",
    "Clinozoisite Crystal":             "clinozoisite crystal alpine",
    "Manganite Crystal":                "manganite crystal mineral manganese",
    "Native Silver Wires":              "native silver wire crystal kongsberg",
    "Native Copper Arborescent":        "native copper arborescent michigan",
    "Hematite Rose":                    "hematite rose iron mineral elba",
    "Ilvaite Crystal":                  "ilvaite crystal mineral",
    "Kyanite Crystal":                  "kyanite crystal blue mineral",
    "Sillimanite Fibrous":              "sillimanite fibrolite mineral",
    "Pyrite Cube Cluster":              "pyrite cube crystal",

    # Gemstones
    "Diamond Crystal":                  "diamond crystal rough octahedron",
    "Ruby Crystal in Matrix":           "ruby crystal corundum red",
    "Padparadscha Sapphire Crystal":    "padparadscha sapphire orange pink",
    "Star Sapphire":                    "star sapphire cabochon asterism",
    "Cat's Eye Chrysoberyl":            "cat eye chrysoberyl chatoyancy",
    "Star Ruby":                        "star ruby cabochon asterism",
    "Black Opal":                       "black opal lightning ridge",
    "White Opal":                       "white opal harlequin",
    "Fire Opal Crystal":                "fire opal mexico orange",
    "Topaz":                            "topaz imperial orange crystal",
    "Tsavorite Garnet Crystal":         "tsavorite garnet green crystal",
    "Color-Change Garnet":              "color change garnet madagascar",
    "Spinel Crystal":                   "spinel crystal red gemstone",
    "Demantoid Garnet":                 "demantoid andradite garnet green",
    "Paraíba Tourmaline":               "paraiba tourmaline neon blue copper",
    "Sphene Crystal":                   "titanite sphene crystal yellow green",
    "Kornerupine Crystal":              "kornerupine crystal mineral",
    "Grandidierite Crystal":            "grandidierite crystal teal blue",
    "Jeremejevite Crystal":             "jeremejevite crystal rare mineral",
    "Amber with Insect Inclusion":      "amber insect inclusion fossil baltic",
    "Burmese Amber with Lizard Inclusion":"burmese amber cretaceous inclusion",
    "Jet Carved Specimen":              "jet whitby carved black organic gem",
    "Coral Specimen":                   "red coral specimen mediterranean",
    "Rough Emerald Crystal":            "emerald crystal rough colombian beryl",

    # Fossils
    "Trilobite":                        "trilobite fossil phacops enrolled",
    "Ammonite":                         "ammonite fossil polished section",
    "Fish Fossil":                      "fish fossil green river formation",
    "Mosasaur Tooth on Matrix":         "mosasaur tooth fossil cretaceous",
    "Megalodon Tooth Replica":          "megalodon shark tooth fossil",
    "Dinosaur Tooth":                   "dinosaur tooth fossil theropod",
    "Insect in Amber":                  "insect amber fossil eocene",
    "Spider in Amber":                  "spider amber burmese fossil",
    "Fern Fossil":                      "fern fossil carboniferous mazon creek",
    "Petrified Wood":                   "petrified wood silicified fossil",
    "Sea Urchin":                       "sea urchin micraster fossil chalk",
    "Crinoid Stem Section":             "crinoid stem fossil polished",
    "Nautiloid":                        "orthoceras nautiloid fossil polished",
    "Trace Fossil":                     "dinosaur footprint trace fossil",
    "Coprolite":                        "coprolite fossil feces",
    "Brachiopod Cluster":               "brachiopod spirifer fossil devonian",
    "Eurypterid":                       "eurypterid sea scorpion fossil silurian",
    "Horseshoe Crab":                   "horseshoe crab limulus fossil",
    "Plant Fossil":                     "sigillaria plant fossil carboniferous",
    "Shark Teeth":                      "shark teeth fossil miocene",
    "Mammoth Molar":                    "mammoth molar fossil pleistocene",
    "Glyptodon Osteoderms":             "glyptodon osteoderm fossil",
    "Plesiosaurian Vertebra":           "plesiosaur vertebra fossil jurassic",

    # Meteorites
    "Gibeon Iron Meteorite":            "gibeon meteorite widmanstatten etched",
    "Campo del Cielo Iron Meteorite":   "campo del cielo iron meteorite",
    "Sikhote-Alin Individual":          "sikhote-alin iron meteorite shrapnel",
    "Chondrite Meteorite":              "chondrite meteorite chondrules",
    "Carbonaceous Chondrite":           "carbonaceous chondrite cm2 meteorite",
    "Pallasite Meteorite":              "pallasite meteorite olivine iron",
    "Lunar Meteorite":                  "lunar meteorite mare basalt",
    "Martian Meteorite":                "martian meteorite shergottite",
    "Moldavite":                        "moldavite tektite green glass czech",
    "Libyan Desert Glass":              "libyan desert glass silica tektite",
    "Australite Button":                "australite button tektite australia",
    "Darwin Glass":                     "darwin glass tektite tasmania",
    "Iron Meteorite":                   "iron meteorite widmanstatten pattern",
    "Imilac Pallasite":                 "imilac pallasite meteorite olivine",
    "Seymchan Pallasite":               "seymchan pallasite meteorite",

    # Geological specimens
    "Amethyst Cathedral Geode":         "amethyst cathedral geode half",
    "Celestite Geode":                  "celestite geode blue crystal ohio",
    "Obsidian":                         "obsidian volcanic glass mahogany",
    "Fulgurite":                        "fulgurite lightning glass sand tube",
    "Banded Iron Formation":            "banded iron formation BIF precambrian",
    "Septarian Nodule":                 "septarian nodule polished calcite",
    "Volcanic Bomb":                    "volcanic bomb breadcrust lava",
    "Pele's Tears":                     "pele tears hawaiian basaltic glass",
    "Suevite":                          "suevite impact breccia meteorite crater",
    "Shatter Cone":                     "shatter cone impact structure",
    "Eclogite":                         "eclogite garnet omphacite metamorphic",
    "Oolitic Limestone":                "oolitic limestone ooids sedimentary",
    "Desert Varnish Sandstone":         "desert varnish sandstone rock art",
    "Chalk with Flint Nodule":          "flint nodule chalk cretaceous",
    "Garnet Schist":                    "garnet schist metamorphic mineral",
    "Pumice from Santorini":            "pumice volcanic santorini greece",
    "Serpentinite":                     "serpentinite ophiolite green rock",
    "Radiolarite":                      "radiolarite chert siliceous rock",
    "Conglomerate":                     "tillite glacial conglomerate",
}


def wiki_get(url, timeout=15):
    """HTTP GET with exponential backoff on 429."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = API_DELAY * (2 ** attempt)
                print(f"    Rate limited (429) — waiting {wait:.1f}s before retry {attempt+1}/{MAX_RETRIES}", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError(f"Gave up after {MAX_RETRIES} retries (429)")


def wikimedia_search(query):
    """Return filename or None."""
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",
        "srlimit": "8",
        "format": "json",
    })
    try:
        data = json.loads(wiki_get(f"{WIKI_API}?{params}"))
        results = data.get("query", {}).get("search", [])
        for result in results:
            title = result["title"]  # e.g. "File:Amethyst.jpg"
            filename = title.replace("File:", "")
            # Skip SVGs, animations, maps
            if not re.search(r'\.(jpg|jpeg|png|webp)$', filename, re.I):
                continue
            # Skip files that look like maps, diagrams, icons, logos
            if re.search(r'map|diagram|icon|logo|flag|coat|emblem|scheme|chart|graph|symbol',
                         filename, re.I):
                continue
            return filename
        return None
    except Exception as e:
        print(f"    Search error: {e}", file=sys.stderr)
        return None


def wikimedia_image_url(filename):
    """Return (thumb_url, page_url, author, license_short) or None."""
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": str(MAX_PX),
        "format": "json",
    })
    try:
        data = json.loads(wiki_get(f"{WIKI_API}?{params}"))
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            thumb_url = info.get("thumburl") or info.get("url")
            page_url = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(filename)}"
            meta = info.get("extmetadata", {})
            author = meta.get("Artist", {}).get("value", "Unknown")
            author = re.sub(r'<[^>]+>', '', author).strip()[:80]
            license_short = meta.get("LicenseShortName", {}).get("value", "Unknown")
            return thumb_url, page_url, author, license_short
        return None
    except Exception as e:
        print(f"    Imageinfo error: {e}", file=sys.stderr)
        return None


def download_and_optimize(url, out_path):
    """Download image, resize to MAX_PX, save as JPEG ≤ MAX_BYTES."""
    try:
        raw = wiki_get(url, timeout=30)
    except Exception as e:
        print(f"    Download error: {e}", file=sys.stderr)
        return False

    try:
        img = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception as e:
        print(f"    Image open error: {e}", file=sys.stderr)
        return False

    # Resize so longest side ≤ MAX_PX
    w, h = img.size
    if max(w, h) > MAX_PX:
        if w >= h:
            img = img.resize((MAX_PX, int(h * MAX_PX / w)), Image.LANCZOS)
        else:
            img = img.resize((int(w * MAX_PX / h), MAX_PX), Image.LANCZOS)

    # Save with decreasing quality until under MAX_BYTES
    for quality in (JPEG_QUALITY, 60, 50, 40, 30):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
        if buf.tell() <= MAX_BYTES:
            break

    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    return True


def safe_filename(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')[:80]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    with open(JSON_PATH) as f:
        products = json.load(f)

    # Load existing sources if resuming
    if os.path.exists(SOURCES_PATH):
        with open(SOURCES_PATH) as f:
            sources = json.load(f)
    else:
        sources = {}

    # Build base-name → [sku, ...] mapping
    base_to_skus = {}
    for p in products:
        base = p['name'].split(' — ')[0].strip()
        for prefix in ['Large ', 'Museum-Quality ', 'Exceptional ', 'Small ']:
            if base.startswith(prefix):
                base = base[len(prefix):]
        base_to_skus.setdefault(base, []).append(p['sku'])

    print(f"Unique base names: {len(base_to_skus)}")
    print(f"Total products:    {len(products)}")
    print()

    downloaded = 0
    reused = 0
    failed = 0

    # Process each unique base name
    for base_name, skus in sorted(base_to_skus.items()):
        # Determine the output filename (use first SKU as canonical)
        canonical_sku = skus[0]
        canonical_product = next(p for p in products if p['sku'] == canonical_sku)
        canonical_out = os.path.join(
            OUTPUT_DIR,
            f"{canonical_sku}-{safe_filename(canonical_product['name'])}.jpg"
        )

        # Already fetched this base name?
        if base_name in sources and os.path.exists(canonical_out):
            reused += len(skus)
            continue

        # Determine search query
        query = SEARCH_TERMS.get(base_name, base_name + " mineral specimen")

        print(f"[{downloaded+failed+1}/{len(base_to_skus)}] {base_name}")
        print(f"  Query: {query}")

        time.sleep(API_DELAY)
        filename = wikimedia_search(query)
        if not filename:
            print(f"  No result — keeping placeholder")
            failed += 1
            continue

        print(f"  File:  {filename}")
        time.sleep(API_DELAY)
        result = wikimedia_image_url(filename)
        if not result:
            print(f"  No image URL — keeping placeholder")
            failed += 1
            continue

        thumb_url, page_url, author, license_short = result
        print(f"  URL:   {thumb_url[:80]}…")

        # Download to canonical path
        ok = download_and_optimize(thumb_url, canonical_out)
        if not ok:
            print(f"  Download failed — keeping placeholder")
            failed += 1
            continue

        size_kb = os.path.getsize(canonical_out) / 1024
        print(f"  Saved: {size_kb:.1f} KB → {canonical_out}")

        # Record source attribution
        sources[base_name] = {
            "wikimedia_file": filename,
            "page_url": page_url,
            "thumb_url": thumb_url,
            "author": author,
            "license": license_short,
            "used_by_skus": skus,
        }

        # For variant SKUs, create symlinks or copies pointing to the same JPEG
        for sku in skus:
            if sku == canonical_sku:
                continue
            p = next((x for x in products if x['sku'] == sku), None)
            if not p:
                continue
            variant_out = os.path.join(
                OUTPUT_DIR,
                f"{sku}-{safe_filename(p['name'])}.jpg"
            )
            if not os.path.exists(variant_out):
                import shutil
                shutil.copy2(canonical_out, variant_out)

        downloaded += 1

        # Save sources incrementally (resume-safe)
        with open(SOURCES_PATH, "w") as f:
            json.dump(sources, f, indent=2)

    print()
    print(f"Done.")
    print(f"  Downloaded (new):  {downloaded}")
    print(f"  Reused (cached):   {reused}")
    print(f"  Failed/no result:  {failed}")
    print()

    # Count total JPEG files now in directory
    jpgs = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.jpg')]
    pngs = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
    print(f"  JPEG files in uploads: {len(jpgs)}")
    print(f"  PNG  files in uploads: {len(pngs)} (placeholders for unmatched)")

    total_mb = sum(
        os.path.getsize(os.path.join(OUTPUT_DIR, f))
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(('.jpg', '.png'))
    ) / (1024 * 1024)
    print(f"  Total uploads size:    {total_mb:.1f} MB")


if __name__ == '__main__':
    main()
