# Terra Collecta — Content Sources & Licenses

This file documents the origin of all content, data, and media used in the Terra Collecta demonstration site.

---

## Overview

Terra Collecta is a fictional e-commerce demonstration site. All 1,000 products are imaginary specimens — names, prices, descriptions, and inventory levels are generated for demonstration purposes only. No real transactions are processed.

---

## Product Data

### Mineral, Gemstone, Fossil, Meteorite & Geological Specimen Data

All product data (names, localities, chemical formulas, crystal systems, Mohs hardness values, specific gravities, luster types, formation narratives, collector notes) was **generated from curated geological reference knowledge** compiled for this demonstration.

Scientific accuracy was a design goal: chemical formulas, crystal systems, and Mohs hardness values reflect established mineralogical literature. Where demo data diverges from real specimens (e.g., prices for extremely rare minerals, stock levels for unique specimens), this is clearly a product of the fictional e-commerce context.

**Reference sources used for scientific accuracy:**

- Mindat.org — the world's largest mineralogy database (https://www.mindat.org). Data accessed under open research use.
- Smithsonian National Museum of Natural History — Gem & Mineral collection references (https://geogallery.si.edu)
- Anthony, Bideaux, Bladh, Nichols: *Handbook of Mineralogy* (Mineralogical Society of America)
- Klein & Dutrow: *Manual of Mineral Science* (23rd ed., Wiley)
- Wenk & Bulakh: *Minerals: Their Constitution and Origin* (Cambridge University Press)

**Content generation:** All narrative product descriptions were written programmatically from geological reference data compiled by the site authors. No AI-generated text from external services is used in production product descriptions.

---

## Product Images

All product images in `wp-content/uploads/terra-collecta/` are **programmatically generated placeholder images** created by the `import/generate-placeholders.py` script included in this repository.

**Image specifications:**
- Format: PNG
- Dimensions: 400 × 400 pixels
- Content: Solid-color background with slight texture variation, color-coded by mineral category
- Generation method: Pure Python (stdlib only — no external dependencies)
- License: Original work, dedicated to the public domain

**Color key:**
| Category | Background Color |
|---|---|
| Minerals | Deep indigo (#2A2A44) |
| Gemstones | Deep ruby (#3E162C) |
| Fossils | Sediment brown (#372D1C) |
| Meteorites | Near-black (#202020) |
| Geological Specimens | Dark green (#1C2A1C) |
| Curated Collections | Dark gold (#2A2210) |

Specific mineral types use color-keyed overrides (e.g., amethyst → purple, malachite → green, pyrite → gold) defined in `generate-placeholders.py`.

**A note on real geological specimen images:**

For a production deployment, we recommend sourcing photographs from:

1. **Wikimedia Commons** — Large collection of CC0/public domain mineral photographs. Example searches: `https://commons.wikimedia.org/wiki/Category:Minerals`
2. **Smithsonian Open Access** — The Smithsonian Institution's digitized collection, freely available for non-commercial use: https://www.si.edu/openaccess
3. **USGS Image Gallery** — Public domain geological photographs: https://www.usgs.gov/media/images
4. **Unsplash** — Free-to-use photography (search "mineral", "gemstone", "crystal"): https://unsplash.com
5. **Pexels** — Free-to-use photography: https://www.pexels.com

**Image fetch script:** `import/fetch-real-images.sh` (not included in this release) would automate downloading, resizing to max 600px width, and JPEG compression of real photographs. Placeholder images are used in this demo to avoid distributing third-party content without per-image credit tracking.

---

## Software

| Component | Version | License | Source |
|---|---|---|---|
| WordPress | 6.9.4 | GPL-2.0 | https://wordpress.org |
| WooCommerce | 10.7.0 | GPL-3.0 | https://woocommerce.com |
| TwentyTwentyFive | 1.4 | GPL-2.0 | https://wordpress.org/themes/twentytwentyfive |
| DDEV | 1.24.7 | Apache-2.0 | https://ddev.com |
| MariaDB | 10.11 | GPL-2.0 | https://mariadb.org |

---

## Scolta Plugin

The Scolta WooCommerce search plugin is proprietary software developed by Tag1 Consulting. It is committed to this repository for demonstration purposes only and is not licensed for redistribution.

---

## Site Content

| Content Type | Origin | License |
|---|---|---|
| Product names | Original, based on mineralogical conventions | Original work |
| Product descriptions | Original geological prose | Original work |
| Scientific data | Compiled from public mineralogical literature | Facts are not copyrightable |
| Placeholder images | Programmatically generated | Public domain |
| Theme CSS/JS | Original work | GPL-2.0 |
| Theme PHP | Original work | GPL-2.0 |

---

## Disclaimer

Terra Collecta is a demonstration site. All products, prices, and inventory are fictional. No transactions are processed. The geological descriptions are written for educational entertainment and should not be used as authoritative scientific references for purchase decisions involving real specimens.

---

*Last updated: 2026-04-28*
*Maintained by Tag1 Consulting — https://tag1.com*
