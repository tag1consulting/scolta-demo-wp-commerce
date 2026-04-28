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
API_DELAY      = 2.0        # seconds between Wikimedia API calls
DOWNLOAD_DELAY = 5.0        # extra pause before each image download
MAX_RETRIES    = 5          # max retries on 429
MAX_WAIT       = 30.0       # cap per-retry backoff at this many seconds
WIKI_API     = "https://commons.wikimedia.org/w/api.php"
USER_AGENT   = "TerraCollectaDemo/1.0 (tag1.com; scolta-demo) python-urllib"

# ── Search-term overrides ─────────────────────────────────────────────────────
# Maps base product name → Wikimedia Commons search query (primary)
SEARCH_TERMS = {
    # Minerals
    "Amethyst Cluster":                  "amethyst geode crystal cluster",
    "Rose Quartz Sphere":                "rose quartz crystal mineral",
    "Citrine Crystal Point":             "citrine quartz crystal point",
    "Smoky Quartz Elestial":             "smoky quartz skeletal elestial crystal",
    "Agate Slice":                       "agate slice botswana polished",
    "Labradorite Freeform":              "labradorite feldspar labradorescence",
    "Moonstone with Adularescence":      "moonstone gemstone adularescence",
    "Amazonite Crystal":                 "amazonite feldspar crystal",
    "Black Tourmaline Schorl Crystal":   "schorl tourmaline crystal black",
    "Rubellite Tourmaline Crystal":      "rubellite tourmaline pink crystal",
    "Indicolite Tourmaline":             "indicolite tourmaline blue crystal",
    "Emerald Crystal in Matrix":         "emerald crystal beryl colombian",
    "Aquamarine Crystal":                "aquamarine beryl crystal",
    "Heliodor Crystal":                  "heliodor golden beryl crystal",
    "Goshenite":                         "goshenite beryl colorless crystal",
    "Grossular Garnet":                  "grossular garnet green crystal",
    "Spessartine Garnet Crystal":        "spessartine garnet orange crystal",
    "Rhodolite Garnet Crystal":          "rhodolite garnet crystal",
    "Topaz":                             "topaz crystal specimen mineral",
    "Blue Topaz Crystal":                "blue topaz crystal",
    "Purple Fluorite Octahedron":        "fluorite octahedron purple crystal",
    "Green Fluorite Cubic Cluster":      "fluorite green cubic crystal",
    "Malachite Botryoidal Specimen":     "malachite botryoidal mineral",
    "Azurite-Malachite Crystal Cluster": "azurite malachite mineral",
    "Pyrite Cube Cluster":               "pyrite cube crystal navajun",
    "Chalcopyrite Crystal on Sphalerite":"chalcopyrite sphalerite iridescent mineral",
    "Native Gold in Quartz Vein":        "native gold quartz vein mineral",
    "Stibnite Crystal Group":            "stibnite crystal antimony mineral",
    "Crocoite Crystal Cluster":          "crocoite crystal red orange",
    "Vanadinite on Barite":              "vanadinite crystal red hexagonal",
    "Wulfenite Crystal Plate":           "wulfenite crystal orange plate",
    "Rhodochrosite Stalactite Slice":    "rhodochrosite stalactite argentina",
    "Selenite Gypsum Wand":              "selenite gypsum crystal clear",
    "Desert Rose Barite":                "desert rose barite crystal",
    "Celestite Geode":                   "celestite geode crystal blue",
    "Calcite Dog-Tooth Cluster":         "calcite dogtooth crystal cluster",
    "Iceland Spar":                      "iceland spar optical calcite",
    "Apophyllite Crystal Cluster on Stilbite": "apophyllite stilbite crystal india",
    "Rhodonite Specimen":                "rhodonite mineral pink",
    "Dioptase Crystal Cluster":          "dioptase crystal green copper",
    "Zircon Crystal in Pegmatite":       "zircon crystal mineral",
    "Pyrrhotite Crystal":                "pyrrhotite crystal magnetic iron sulfide",
    "Realgar Crystal on Orpiment":       "realgar crystal red arsenic orpiment",
    "Wollastonite Spray":                "wollastonite mineral calcium silicate",
    "Staurolite Twin":                   "staurolite fairy stone twin crystal",
    "Prehnite Stalactite":               "prehnite green botryoidal stalactite",
    "Kunzite Crystal":                   "kunzite pink spodumene crystal",
    "Hiddenite Crystal":                 "hiddenite green spodumene crystal",
    "Benitoite Crystal on Natrolite":    "benitoite crystal blue",
    "Tanzanite Crystal":                 "tanzanite zoisite crystal blue",
    "Alexandrite Crystal":               "alexandrite color change chrysoberyl",
    "Painite Crystal":                   "painite crystal myanmar mineral",
    "Red Beryl Crystal":                 "red beryl bixbite utah crystal",
    "Euclase Crystal":                   "euclase crystal beryllium mineral",
    "Fluorapatite Crystal":              "apatite crystal hexagonal green",
    "Clinozoisite Crystal":              "clinozoisite epidote crystal alpine",
    "Manganite Crystal":                 "manganite crystal manganese mineral",
    "Native Silver Wires":               "native silver wire kongsberg",
    "Native Copper Arborescent":         "native copper arborescent dendritic",
    "Hematite Rose":                     "iron rose hematite mineral",
    "Ilvaite Crystal":                   "ilvaite crystal mineral",
    "Kyanite Crystal":                   "kyanite blue blade crystal",
    "Sillimanite Fibrous":               "sillimanite fibrolite mineral",

    # Gemstones
    "Diamond Crystal":                   "diamond crystal natural rough",
    "Ruby Crystal in Matrix":            "ruby corundum red crystal matrix",
    "Padparadscha Sapphire Crystal":     "padparadscha sapphire gemstone",
    "Star Sapphire":                     "star sapphire cabochon asterism",
    "Cat's Eye Chrysoberyl":             "cat eye chrysoberyl chatoyancy",
    "Star Ruby":                         "star ruby cabochon asterism",
    "Black Opal":                        "black opal lightning ridge",
    "White Opal":                        "opal white precious gemstone",
    "Fire Opal Crystal":                 "fire opal mexico orange",
    "Tsavorite Garnet Crystal":          "tsavorite garnet green crystal",
    "Color-Change Garnet":               "color change garnet alexandrite effect",
    "Spinel Crystal":                    "spinel crystal red gemstone",
    "Demantoid Garnet":                  "demantoid andradite garnet green",
    "Paraíba Tourmaline":                "paraiba tourmaline blue copper",
    "Sphene Crystal":                    "titanite sphene crystal yellow green",
    "Kornerupine Crystal":               "Kornerupine mineral gemstone",
    "Grandidierite Crystal":             "grandidierite teal blue mineral",
    "Jeremejevite Crystal":              "jeremejevite crystal mineral",
    "Amber with Insect Inclusion":       "amber insect inclusion fossil baltic",
    "Burmese Amber with Lizard Inclusion":"burmese amber cretaceous inclusion",
    "Jet Carved Specimen":               "jet gemstone black organic whitby",
    "Coral Specimen":                    "red coral branch specimen",
    "Rough Emerald Crystal":             "emerald crystal rough colombian beryl",

    # Fossils
    "Trilobite":                         "trilobite fossil enrolled",
    "Ammonite":                          "ammonite fossil polished section",
    "Fish Fossil":                       "fish fossil green river formation",
    "Mosasaur Tooth on Matrix":          "mosasaur tooth fossil cretaceous",
    "Megalodon Tooth Replica":           "megalodon shark tooth fossil",
    "Dinosaur Tooth":                    "dinosaur tooth fossil theropod",
    "Insect in Amber":                   "insect amber fossil eocene",
    "Spider in Amber":                   "spider amber fossil inclusion",
    "Fern Fossil":                       "fern fossil carboniferous",
    "Petrified Wood":                    "petrified wood silicified fossil",
    "Sea Urchin":                        "echinoid sea urchin fossil",
    "Crinoid Stem Section":              "crinoid stem fossil polished",
    "Nautiloid":                         "orthoceras nautiloid fossil polished",
    "Trace Fossil":                      "dinosaur footprint trace fossil",
    "Coprolite":                         "coprolite fossil feces",
    "Brachiopod Cluster":                "brachiopod fossil shell devonian",
    "Eurypterid":                        "eurypterid fossil sea scorpion",
    "Horseshoe Crab":                    "horseshoe crab limulus fossil",
    "Plant Fossil":                      "sigillaria plant fossil carboniferous",
    "Shark Teeth":                       "shark teeth fossil miocene",
    "Mammoth Molar":                     "mammoth molar fossil pleistocene",
    "Glyptodon Osteoderms":              "glyptodon osteoderm fossil",
    "Plesiosaurian Vertebra":            "plesiosaur vertebra fossil jurassic",

    # Meteorites
    "Gibeon Iron Meteorite":             "gibeon meteorite widmanstatten etched",
    "Campo del Cielo Iron Meteorite":    "campo del cielo iron meteorite",
    "Sikhote-Alin Individual":           "sikhote-alin iron meteorite shrapnel",
    "Chondrite Meteorite":               "chondrite meteorite chondrules",
    "Carbonaceous Chondrite":            "carbonaceous chondrite cm2 meteorite",
    "Pallasite Meteorite":               "pallasite meteorite olivine iron",
    "Lunar Meteorite":                   "lunar meteorite mare basalt",
    "Martian Meteorite":                 "martian meteorite shergottite",
    "Moldavite":                         "moldavite tektite green glass czech",
    "Libyan Desert Glass":               "libyan desert glass silica tektite",
    "Australite Button":                 "australite tektite button australia",
    "Darwin Glass":                      "darwin glass tektite tasmania",
    "Iron Meteorite":                    "iron meteorite widmanstatten pattern",
    "Imilac Pallasite":                  "imilac pallasite meteorite olivine",
    "Seymchan Pallasite":                "seymchan pallasite meteorite",

    # Geological specimens
    "Amethyst Cathedral Geode":          "amethyst cathedral geode half",
    "Obsidian":                          "obsidian volcanic glass mahogany",
    "Fulgurite":                         "fulgurite lightning glass sand tube",
    "Banded Iron Formation":             "banded iron formation BIF precambrian",
    "Septarian Nodule":                  "septarian nodule polished calcite",
    "Volcanic Bomb":                     "volcanic bomb breadcrust lava",
    "Pele's Tears":                      "pele tears hawaiian basaltic glass",
    "Suevite":                           "suevite breccia nordlingen impact",
    "Shatter Cone":                      "shatter cone impact structure",
    "Eclogite":                          "eclogite garnet omphacite metamorphic",
    "Oolitic Limestone":                 "oolitic limestone ooids sedimentary",
    "Desert Varnish Sandstone":          "desert varnish sandstone rock art",
    "Chalk with Flint Nodule":           "flint nodule chalk cretaceous",
    "Garnet Schist":                     "garnet schist metamorphic rock",
    "Pumice from Santorini":             "pumice volcanic santorini greece",
    "Serpentinite":                      "serpentinite ophiolite green rock",
    "Radiolarite":                       "radiolarite chert siliceous rock",
    "Conglomerate":                      "tillite glacial conglomerate",

    # Curated Collections — use representative specimen imagery
    "Gift Set":                          "mineral crystal collection box gift",
    "Fluorescent Mineral Set":           "fluorescent minerals ultraviolet shortwave",
    "Meteorite Collectors Set":          "meteorite collection iron chondrite pallasite",
    "Educational Kit":                   "mineral rock collection identification",
    "Geological Timeline Collection":    "geological rock specimen collection formation",
    "Rainbow Minerals Collection":       "colorful mineral collection malachite azurite",
    "Space Rocks Starter Kit":           "meteorite tektite impactite collection",
    "Crystal Healing Skeptic's Kit":     "crystal quartz amethyst mineral collection",
    "Collector's Gemstone Rough Box":    "rough gemstone crystal collection assortment",
    "World Tour Collection":             "mineral specimen collection display tray",
}

