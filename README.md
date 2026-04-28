# Terra Collecta

**Premium geological specimen e-commerce demo for [Scolta](https://tag1.com) search technology.**

Browse 1,000 rare minerals, gemstones, fossils, meteorites, and geological specimens. Use natural language to find what you're looking for — "something blue and sparkly for a gift," "oldest thing you have," "space rock," "scary looking."

---

## Quick Start

```bash
git clone <repo-url>
cd terra-collecta
ddev start
```

That's it. DDEV automatically imports the database on first start. Open https://terra-collecta.ddev.site in your browser.

**Admin:** https://terra-collecta.ddev.site/wp-admin  
**Username:** `admin`  
**Password:** `admin`

---

## What's Included

| | Count |
|---|---|
| Total products | 1,000 |
| Minerals | 300 |
| Gemstones | 200 |
| Fossils | 200 |
| Meteorites | 100 |
| Geological Specimens | 100 |
| Curated Collections | 100 |

Each product has:
- Full literary description (2–3 paragraphs)
- Scientific details (chemical formula, crystal system, Mohs hardness, specific gravity, luster, transparency)
- Formation, locality, and collector notes
- Color-coded placeholder image (400×400px PNG)
- Realistic price ($15 common minerals → $50,000+ rare meteorites)
- Realistic stock (10–50 common items, 1–3 rare items)

---

## Stack

| Component | Version |
|---|---|
| WordPress | 6.9.4 |
| WooCommerce | 10.7.0 |
| PHP | 8.3 |
| MariaDB | 10.11 |
| Theme | TwentyTwentyFive child (terra-collecta) |
| DDEV | 1.24.7+ |

---

## Demo Behavior

**Cart:** Fully functional. Add items, view cart, adjust quantities.

**Checkout:** A friendly modal blocks completion:

> *"Thank you for your impeccable taste in geological wonders! Terra Collecta is a demonstration site for Scolta search technology. These specimens exist only in our carefully curated imagination."*

Click "Keep Exploring" to return to the shop.

---

## Scolta Showcase Queries

These queries demonstrate Scolta's semantic re-ranking:

| Query | Expected Results |
|---|---|
| something blue | lapis lazuli, azurite, labradorite, blue apatite |
| sparkly gift | quartz clusters, pyrite, tourmaline, opal |
| space rock | meteorites, tektites, impactites, Libyan desert glass |
| dinosaur | fossil teeth, coprolites, bone fragments |
| oldest thing you have | zircon (4.4Ga), iron meteorites, banded iron formation |
| wedding anniversary | gemstones, polished specimens, curated gift sets |
| scary looking | stibnite needles, crocoite, realgar |
| looks like gold | pyrite, chalcopyrite, native gold specimens |

---

## Rebuilding the Database

If you need to regenerate all products from scratch:

```bash
# 1. Regenerate product JSON (1,000 products)
python3 import/generate-products.py

# 2. Start DDEV (fresh WordPress install)
ddev start
ddev wp core install \
  --url="https://terra-collecta.ddev.site" \
  --title="Terra Collecta" \
  --admin_user="admin" \
  --admin_password="admin" \
  --admin_email="admin@terra-collecta.example.com" \
  --skip-email

# 3. Import products
ddev wp eval-file import/import-products.php

# 4. Generate and attach images
python3 import/generate-placeholders.py
ddev wp eval-file import/attach-images.php

# 5. Export database
ddev export-db --gzip --file=db/dump.sql.gz
```

---

## Updating Content

1. Make changes via wp-admin
2. Export: `ddev export-db --gzip --file=db/dump.sql.gz`
3. Commit: `git add db/dump.sql.gz && git commit -m "Update product database"`

---

## Updating WordPress / WooCommerce

```bash
ddev wp core update
ddev wp plugin update woocommerce
# Test site
ddev export-db --gzip --file=db/dump.sql.gz
git add db/dump.sql.gz wp-includes/ wp-admin/ wp-content/plugins/woocommerce/
git commit -m "Update WordPress and WooCommerce"
```

---

## Project Structure

```
terra-collecta/
├── .ddev/config.yaml          # DDEV configuration
├── .gitignore
├── db/dump.sql.gz             # Complete database (1,000 products)
├── wp-config.php              # DDEV-compatible WordPress config
├── wp-content/
│   ├── plugins/
│   │   ├── woocommerce/       # WooCommerce 10.7.0
│   │   └── scolta/            # Scolta search plugin
│   ├── themes/
│   │   ├── twentytwentyfive/  # Parent theme
│   │   └── terra-collecta/    # Child theme (charcoal/gold/stone-grey)
│   └── uploads/terra-collecta/ # 1,000 product placeholder images
├── import/
│   ├── products.json          # Source product data (reference)
│   ├── generate-products.py   # Product JSON generator
│   ├── import-products.php    # WP-CLI import script
│   ├── generate-placeholders.py # Image generator
│   └── attach-images.php      # WP-CLI image attachment script
├── SOURCES.md                 # Content provenance & licenses
└── README.md                  # This file
```

---

## Theme Colors

| Variable | Value | Use |
|---|---|---|
| `--tc-charcoal` | `#1a1a2e` | Primary background |
| `--tc-gold` | `#c9a45c` | Accents, prices, CTAs |
| `--tc-stone` | `#e0dcd3` | Body text |
| `--tc-dark-bg` | `#0f0f1e` | Header / footer |
| `--tc-card-bg` | `#23233a` | Product cards |

---

*Terra Collecta — A [Tag1 Consulting](https://tag1.com) demonstration for Scolta search technology.*
