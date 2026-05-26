<?php
/**
 * Configure Scolta filter and sortable fields for Terra Collecta.
 *
 * Run with: ddev wp eval-file import/setup-scolta-filters.php
 */
$settings = get_option('scolta_settings', []);

$settings['sortable_fields'] = ['price', 'mohs_hardness', 'date'];
$settings['sortable_field_descriptions'] = [
    'price' => 'Product price in USD (typically $5-$30,000)',
    'mohs_hardness' => 'Mohs hardness scale (1=talc to 10=diamond)',
    'date' => 'Date product was added to the store',
];

$settings['filter_fields'] = ['category', 'crystal_system'];
$settings['filter_field_descriptions'] = [
    'category' => 'Product category. Map the user\'s query to one of these values: Minerals (raw mineral specimens, crystals, ores), Gemstones (cut and polished gems, precious and semi-precious stones), Fossils (paleontological specimens, petrified remains, amber inclusions), Meteorites (extraterrestrial specimens, iron meteorites, stony meteorites, pallasites), Geological Specimens (rock samples, geological formations), Curated Collections (themed sets, gift boxes, starter collections)',
    'crystal_system' => 'Crystallographic system. Values: Cubic (isometric, diamond, pyrite, fluorite, garnet), Hexagonal (quartz, beryl, emerald, tourmaline, apatite), Trigonal (calcite, rhodochrosite, hematite), Orthorhombic (topaz, olivine, aragonite, barite), Monoclinic (gypsum, orthoclase, augite, jade), Triclinic (labradorite, amazonite, turquoise, kyanite), Tetragonal (zircon, rutile, cassiterite), Amorphous (obsidian, opal, glass)',
];

update_option('scolta_settings', $settings);
echo "Scolta filter settings updated.\n";