# Known Wikimedia filenames for items whose search keeps failing — skips the
# search API call entirely and goes straight to imageinfo + download.
KNOWN_FILENAMES = {
    "Kunzite Crystal":               "Spodumene-191611.jpg",
    "Libyan Desert Glass":           "Libyan Desert Glass tektite (Oligocene, 28.5 Ma; Libyan Desert, Egypt) 1.jpg",
    "Manganite Crystal":             "Manganite-239863.jpg",
    "Native Copper Arborescent":     "Copper-35877.jpg",
    "Nautiloid":                     "Orthoceras characters.JPG",
    "Paraíba Tourmaline":            "Tourmaline-49508.jpg",
    "Prehnite Stalactite":           "Prehnite-121759.jpg",
    "Rainbow Minerals Collection":   "Cyanotrichite-Malachite-Azurite-147025.jpg",
    "Rhodochrosite Stalactite Slice":"Rhodochrosite-50006.jpg",
    "Ruby Crystal in Matrix":        "Corundum (Variety trapiche ruby)-649830.jpg",
    "Smoky Quartz Elestial":         "Smoky-quartz-TUCQTZ09-03-arkenstone-irocks.png",
    "Topaz":                         "Topaz-imperial topaz1b.jpg",
    "Trilobite":                     "Phacops enrolled.png",
    "World Tour Collection":         "Mineralien.jpg",
    "Wulfenite Crystal Plate":       "Wulfenite-Calcite-191707.jpg",
}

# Simpler fallback queries tried if the primary returns no result
SEARCH_FALLBACKS = {
    "Agate Slice":                       "agate slice mineral",
    "Smoky Quartz Elestial":             "smoky quartz crystal",
    "Goshenite":                         "beryl crystal colorless white",
    "Grossular Garnet":                  "grossular garnet crystal",
    "Topaz":                             "topaz crystal",
    "Chalcopyrite Crystal on Sphalerite":"chalcopyrite crystal mineral",
    "Crocoite Crystal Cluster":          "crocoite crystal",
    "Rhodochrosite Stalactite Slice":    "rhodochrosite crystal mineral",
    "Celestite Geode":                   "celestite crystal mineral",
    "Calcite Dog-Tooth Cluster":         "calcite crystal cluster",
    "Prehnite Stalactite":               "prehnite crystal green",
    "Kunzite Crystal":                   "kunzite crystal mineral",
    "Benitoite Crystal on Natrolite":    "benitoite crystal mineral",
    "Tanzanite Crystal":                 "tanzanite crystal mineral",
    "Painite Crystal":                   "painite mineral",
    "Euclase Crystal":                   "euclase crystal",
    "Fluorapatite Crystal":              "apatite crystal mineral",
    "Clinozoisite Crystal":              "clinozoisite crystal",
    "Manganite Crystal":                 "manganite crystal",
    "Native Silver Wires":               "native silver mineral",
    "Native Copper Arborescent":         "native copper mineral",
    "Hematite Rose":                     "hematite iron rose specular mineral",
    "Ilvaite Crystal":                   "ilvaite mineral crystal",
    "Kyanite Crystal":                   "kyanite crystal mineral",
    "Realgar Crystal on Orpiment":       "realgar crystal mineral",
    "Wulfenite Crystal Plate":           "wulfenite crystal",
    "Labradorite Freeform":              "labradorite mineral",
    "Libyan Desert Glass":               "libyan glass tektite",
    "Diamond Crystal":                   "diamond crystal rough",
    "Ruby Crystal in Matrix":            "ruby corundum crystal",
    "Padparadscha Sapphire Crystal":     "padparadscha sapphire",
    "Color-Change Garnet":               "garnet color change",
    "Kornerupine Crystal":               "kornerupine mineral",
    "Grandidierite Crystal":             "grandidierite mineral",
    "Jeremejevite Crystal":              "jeremejevite mineral",
    "Jet Carved Specimen":               "jet gemstone black",
    "Paraíba Tourmaline":                "tourmaline blue copper",
    "White Opal":                        "opal white gemstone",
    "Trilobite":                         "trilobite fossil",
    "Brachiopod Cluster":                "brachiopod fossil",
    "Eurypterid":                        "eurypterid fossil",
    "Nautiloid":                         "orthoceras fossil",
    "Sea Urchin":                        "echinoid fossil",
    "Spider in Amber":                   "spider amber fossil",
    "Australite Button":                 "australite tektite",
    "Garnet Schist":                     "schist metamorphic rock",
    "Suevite":                           "suevite breccia impact",
    "Gift Set":                          "mineral crystal display collection",
    "Fluorescent Mineral Set":           "fluorescent calcite mineral",
    "Meteorite Collectors Set":          "meteorite collection",
    "Educational Kit":                   "mineral collection rocks",
    "Geological Timeline Collection":    "geological rock collection",
    "Rainbow Minerals Collection":       "colorful minerals collection",
    "Space Rocks Starter Kit":           "meteorite space rock",
    "Crystal Healing Skeptic's Kit":     "crystal mineral collection",
    "Collector's Gemstone Rough Box":    "rough gemstone mineral",
    "World Tour Collection":             "mineral specimen worldwide",
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
                wait = min(API_DELAY * (2 ** attempt), MAX_WAIT)
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
        "srlimit": "20",
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

        print(f"[{downloaded+failed+1}/{len(base_to_skus)}] {base_name}")

        # Use known filename directly (skips search API call)
        if base_name in KNOWN_FILENAMES:
            filename = KNOWN_FILENAMES[base_name]
            print(f"  Known: {filename}")
        else:
            query = SEARCH_TERMS.get(base_name, base_name.split()[0] + " crystal mineral")
            print(f"  Query: {query}")

            time.sleep(API_DELAY)
            filename = wikimedia_search(query)

            # Try fallback query if primary failed
            if not filename and base_name in SEARCH_FALLBACKS:
                fallback = SEARCH_FALLBACKS[base_name]
                print(f"  Fallback: {fallback}")
                time.sleep(API_DELAY)
                filename = wikimedia_search(fallback)

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

        # Extra pause before image download to respect upload.wikimedia.org limits
        time.sleep(DOWNLOAD_DELAY)
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
