#!/usr/bin/env python3
"""
Generate 1,000 Terra Collecta geological specimen products.
Output: import/products.json
"""
import json, random, math

random.seed(42)

# ──────────────────────────────────────────────────────────────────────────────
# PRODUCT TEMPLATES
# ──────────────────────────────────────────────────────────────────────────────

MINERALS = [
    # (name, locality, formula, crystal_sys, mohs, sg, luster, transparency, price_range, story_seed)
    ("Amethyst Cluster", "Artigas District, Uruguay",
     "SiO₂", "Trigonal", "7", "2.65", "Vitreous", "Transparent to translucent",
     (28, 185),
     "The deep violet comes from trace iron and natural irradiation during crystal growth. Each cathedral-shaped cluster is a frozen moment from 135 million years ago, when silica-rich groundwater seeped into basalt voids left by ancient volcanism."),

    ("Rose Quartz Sphere", "Minas Gerais, Brazil",
     "SiO₂", "Trigonal", "7", "2.65", "Vitreous to waxy", "Translucent",
     (22, 120),
     "The blush hue is caused by microscopic inclusions of dumortierite or titanite needles — the exact mechanism debated for decades. Polished into spheres, the diffused light creates a luminous glow that photographers chase and collectors covet."),

    ("Citrine Crystal Point", "Rio Grande do Sul, Brazil",
     "SiO₂", "Trigonal", "7", "2.65", "Vitreous", "Transparent",
     (18, 95),
     "Most commercial citrine is heat-treated amethyst, but this naturally golden quartz owes its color to ferric iron trapped in the lattice during hydrothermal crystallization. Natural citrine is genuinely rare — demand far exceeds supply."),

    ("Smoky Quartz Elestial", "Nagar, Pakistan",
     "SiO₂", "Trigonal", "7", "2.65", "Vitreous", "Transparent to smoky",
     (35, 220),
     "Elestial quartzes grow in skeletal layers, the crystal repeatedly starting and stopping in a record of changing hydrothermal conditions. The smoky grey tones come from natural irradiation from surrounding granite. Pakistani specimens are prized for exceptional clarity and complex terminations."),

    ("Agate Slice — Fortification Pattern", "Botswana, Africa",
     "SiO₂", "Trigonal", "6.5–7", "2.60", "Waxy", "Translucent",
     (25, 150),
     "Botswana agate forms in volcanic amygdales — gas bubbles in ancient lava flows — over millions of years as chalcedony layers deposit concentrically. The fortification pattern maps each episode of deposition: a geological autobiography in concentric arcs."),

    ("Labradorite Freeform", "Labrador, Canada",
     "NaAlSi₃O₈–CaAl₂Si₂O₈", "Triclinic", "6–6.5", "2.69", "Vitreous to pearly", "Translucent",
     (35, 280),
     "Labradorescence — that ghostly play of blue, green, and gold — occurs when light diffracts between ultra-thin feldspar layers deposited during slow magmatic cooling. Each specimen is a prism masquerading as stone. Turn it in sunlight and it remembers something ancient."),

    ("Moonstone with Adularescence", "Dumbara District, Sri Lanka",
     "(Na,K)AlSi₃O₈", "Monoclinic", "6–6.5", "2.56", "Pearly", "Translucent",
     (55, 480),
     "The floating blue glow — adularescence — is light scattering off alternating layers of orthoclase and albite feldspar. Sri Lankan moonstone has been prized since antiquity. Roman naturalist Pliny the Elder believed it formed from solidified moonbeams, which, poetically, is not entirely wrong."),

    ("Amazonite Crystal", "Pikes Peak, Colorado, USA",
     "KAlSi₃O₈", "Triclinic", "6–6.5", "2.56", "Vitreous", "Opaque to translucent",
     (28, 165),
     "This striking blue-green feldspar gets its color from trace lead and water impurities — a sensitive indicator of the fluid chemistry present when the Crystal System granite cooled slowly, millions of years ago. Colorado specimens are among the world's finest."),

    ("Black Tourmaline Schorl Crystal", "Erongo Mountain, Namibia",
     "NaFe₃Al₆(BO₃)₃Si₆O₁₈(OH)₄", "Trigonal", "7–7.5", "3.18", "Vitreous to resinous", "Opaque",
     (22, 140),
     "Schorl is the most common tourmaline, yet these striated black prisms from Namibia's Erongo region are exceptional — sharp terminations, lustrous faces, and often perched on clusters of smoky quartz in a composition nature arranged over millions of years."),

    ("Rubellite Tourmaline Crystal", "Pala, California, USA",
     "Na(Li,Al)₃Al₆(BO₃)₃Si₆O₁₈(OH)₄", "Trigonal", "7–7.5", "3.06", "Vitreous", "Transparent to translucent",
     (180, 2400),
     "Pala, California produced world-famous rubellites — deep raspberry-red lithium tourmalines — in mines that captivated Tiffany & Co. in the 1800s. This color comes from manganese. A fine rubellite in daylight holds a warmth that rubies can only envy."),

    ("Indicolite Tourmaline", "Paprok, Nuristan, Afghanistan",
     "Na(Fe,Al)₃Al₆(BO₃)₃Si₆O₁₈(OH)₄", "Trigonal", "7–7.5", "3.14", "Vitreous", "Transparent",
     (220, 3200),
     "Blue tourmaline — indicolite — requires iron in the right oxidation state during crystallization. Afghan specimens from the Kunar pegmatites rival anything from Brazil. The color ranges from teal to deep ink-blue, with the finest showing a slightly greenish hue in one direction (tourmaline is strongly pleochroic)."),

    ("Emerald Crystal in Matrix", "Muzo Mine, Boyacá, Colombia",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.76", "Vitreous", "Transparent",
     (380, 8500),
     "Muzo Colombian emeralds are a geological anomaly — formed not in pegmatites like most beryls, but in black shales rich in carbon, chromium, and vanadium. The resulting color is the purest green in the mineral kingdom. Owning a Muzo emerald crystal in its original calcite matrix is owning a piece of the world's most romanticized mine."),

    ("Aquamarine Crystal", "Shigar Valley, Pakistan",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.69", "Vitreous", "Transparent",
     (165, 2200),
     "The name means 'seawater' in Latin — an apt description of that particular blue-green, the color of a shallow tropical ocean in morning light. Pakistani aquamarine from the Karakoram region grows in phenomenal prisms, sometimes measuring thirty centimeters. The color comes from ferrous iron."),

    ("Heliodor Crystal", "Erongo Region, Namibia",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.70", "Vitreous", "Transparent",
     (85, 680),
     "Golden beryl — heliodor, 'gift of the sun' — gets its yellow from trace ferric iron. Namibian crystals from the Erongo granite are among the most gem-quality in the world, forming long striated prisms of crystalline gold on pegmatite matrices."),

    ("Goshenite — White Beryl", "Goshen, Hampshire County, Massachusetts, USA",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.66", "Vitreous", "Transparent",
     (45, 320),
     "The pure, colorless member of the beryl family, named for the Massachusetts town where it was first described. Without chromophores it is optically flawless — used historically as lens substitutes and for spectacles before glass-working advanced. Gem quality goshenite is paradoxically rarer than colored beryls."),

    ("Grossular Garnet — Tsavorite", "Merelani Hills, Tanzania",
     "Ca₃Al₂(SiO₄)₃", "Cubic", "7–7.5", "3.59", "Vitreous", "Transparent",
     (420, 9800),
     "Discovered in 1967 along the Kenya-Tanzania border by British geologist Campbell Bridges, tsavorite quickly rivaled emerald for intense green color — with greater hardness, better clarity, and no oiling treatments. It forms in metamorphic rocks under conditions so specific that new deposits remain elusive."),

    ("Spessartine Garnet Crystal", "Navegador Mine, Minas Gerais, Brazil",
     "Mn₃Al₂(SiO₄)₃", "Cubic", "7–7.5", "4.19", "Vitreous", "Transparent to translucent",
     (95, 1200),
     "Mandarin-orange spessartine — manganese garnet — from this famous Minas Gerais locality is among the most vivid specimens in mineralogy. The color is the saturated orange of molten glass, the luster adamantine. Collectors waited decades for material this clean."),

    ("Rhodolite Garnet Crystal", "Umba Valley, Tanzania",
     "(Mg,Fe)₃Al₂(SiO₄)₃", "Cubic", "7–7.5", "3.84", "Vitreous", "Transparent",
     (65, 580),
     "Rhodolite — a magnesium-iron garnet intermediate — occupies the most desirable color territory between pyrope red and almandine purple. Tanzanian material from the Umba Valley is legendary: deeply saturated raspberry-rose, high clarity, and a brilliance that outperforms ruby-colored stones costing ten times more."),

    ("Topaz — Imperial Orange", "Ouro Preto, Minas Gerais, Brazil",
     "Al₂SiO₄(F,OH)₂", "Orthorhombic", "8", "3.53", "Vitreous", "Transparent",
     (280, 4500),
     "Imperial topaz in the precious sherry-to-deep-orange range is found in one place on Earth: the hills above Ouro Preto. The color comes from chromophoric impurities stabilized during crystallization in topaz-bearing pegmatites. Brazilian law once restricted export to protect royal reserves. Some specimens still carry that weight of exclusivity."),

    ("Blue Topaz Crystal — Natural", "Schneckenstein, Saxony, Germany",
     "Al₂SiO₄(F,OH)₂", "Orthorhombic", "8", "3.53", "Vitreous", "Transparent",
     (120, 850),
     "Natural blue topaz — as opposed to irradiated commercial blue — is remarkably rare. The Schneckenstein locality in Saxony has produced crystals since the 1700s. The pale blue is caused by natural radiation from surrounding granites, acting over geological time. It is patience made visible."),

    ("Purple Fluorite Octahedron", "Cave-in-Rock, Illinois, USA",
     "CaF₂", "Cubic", "4", "3.18", "Vitreous", "Transparent to translucent",
     (18, 95),
     "Illinois' Cave-in-Rock fluorite district produced some of history's greatest fluorite specimens — giant cubic and octahedral crystals in purple, yellow, and green. The cubic cleavage is perfect in three directions; split any crystal and you get smooth, mirror-perfect faces. The purple comes from color centers caused by natural irradiation."),

    ("Green Fluorite Cubic Cluster", "Xianghualing Mine, Hunan, China",
     "CaF₂", "Cubic", "4", "3.18", "Vitreous", "Transparent",
     (22, 145),
     "Hunan province produces prolific fluorite in every color, but the emerald-green cubic crystals from Xianghualing — sometimes meter-sized — are a category apart. The green comes from trace yttrium and other rare earth elements. Under short-wave UV, they fluoresce intensely blue — fluorite gave fluorescence its name."),

    ("Malachite Botryoidal Specimen", "Tenke Mine, Katanga, DR Congo",
     "Cu₂(CO₃)(OH)₂", "Monoclinic", "3.5–4", "3.88", "Vitreous to silky", "Opaque",
     (45, 380),
     "The peacock-green banding of malachite records episodes of copper-rich groundwater flowing through limestone — each ring a chapter of chemistry. Katanga's Tenke district is the world's most productive copper basin, and its malachite is correspondingly spectacular: deep greens, tight banding, botryoidal surfaces like compacted velvet."),

    ("Azurite-Malachite Crystal Cluster", "Chessy-les-Mines, France",
     "Cu₃(CO₃)₂(OH)₂ / Cu₂(CO₃)(OH)₂", "Monoclinic", "3.5–4", "3.77", "Vitreous", "Translucent to opaque",
     (85, 650),
     "Azurite — deep Prussian blue — gradually converts to green malachite as conditions change. The Chessy locality near Lyon gave azurite its historical name 'chessylite.' Specimens showing both minerals in a single cluster are among mineralogy's most painterly."),

    ("Pyrite Cube Cluster", "Navajún, La Rioja, Spain",
     "FeS₂", "Cubic", "6–6.5", "5.01", "Metallic", "Opaque",
     (35, 280),
     "Navajún produces the most geometrically perfect pyrite cubes on Earth — faces so flat they reflect like mirrors, edges so sharp they appear machined. The formation mechanism is debated but involves replacement of organic material in marine sediments. Each cube grew slowly in Cretaceous seafloor mud, achieving precision a factory would envy."),

    ("Chalcopyrite Crystal on Sphalerite", "Huaron, Pasco, Peru",
     "CuFeS₂", "Tetragonal", "3.5–4", "4.35", "Metallic", "Opaque",
     (28, 175),
     "Chalcopyrite — brassy yellow, iridescent when tarnished — is Earth's primary copper ore, but Peru's Huaron mine produces crystals of sculptural quality atop contrasting dark sphalerite matrices. The iridescence comes from thin oxide layers that act as diffraction gratings, creating peacock-like color play."),

    ("Native Gold in Quartz Vein", "Grass Valley, California, USA",
     "Au", "Cubic", "2.5–3", "19.3", "Metallic", "Opaque",
     (280, 4200),
     "Grass Valley was the richest gold-mining district in California — and some of its finest specimens show wire or arborescent gold still locked in milky quartz veins, exactly as miners encountered it. Gold crystallizes from hydrothermal fluids as they cool; these specimens are frozen at that moment of precipitation."),

    ("Stibnite Crystal Group", "Xikuangshan, Hunan, China",
     "Sb₂S₃", "Orthorhombic", "2", "4.63", "Metallic", "Opaque",
     (65, 550),
     "Stibnite's needle-like crystals, silver-black and mirror-bright, cluster in formations that look like abstract metallic sculptures — or, in the imagination of Japanese sword-makers who once prized it, the quintessence of a blade. Hunan's Xikuangshan district is the world's largest antimony producer and its specimens are legendary."),

    ("Crocoite Crystal Cluster", "Adelaide Mine, Dundas, Tasmania",
     "PbCrO₄", "Monoclinic", "2.5–3", "6.00", "Adamantine to vitreous", "Translucent",
     (285, 2800),
     "No mineral is more aggressively orange than crocoite — lead chromate in crystalline form. Tasmania's Adelaide Mine is the only source of world-class material: long prismatic crystals in intense orange-red, matte on surfaces, bright within. The toxicity of both lead and chromium makes these specimens beautiful and sobering in equal measure."),

    ("Vanadinite on Barite", "Mibladen, Khénifra, Morocco",
     "Pb₅(VO₄)₃Cl", "Hexagonal", "2.5–3", "6.88", "Adamantine to resinous", "Translucent to opaque",
     (38, 245),
     "Vanadinite's intense red-orange hexagonal prisms on white barite matrix are one of mineralogy's most photogenic combinations. This Moroccan locality is the world standard for the species. The color comes from vanadium — the same element used to strengthen steel — here precipitated from oxidizing lead ore deposits."),

    ("Wulfenite Crystal Plate", "Red Cloud Mine, La Paz County, Arizona",
     "PbMoO₄", "Tetragonal", "3", "6.82", "Adamantine to resinous", "Transparent to translucent",
     (145, 1800),
     "Red Cloud wulfenite is the benchmark — tabular orange crystals so thin they seem pressed, arranged in plates that catch light from every angle. Arizona law has since restricted collecting. These specimens from peak production years (1970s–90s) represent a geological moment that cannot be repeated."),

    ("Rhodochrosite Stalactite Slice", "Capillitas Mine, Catamarca, Argentina",
     "MnCO₃", "Trigonal", "3.5–4", "3.70", "Vitreous", "Transparent to translucent",
     (65, 580),
     "Argentina's Capillitas mine produces stalactitic rhodochrosite — pink manganese carbonate deposited in layers by ancient hydrothermal solutions. Sliced and polished, the cross-section reveals concentric rose-and-cream banding that looks like a geological dessert. The Incas called rhodochrosite 'Inca Rose.'"),

    ("Selenite Gypsum Wand", "Naica Mine, Chihuahua, Mexico",
     "CaSO₄·2H₂O", "Monoclinic", "2", "2.32", "Vitreous to pearly", "Transparent",
     (18, 85),
     "The Cave of Crystals under Naica contains selenite beams up to 12 meters long — the largest natural crystals on Earth. These collector-size wands from the same deposit are crystallographically identical: pure, colorless, with perfect cleavage and a translucency that turns light creamy white. They grew over 500,000 years in 50°C saline groundwater."),

    ("Desert Rose Barite", "Sahara Desert, Algeria",
     "BaSO₄", "Orthorhombic", "3–3.5", "4.48", "Vitreous to resinous", "Opaque",
     (18, 65),
     "Desert roses form when barite crystalizes around sand grains in arid conditions — typically in dry lakebeds or evaporitic flats. The 'petals' are barite crystals grown in rosette clusters, each blade incorporating incorporated sand that gives them their sandy surface. They form over thousands of years, patient sculptures of the desert."),

    ("Celestite Geode", "Sakoany, Madagascar",
     "SrSO₄", "Orthorhombic", "3–3.5", "3.97", "Vitreous", "Transparent to translucent",
     (45, 320),
     "Madagascar's Sakoany district is the world's top source for celestite — strontium sulfate in pale sky-blue crystals that earned the mineral its name ('sky stone' in Latin). Geodes here can reach 50 cm diameter, lined with tabular crystals that shimmer with a calming blue impossible to replicate in glass."),

    ("Calcite Dog-Tooth Cluster", "Elmwood Mine, Tennessee, USA",
     "CaCO₃", "Trigonal", "3", "2.71", "Vitreous", "Transparent",
     (28, 195),
     "Tennessee's Elmwood zinc mine produced calcite specimens of museum quality — scalenohedral 'dogtooth' crystals several centimeters long, water-clear, often with galena or sphalerite partners. The mine closed but these specimens endure as benchmarks. Calcite cleaves in three directions and shows strong double refraction."),

    ("Iceland Spar — Optical Calcite", "Helgustaðir, Iceland",
     "CaCO₃", "Trigonal", "3", "2.71", "Vitreous", "Transparent",
     (18, 95),
     "Iceland spar — transparent, colorless calcite — famously shows double refraction: place a crystal over text and see two images. It was used in Viking navigation (the 'sunstone' of sagas) and later in optical instruments before glass could be made pure enough. The Helgustaðir deposit in Iceland is the historical source."),

    ("Apophyllite Crystal Cluster on Stilbite", "Jalgaon, Maharashtra, India",
     "KCa₄Si₈O₂₀(F,OH)·8H₂O", "Tetragonal", "4.5–5", "2.35", "Pearly to vitreous", "Transparent to translucent",
     (28, 185),
     "Indian trap basalts host a staggering variety of zeolite minerals. Apophyllite forms cubic or pyramidal crystals, often colorless or pale green, perched on salmon-pink stilbite fans. The combination is one of mineralogy's most arresting — ice-clear prisms on the warmth of stilbite."),

    ("Rhodonite Specimen", "Morro da Mina, Minas Gerais, Brazil",
     "MnSiO₃", "Triclinic", "5.5–6.5", "3.57–3.76", "Vitreous to pearly", "Opaque to translucent",
     (22, 145),
     "Rhodonite's rose-pink color (manganese) often plays against black manganese oxide dendrites in a pattern that looks like antique lacquerwork. Minas Gerais material is particularly valued for rich pink and striking contrast. The mineral was named from the Greek for 'rose,' a straightforward honor for once."),

    ("Dioptase Crystal Cluster", "Tsumeb, Namibia",
     "CuSiO₂(OH)₂", "Trigonal", "5", "3.28–3.35", "Vitreous", "Transparent to translucent",
     (165, 1400),
     "When dioptase was first brought to Europe in 1785, it was initially mistaken for emerald — the color is that intense. Namibia's Tsumeb mine is the world's greatest dioptase source, producing emerald-green crystals on white calcite that remain unsurpassed. The copper-silicate structure produces a color no other mineral quite replicates."),

    ("Zircon Crystal in Pegmatite", "Ratnapura District, Sri Lanka",
     "ZrSiO₄", "Tetragonal", "7.5", "4.60–4.70", "Adamantine", "Transparent",
     (85, 680),
     "Zircon is Earth's oldest mineral — crystals from Western Australia have been dated at 4.4 billion years, older than any rock formation. Sri Lankan zircons are typically 540–600 million years old and are prized for their adamantine luster and dispersion that rivals diamond. They contain the earliest clock in Earth's geological record."),

    ("Pyrrhotite Crystal", "Dalnegorsk, Primorsky Krai, Russia",
     "Fe₁₋ₓS", "Monoclinic", "3.5–4.5", "4.58–4.65", "Metallic", "Opaque",
     (35, 195),
     "Pyrrhotite — iron sulfide with a magnetic personality — forms bronze-coloured hexagonal plates at Dalnegorsk, often accompanied by sphalerite and galena. It is slightly magnetic due to a non-stoichiometric iron lattice, which means some specimens will move a compass needle. A mineral with an invisible force."),

    ("Realgar Crystal on Orpiment", "Jiepaiyu Mine, Hunan, China",
     "As₄S₄", "Monoclinic", "1.5–2", "3.56", "Resinous", "Transparent to translucent",
     (55, 380),
     "Realgar's scarlet-orange crystals on yellow orpiment creates a composition that Renaissance painters literally ground up for pigment — 'King's Yellow' and 'Realgar Red.' Both are arsenic sulfides, so these specimens are handled with care and not displayed in sunlight. Orpiment converts to arsenolite in UV; the colors fade. Keep them dark."),

    ("Wollastonite Spray", "Crestmore Quarry, Riverside County, California",
     "CaSiO₃", "Triclinic", "4.5–5", "2.86–3.09", "Vitreous to silky", "Translucent",
     (22, 95),
     "Wollastonite forms in contact metamorphic zones where limestone meets igneous intrusions — limestone calcium reacting with silica-rich fluids at high temperature. California's Crestmore quarry produced exceptionally fine sprays of fibrous white crystals that capture light like frosted glass."),

    ("Staurolite Twin — Fairy Stone", "Patrick County, Virginia, USA",
     "Fe₂Al₉O₆(SiO₄)₄(O,OH)₂", "Monoclinic", "7–7.5", "3.74–3.83", "Resinous to vitreous", "Opaque",
     (18, 65),
     "Staurolite crystals famously twin at 60° or 90° angles, creating natural crosses. Virginia fairy stones were worn as charms long before Europeans arrived — Cherokee legend held they formed from the tears of forest fairies mourning a tragedy. The 'tears crystallized as they hit the ground' is, geologically, not that far from the truth of how contact metamorphism works."),

    ("Prehnite Stalactite", "Jeffrey Mine, Asbestos, Quebec, Canada",
     "Ca₂Al(Si₃Al)O₁₀(OH)₂", "Orthorhombic", "6–6.5", "2.80–2.95", "Vitreous to waxy", "Translucent",
     (28, 175),
     "Prehnite's pale pistachio green is among mineralogy's most soothing colors. Quebec's Jeffrey Mine (now called the LAB Chrysotile mine) produced spherical and stalactitic prehnite of remarkable quality. The mineral was the first named after a person — Dutch Colonel Hendrik von Prehn, who brought specimens from South Africa in 1774."),

    ("Kunzite Crystal", "Pala, California, USA",
     "LiAlSi₂O₆", "Monoclinic", "6.5–7", "3.15–3.21", "Vitreous", "Transparent",
     (165, 2200),
     "Kunzite — pink spodumene — was first described from Pala, California in 1902 and named after mineralogist George Kunz, Tiffany's legendary gem buyer. The lilac-pink to rose color comes from trace manganese. Kunzite is strongly pleochroic: rotate it and the color shifts from vivid pink to near-colorless. It is also sensitive to heat and prolonged light exposure — a delicate beauty."),

    ("Hiddenite Crystal", "Stony Point, Alexander County, North Carolina, USA",
     "LiAlSi₂O₆", "Monoclinic", "6.5–7", "3.15–3.21", "Vitreous", "Transparent",
     (220, 3800),
     "Green spodumene — hiddenite — is arguably the rarest gem-quality mineral found in the United States. Named for W.E. Hidden who first found it in North Carolina in 1879, its emerald-green color comes from chromium and vanadium. Large gem-quality crystals are essentially uncollectable; even small bright specimens are significant finds."),

    ("Benitoite Crystal on Natrolite", "San Benito County, California, USA",
     "BaTiSi₃O₉", "Hexagonal (ditrigonal dipyramidal)", "6–6.5", "3.67", "Vitreous", "Transparent",
     (580, 8500),
     "California's state gemstone is found in one commercial location on Earth: the Benitoite Gem Mine in San Benito County. The deep sapphire-blue crystals sit on snow-white natrolite matrices in a combination so striking it feels staged. Under short-wave UV they fluoresce an electric blue that beggers description. Active collecting ended; existing specimens are a finite resource."),

    ("Tanzanite Crystal — Unheated", "Merelani Hills, Arusha, Tanzania",
     "Ca₂Al₃(SiO₄)₃(OH)", "Orthorhombic", "6.5", "3.35", "Vitreous", "Transparent",
     (420, 6500),
     "Tanzanite — blue-purple zoisite — was discovered in 1967, reportedly by a Maasai herder who noticed blue stones scattered by a lightning-caused brush fire. The heat had converted brown trichroic zoisite into the blue-purple we prize. An unheated natural crystal shows the raw trichroism: blue, purple, and burgundy shifting with viewing direction."),

    ("Alexandrite Crystal — Color-Change", "Malysheva, Ural Mountains, Russia",
     "BeAl₂O₄", "Orthorhombic", "8.5", "3.73", "Vitreous", "Transparent",
     (1200, 28000),
     "The original alexandrite — discovered in the Ural Mountains on Tsar Alexander II's birthday in 1834 — changes from emerald green in daylight to raspberry red in incandescent light. This is chromium absorbing specific wavelengths differently under different light sources. Uralian material is rarer than diamonds; a fine crystal is one of mineralogy's supreme achievements."),

    ("Painite Crystal", "Mogok, Mandalay Region, Myanmar",
     "CaZrBAl₉O₁₈", "Hexagonal", "8", "4.01", "Vitreous", "Transparent",
     (3500, 45000),
     "For decades, painite held the record as Earth's rarest mineral — only two specimens were known to science until 2001. Mogok's alluvial deposits then yielded a few hundred crystals, but fine gem-quality pieces remain extraordinary. The orange-red to brownish-red color comes from iron and chromium. This is mineralogy's equivalent of finding a new species of large mammal."),

    ("Red Beryl Crystal", "Wah Wah Mountains, Beaver County, Utah, USA",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.84–2.91", "Vitreous", "Transparent",
     (2800, 38000),
     "Red beryl — bixbite — forms in a single deposit: Utah's Wah Wah Mountains, where rhyolitic volcanism created exactly the right chemical conditions for manganese-bearing beryl. It is estimated to be 1,000 times rarer than emerald. Gem-quality crystals over 2 carats are nearly nonexistent. A small, clean crystal is a mineralogical unicorn."),

    ("Euclase Crystal", "Gachala, Cundinamarca, Colombia",
     "BeAlSiO₄(OH)", "Monoclinic", "7.5", "3.10", "Vitreous", "Transparent",
     (380, 4200),
     "Euclase — named for its perfect cleavage (Greek: 'eu' + 'klasis') — is a beryllium-aluminum silicate of extraordinary rarity. Colombian material from emerald-producing regions shows pale blue to blue-green color. Because of its perfect cleavage it rarely survives gemcutting intact, making crystals more valuable than faceted stones."),

    ("Fluorapatite Crystal", "Cerro de Mercado, Durango, Mexico",
     "Ca₅(PO₄)₃F", "Hexagonal", "5", "3.14–3.21", "Vitreous to resinous", "Transparent to translucent",
     (22, 145),
     "Apatite is the mineral of bones and teeth — literally: hydroxyapatite makes your skeleton. The gem-quality fluorapatite from Mexico's Cerro de Mercado (which translates, beautifully, as Hill of the Market) shows rich blue-green colors and well-formed hexagonal prisms that belie its position in the phosphate group."),

    ("Clinozoisite Crystal", "Knappenwand, Untersulzbachtal, Austria",
     "Ca₂Al₃(SiO₄)₃(OH)", "Monoclinic", "6.5", "3.21–3.38", "Vitreous", "Transparent",
     (45, 320),
     "Alpine clinozoisite from classic Austrian localities shows olive-green to yellowish-green crystals of exceptional transparency and form. The mineral is an epidote-group aluminum calcium silicate that forms in metamorphic terrains. Austrian specimens are among the reference standards in any mineral collection."),

    ("Manganite Crystal", "Ilfeld, Harz Mountains, Germany",
     "MnO(OH)", "Monoclinic", "4", "4.29–4.34", "Submetallic to adamantine", "Opaque",
     (28, 165),
     "Manganite — black, striated, and metallic — forms in low-temperature hydrothermal veins and is the primary ore of manganese. The Ilfeld locality in Germany's Harz Mountains produced reference-quality prismatic crystals in the 19th century. These specimens helped define the species; some remain in museum collections that are the envy of science."),

    ("Native Silver Wires", "Kongsberg, Numedal, Norway",
     "Ag", "Cubic", "2.5–3", "10.5", "Metallic", "Opaque",
     (280, 3500),
     "Kongsberg Silver Mine, active from 1623 to 1957, produced native silver in forms unmatched anywhere: wire silver twisted into delicate knots, sheet silver, and arborescent silver 'trees' weighing hundreds of kilograms. A Kongsberg wire silver specimen is a piece of Scandinavian mining history — and one of the most photogenic objects in mineralogy."),

    ("Native Copper Arborescent", "Keweenaw Peninsula, Michigan, USA",
     "Cu", "Cubic", "2.5–3", "8.96", "Metallic", "Opaque",
     (65, 580),
     "Michigan's Keweenaw Peninsula contains the world's largest deposit of native copper — pure copper metal, not ore, occurring in basalt amygdales and conglomerate beds. It was mined by Indigenous peoples for thousands of years before European contact. Arborescent ('tree-like') specimens show copper's natural tendency to branch as it grows from solution."),

    ("Hematite Rose", "Elba, Tuscany, Italy",
     "Fe₂O₃", "Trigonal", "5–6", "5.26", "Metallic to splendent", "Opaque",
     (28, 175),
     "Elba produces hematite in a spectacular form: 'iron roses' — tabular crystals arranged in rosette clusters that look, unmistakably, like metallic flowers. Hematite is iron oxide — rust, essentially — but crystallized with geological patience into geometric perfection. Iron Island (Elba's Etruscan name means iron) has exported these since antiquity."),

    ("Ilvaite Crystal", "Serifos, Cyclades, Greece",
     "CaFe₂²⁺Fe³⁺(Si₂O₇)O(OH)", "Orthorhombic", "5.5–6", "3.99–4.05", "Submetallic", "Opaque",
     (35, 245),
     "Named for Ilva (ancient Elba), ilvaite occurs in contact metamorphic skarns. The black prismatic crystals from Serifos are among the finest in the world, associated with epidote and calcite in combinations that show mineralogy's talent for chromatic contrast. The Greek island setting adds a mythological resonance."),

    ("Kyanite Crystal", "Barra do Salinas, Minas Gerais, Brazil",
     "Al₂SiO₅", "Triclinic", "4.5–7 (directional)", "3.53–3.67", "Vitreous to pearly", "Transparent to translucent",
     (22, 155),
     "Kyanite's defining property is its anisotropic hardness: 4.5 across the bladed crystal, 6.5–7 along it. A single crystal can scratch one way and be scratched from the other. The blue color comes from iron and titanium. Brazilian material — often sapphire-blue, sometimes teal — is among the most gem-like."),

    ("Sillimanite Fibrous", "Brandywine Summit, Delaware, USA",
     "Al₂SiO₅", "Orthorhombic", "7–7.5", "3.23", "Vitreous to silky", "Translucent",
     (18, 85),
     "Sillimanite is one of three aluminum silicate polymorphs (kyanite and andalusite being the others), each stable at different temperature-pressure conditions. Fibrous sillimanite — 'fibrolite' — indicates high-grade metamorphism. Delaware's state mineral, it was first described from these very outcrops in 1824."),
]

GEMSTONES = [
    ("Diamond Crystal — Rough Octahedron", "Jwaneng Mine, Botswana",
     "C", "Cubic", "10", "3.51", "Adamantine", "Transparent",
     (380, 4500),
     "A diamond octahedron is carbon atoms arranged in the most efficient three-dimensional lattice possible. This geometry emerged over a billion years ago, 150 kilometers underground, under pressures that would crush a submarine. It was then blasted to the surface in a kimberlite eruption. The hardest natural substance on Earth began as something ordinary: carbon."),

    ("Ruby Crystal in Matrix", "Mogok Valley, Mandalay Region, Myanmar",
     "Al₂O₃", "Trigonal", "9", "4.00", "Vitreous to adamantine", "Transparent",
     (580, 18500),
     "Mogok rubies are the world's standard — the 'pigeon's blood' color that all other rubies are compared against. This comes from chromium replacing aluminum in corundum's crystal lattice, combined with strong fluorescence that makes Mogok stones glow under sunlight. These crystals grew in marble limestone under conditions so specific that the Mogok Stone Tract remains the world's premier ruby source after centuries of mining."),

    ("Sapphire Crystal — Cornflower Blue", "Ratnapura, Sabaragamuwa Province, Sri Lanka",
     "Al₂O₃", "Trigonal", "9", "4.00", "Vitreous to adamantine", "Transparent",
     (420, 9800),
     "Sri Lankan sapphires have been prized since the Silk Road era — their distinctive cornflower blue, softer and more luminous than Kashmir or Montana material, made Ceylon the default source for royal jewelry for centuries. The color comes from iron and titanium impurities in corundum. A natural, unheated crystal of this quality is rarer than the faceted gem."),

    ("Padparadscha Sapphire Crystal", "Ilakaka, Ihorombe Region, Madagascar",
     "Al₂O₃", "Trigonal", "9", "4.00", "Vitreous to adamantine", "Transparent",
     (1200, 22000),
     "The most sought-after sapphire color has no proper English name. 'Padparadscha' is Sinhalese for lotus blossom — that particular blend of pink and orange that sits at the exact intersection of sunrise and flower. The color comes from trace iron and chromium. Madagascar's Ilakaka deposits yield fine material, though the definition of 'true' padparadscha remains contentious among gemmologists."),

    ("Star Sapphire — 6-Ray", "Mogok, Myanmar",
     "Al₂O₃", "Trigonal", "9", "4.00", "Silky asterism", "Translucent",
     (280, 4800),
     "The asterism in a star sapphire is caused by needle-like inclusions of rutile — titanium dioxide — arranged in three intersecting sets, following the hexagonal symmetry of corundum. When cut as a cabochon, these needles diffract light into a six-rayed star that moves as you tilt the stone. Mogok produces the finest: velvety blue with a sharp, centered star."),

    ("Cat's Eye Chrysoberyl", "Ratnapura, Sri Lanka",
     "BeAl₂O₄", "Orthorhombic", "8.5", "3.75", "Vitreous", "Translucent",
     (580, 9500),
     "The chatoyancy in cat's eye chrysoberyl — a single bright line that moves with light, exactly replicating a feline iris — comes from parallel channels or inclusions of actinolite aligned during crystal growth. In the gem trade, 'cat's eye' alone always means chrysoberyl; other cat's eyes require a qualifying mineral name. Sri Lanka's production is the world benchmark."),

    ("Star Ruby", "Luc Yen, Yen Bai, Vietnam",
     "Al₂O₃", "Trigonal", "9", "4.00", "Silky asterism", "Translucent",
     (380, 6500),
     "A six-rayed star on red corundum — the finest rubies showing asterism are among the rarest gems. Vietnam's Luc Yen district produces rubies with exceptional color, often a pure pigeon's blood without the pink or orange tones that afflict Thai or Indian material. The star is caused by rutile silk oriented by the trigonal symmetry of corundum."),

    ("Black Opal", "Lightning Ridge, New South Wales, Australia",
     "SiO₂·nH₂O", "Amorphous", "5.5–6.5", "2.15", "Vitreous to resinous", "Opaque with play-of-color",
     (580, 18000),
     "Lightning Ridge black opal is the most valuable gem variety on a per-carat basis that the Earth produces routinely. The 'black' refers to the dark body tone, which provides the backdrop against which play-of-color — caused by diffraction from stacked silica spheres of uniform size — blazes most intensely. Each opal's pattern is unique, a frozen snapshot of spheres arranged by sedimentation 100 million years ago."),

    ("White Opal — Harlequin", "Coober Pedy, South Australia",
     "SiO₂·nH₂O", "Amorphous", "5.5–6.5", "2.10", "Vitreous to resinous", "Translucent with play-of-color",
     (185, 3200),
     "Harlequin pattern — large, mosaic-like patches of color in a geometric arrangement — is the rarest and most valued opal pattern. Coober Pedy, discovered in 1915 by a teenage boy on a water prospecting trip, remains the world's largest opal mining area. The town is largely underground, residents having extended their mines into habitable homes to escape the 50°C surface temperatures."),

    ("Fire Opal Crystal", "Querétaro, Mexico",
     "SiO₂·nH₂O", "Amorphous", "5.5–6.5", "2.10", "Vitreous to resinous", "Transparent to translucent",
     (95, 1400),
     "Mexican fire opal is the only opal prized primarily for its body color rather than play-of-color — an intense orange-red that no other gem replicates. It forms in volcanic rhyolites, where silica-rich solutions cool and deposit opal in gas cavities. Transparent fire opal can be faceted; the resulting gems look like drops of flame."),

    ("Topaz — Precious Pink (Unheated)", "Katlang, Mardan, Pakistan",
     "Al₂SiO₄(F,OH)₂", "Orthorhombic", "8", "3.49–3.57", "Vitreous", "Transparent",
     (280, 4800),
     "Natural pink topaz is extraordinarily rare — most pink topaz on the market is heat-treated or irradiated colorless topaz. Pakistan's Katlang produces genuine pink crystals where chromium substitutes for aluminum. The color can be pastel pink or deep rose, and it is stable under light and heat, unlike many artificially colored gems."),

    ("Tsavorite Garnet Crystal", "Komolo, Arusha, Tanzania",
     "Ca₃Al₂(SiO₄)₃", "Cubic", "7–7.5", "3.57–3.73", "Vitreous", "Transparent",
     (380, 7200),
     "Tsavorite's deep green rivals emerald but with greater hardness and clarity — it rarely needs treatment, unlike most emeralds. The color comes from vanadium and chromium in grossular garnet. Found only in the East African metamorphic belt, new deposits are sought eagerly by miners on both sides of the Kenya-Tanzania border. Fine crystals in matrix are rarer than the faceted gems."),

    ("Color-Change Garnet", "Bekily, Anosy Region, Madagascar",
     "Py₃₅-₄₅Sp₁₅Gr₄₀-₅₀", "Cubic", "7.25", "3.75", "Vitreous", "Transparent",
     (420, 6500),
     "Madagascar's color-change garnets perform a trick more dramatic than alexandrite: green to blue-green in daylight, red to purple in incandescent light. The mechanism is chromium absorption, identical to alexandrite's, but in a garnet matrix that intensifies the saturation. This discovery (1990s) upended the gem market's assumptions about garnet's color range."),

    ("Spinel Crystal — Red", "Mogok Valley, Myanmar",
     "MgAl₂O₄", "Cubic", "8", "3.58", "Vitreous", "Transparent",
     (380, 8500),
     "Some of history's most famous 'rubies' — the Black Prince's Ruby in the British Crown Jewels, the Timur Ruby — are actually spinels. Spinel and ruby occur together in Mogok and are nearly identical in color. Spinel is now rightly valued in its own right: it comes in vivid reds, oranges, pinks, blues, and purples, with exceptional brilliance."),

    ("Spinel Crystal — Cobalt Blue", "Luc Yen, Vietnam",
     "MgAl₂O₄", "Cubic", "8", "3.58", "Vitreous", "Transparent",
     (580, 9800),
     "Cobalt-blue spinel is the rarest color variety — the vivid blue comes from cobalt substituting for magnesium. Vietnam's Luc Yen produces specimens of electrifying blue, small but intense. The color is essentially the same mechanism as cobalt glass: cobalt's electronic structure absorbs red and green wavelengths, reflecting only blue."),

    ("Demantoid Garnet — Horsetail Inclusion", "Val Malenco, Sondrio, Italy",
     "Ca₃Fe₂(SiO₄)₃", "Cubic", "6.5–7", "3.84", "Adamantine", "Transparent",
     (850, 12000),
     "The most prized andradite garnet has the highest dispersion of any natural gem — more 'fire' than diamond. The legendary Russian Ural deposits are mostly exhausted; Italian Val Malenco now produces the finest material. The 'horsetail' inclusion — chrysotile asbestos fibers radiating from a chromite crystal — is considered a positive identifier of Russian origin and paradoxically increases value."),

    ("Paraíba Tourmaline — Neon Blue", "Batalha, Rio Grande do Norte, Brazil",
     "Na(Cu,Mn)(Al,Fe)₆(BO₃)₃Si₆O₁₈(OH)₄", "Trigonal", "7–7.5", "3.06", "Vitreous", "Transparent",
     (2800, 65000),
     "In 1987, Heitor Dimas Barbosa started digging a hillside in Paraíba state, Brazil, convinced something extraordinary lay within. He was right. In 1989 the first neon-blue tourmalines emerged — copper-bearing, with a color so vivid it appeared internally lit. Nothing like it had been seen. A Paraíba tourmaline of fine quality per carat now rivals the finest emeralds and rubies."),

    ("Sphene Crystal — Titanite", "Binntal, Valais, Switzerland",
     "CaTiSiO₅", "Monoclinic", "5–5.5", "3.48–3.60", "Adamantine to resinous", "Transparent",
     (165, 2800),
     "Titanite (sphene) has a dispersion exceeding diamond — more 'fire' than any other common transparent gem — combined with a yellow-green color that shifts with viewing angle. Swiss Alpine specimens are the world benchmark: sharp wedge-shaped crystals on calcite matrices from classic localities. The name sphene comes from the Greek for 'wedge.'"),

    ("Kornerupine Crystal", "Mogok, Myanmar",
     "□(Mg,Fe)₄Al₆(Si,Al,B)₅O₂₁(OH)", "Orthorhombic", "6.5", "3.28–3.35", "Vitreous", "Transparent",
     (380, 4800),
     "Kornerupine is a collector's gem — rarely seen in jewelry, spectacular in a collection. The brown-green color changes to reddish in incandescent light. Mogok produces the finest material. The mineral was named after Danish geologist Andreas Nikolaus Kornerup in 1884. Fine facetable crystals are genuinely rare."),

    ("Grandidierite Crystal", "Tranomaro, Anosy Region, Madagascar",
     "(Mg,Fe)Al₃(BSiO₉)", "Orthorhombic", "7–7.5", "2.98–3.00", "Vitreous", "Transparent",
     (580, 8500),
     "Grandidierite was described in 1902 from Madagascar and for decades was represented in mineral collections by a handful of specimens from that original locality. Its teal-blue color comes from iron; it is strongly trichroic, showing blue-green, colorless, and dark blue-green from different directions. Facetable quality remained elusive until a new Malagasy find in 2014."),

    ("Jeremejevite Crystal", "Swakopmund, Erongo Region, Namibia",
     "Al₆B₅O₁₅(F,OH)₃", "Hexagonal", "6.5–7.5", "3.28", "Vitreous", "Transparent",
     (480, 7500),
     "For most of the 20th century, jeremejevite was represented in world collections by fewer than a dozen crystals from Siberia. Then Namibian material emerged — pale blue crystals of exceptional clarity. Named after Russian mineralogist Pavel Jeremejev, it produces a pale aquamarine to colorless gem. Its rarity puts it alongside painite in conversations about the most inaccessible gems."),

    ("Amber with Insect Inclusion", "Kaliningrad Oblast, Russia",
     "Fossil resin (C₁₀H₁₆O)", "Amorphous", "2–2.5", "1.08", "Resinous", "Transparent to translucent",
     (85, 2800),
     "Baltic amber — Eocene tree resin, 44 million years old — is history's most productive source of fossil inclusions. When an insect, spider, or plant fragment became trapped, it could be preserved in atomic detail longer than any other fossilization mode. This specimen contains a complete insect visible under a loupe. Jurassic Park was not entirely fiction."),

    ("Burmese Amber with Lizard Inclusion", "Hukawng Valley, Kachin State, Myanmar",
     "Fossil resin", "Amorphous", "2–2.5", "1.05–1.10", "Resinous", "Transparent",
     (580, 18500),
     "Burmese amber at 99 million years old contains the most spectacular fossil record of Cretaceous forest life — including the first feathered dinosaur tail in amber, frogs, lizards, and intact flowers. A lizard inclusion of this age puts you within 35 million years of T. rex. These specimens are actively studied; owning one is participating in ongoing paleontology."),

    ("Jet Carved Specimen", "Whitby, North Yorkshire, England",
     "Lignite (fossil wood)", "Amorphous", "3.5–4", "1.20–1.35", "Waxy to resinous", "Opaque",
     (55, 380),
     "Whitby jet — compressed fossil wood from 180-million-year-old monkey puzzle trees — became famous during Queen Victoria's mourning period. Victorian jewelers carved it into elaborate pieces; Whitby's jet workshops were legendary. The deep black, lightweight warmth, and workability of jet make it unique among organic gems. A carved piece is Victorian history in your hand."),

    ("Coral Specimen — Red", "Sciacca, Sicily, Mediterranean Sea",
     "CaCO₃ (biological)", "Trigonal (microcrystalline)", "3.5", "2.65", "Waxy to dull", "Opaque",
     (85, 680),
     "Noble coral — Corallium rubrum — is the red skeleton of a colonial marine animal, deposited as microcrystalline calcite. Mediterranean red coral has been harvested since antiquity; Phoenicians traded it along ancient routes. Today it is heavily regulated; this specimen is from a documented pre-regulation collection. The color ranges from pale pink to 'oxblood' red, the deepest shades most prized."),

    ("Rough Emerald Crystal — Gem Grade", "Coscuez Mine, Boyacá, Colombia",
     "Be₃Al₂Si₆O₁₈", "Hexagonal", "7.5–8", "2.69–2.78", "Vitreous", "Transparent",
     (380, 9500),
     "The Coscuez mine, one of three great Colombian emerald mines alongside Muzo and Chivor, produces a distinctive bright green. Colombian emeralds form in black shale and calcite veins — a hydrothermal system unique on Earth. A gem-grade rough crystal still in matrix represents the stone before the cutter's art intervenes: the raw material of history's most coveted colored gem."),
]

FOSSILS = [
    ("Trilobite — Enrolled Phacops", "Hamar Laghdad, Erfoud, Morocco",
     "Calcite/pyritic replacement", "—", "—", "—", "—", "—",
     (28, 185),
     "Phacops enrolled into a defensive ball the moment danger threatened — 380 million years ago in a Devonian sea. This one never unrolled. The calcified eyes, composed of individual calcite lenses each oriented to minimize spherical aberration, represent an optical system that evolution independently re-discovered in modern compound eyes. The Moroccan Sahara was once a shallow tropical sea."),

    ("Trilobite — Walliserops trifurcatus (Trident)", "Foum Zguid, Morocco",
     "Calcified exoskeleton", "—", "—", "—", "—", "—",
     (285, 2800),
     "Walliserops trifurcatus is palaeontology's most improbable arthropod: a trilobite with a long, ornate trident growing from its head. The function of this structure remains debated — competition display? Prey manipulation? — but its geometric elaboration suggests evolution's willingness to experiment. Only a few hundred specimens are known. Each is a unanswered question in stone."),

    ("Ammonite — Polished Section", "Mahajanga Province, Madagascar",
     "Aragonite/calcite shell",  "—", "—", "—", "—", "—",
     (22, 145),
     "Cut and polished, an ammonite's internal chambers reveal the logarithmic spiral that mathematicians called the 'golden ratio' centuries before they understood its name. The iridescent nacreous layer — preserved aragonite from the original shell — creates colors that shift with viewing angle. These Cretaceous cephalopods died 66 million years ago; their shells are more beautiful than they could have imagined."),

    ("Ammonite — Opalized", "Lightning Ridge, New South Wales, Australia",
     "Silica (opal) replacement",  "—", "—", "—", "—", "—",
     (285, 4800),
     "When an ammonite shell dissolves and is replaced atom by atom by silica spheres of uniform size, the result is an opalized fossil — a creature's geometry wearing a gem's colors. Lightning Ridge ammonites are among the most arresting objects in palaeontology: the form of something 100 million years old, in the colors of a fire."),

    ("Fish Fossil — Green River Formation", "Kemmerer, Lincoln County, Wyoming, USA",
     "Phosphatic/calcite preservation",  "—", "—", "—", "—", "—",
     (38, 650),
     "The Green River Formation — Eocene lake beds in Wyoming, Colorado, and Utah — is one of Earth's great fossil deposits. Fish are preserved in such fine-grained varve (annual) layers that individual scales are visible under a loupe, and the stomach contents of some specimens can be identified. These Eocene fish died approximately 50 million years ago, on a calm day in a subtropical lake."),

    ("Fish Fossil — Knightia eocaena (Twin Plate)", "Green River Formation, Wyoming",
     "Phosphatic preservation",  "—", "—", "—", "—", "—",
     (18, 95),
     "Knightia is the Wyoming state fossil and the most commonly collected fossil vertebrate in the world — but a twin plate, two fish preserved together, suggests a specific depositional event: a temperature fluctuation or algal bloom that killed multiple fish simultaneously. Their exact positions at death were preserved by the rapid burial in carbonate sediment."),

    ("Mosasaur Tooth on Matrix", "Khouribga Province, Morocco",
     "Phosphatic replacement",  "—", "—", "—", "—", "—",
     (45, 380),
     "Mosasaurs ruled Cretaceous seas for 23 million years — massive predatory lizards (not dinosaurs) up to 17 meters long, with double-hinged jaws that could swallow large prey whole. This tooth, still embedded in jaw matrix, is from the latest Cretaceous (~70 million years ago). These animals and the non-avian dinosaurs went extinct simultaneously in the end-Cretaceous mass extinction."),

    ("Megalodon Tooth Replica — Detailed", "South Carolina, USA (cast from original)",
     "Fossil enamel (replica)",  "—", "—", "—", "—", "—",
     (28, 95),
     "Carcharocles megalodon — possibly the largest predatory shark to have ever lived — reached perhaps 18 meters and went extinct approximately 3.6 million years ago (not still lurking in ocean trenches, as popularized fiction suggests). These precise casts of actual 7-centimeter teeth from South Carolina show the serrations clearly. The original sharks are gone; the geometry of their teeth endures."),

    ("Dinosaur Tooth — Spinosaurus", "Kem Kem Formation, Morocco",
     "Phosphatic replacement",  "—", "—", "—", "—", "—",
     (85, 680),
     "Spinosaurus aegyptiacus — 95–100 million years old — may have been the largest predatory dinosaur that ever lived, longer than T. rex and adapted for catching fish with conical, unserrated teeth more like a crocodile's. This tooth from Morocco's Kem Kem Formation is from a specimen of that predator, recovered from sediments that were once a vast river delta."),

    ("Dinosaur Tooth — Carcharodontosaurus", "Kem Kem Formation, Morocco",
     "Phosphatic replacement",  "—", "—", "—", "—", "—",
     (95, 750),
     "Carcharodontosaurus — 'shark-toothed lizard' — was one of the largest theropod dinosaurs, rivaling T. rex in body size. Its blade-like serrated teeth, up to 8 centimeters long, could slice through flesh with a lateral shaking motion. This specimen from Morocco's Late Cretaceous Kem Kem Formation is 95 million years old."),

    ("Insect in Amber — Ant Cluster", "Baltic Region, Poland/Russia",
     "Fossil resin",  "—", "—", "—", "—", "—",
     (45, 380),
     "Social insects — ants, bees, termites — evolved their complex societies in the Eocene or earlier, and Baltic amber preserves them in behavioral poses: workers, queens, males, and sometimes entire colonies trapped together. An ant preserved in amber carries all the social information of its species frozen 44 million years ago. Evolution runs on deep time."),

    ("Spider in Amber — Burma", "Hukawng Valley, Myanmar",
     "Fossil resin",  "—", "—", "—", "—", "—",
     (185, 2400),
     "Burmese amber's 99-million-year age places its inclusions squarely in the Cretaceous — contemporary with apex predator dinosaurs. Spiders from this period belong to lineages that look remarkably similar to modern relatives, a testament to the effectiveness of the spider body plan. Some Burmese amber spiders have been found in silk-wrapped prey — hunting behavior frozen at the moment of success."),

    ("Fern Fossil — Pecopteris", "Mazon Creek Formation, Illinois, USA",
     "Siderite concretion",  "—", "—", "—", "—", "—",
     (18, 65),
     "Mazon Creek concretions — iron-carbonate nodules from Carboniferous coal measures — have yielded some of the most diverse fossil flora on Earth. Crack one open and find a perfect fern frond, preserved in three dimensions, from a coal swamp 309 million years ago. This specimen predates the dinosaurs by 75 million years. Carboniferous forests built the coal we burned for the industrial revolution."),

    ("Petrified Wood — Araucarioxylon", "Petrified Forest, Arizona, USA",
     "Silica replacement of wood",  "—", "—", "—", "—", "—",
     (35, 280),
     "228-million-year-old trees from the Triassic floodplains of what would become Arizona were buried in volcanic ash, silicified over millions of years, then exposed by erosion. The original wood cells are replaced by quartz or chalcedony in precise detail — annual rings, cellular structure, and even fungal damage preserved in stone. These trees predated both mammals and birds."),

    ("Ammonite — Hildoceras bifrons", "Whitby, North Yorkshire, England",
     "Pyritic/calcite replacement",  "—", "—", "—", "—", "—",
     (38, 245),
     "Whitby's Jurassic shales have yielded ammonites since the Anglo-Saxon era — local legend turned them into petrified snakes (they lacked the heads, so locals carved them on). The pyritized Hildoceras bifrons specimens, 180 million years old, show the ribbed sutures that distinguish each ammonite genus. Yorkshire's coast is actively eroding, releasing new specimens each winter storm."),

    ("Sea Urchin — Micraster", "Chalk formation, Kent, England",
     "Calcite preservation",  "—", "—", "—", "—", "—",
     (18, 85),
     "The white chalk of southern England — the White Cliffs of Dover — was deposited between 70–100 million years ago as a thick ooze of coccolithophore shells (single-celled algae) on a warm, shallow sea floor. Within it, heart urchins like Micraster were buried and preserved in three dimensions, their test intact. British farmers once called them 'fairy loaves' and placed them on hearths for luck."),

    ("Crinoid Stem Section — Polished", "Mississippian Formation, Indiana, USA",
     "Calcite replacement",  "—", "—", "—", "—", "—",
     (18, 55),
     "Crinoids — 'sea lilies' — are filter-feeding echinoderms that have existed for 480 million years. Their multi-jointed stems, when polished in cross-section, reveal a perfectly five-fold symmetric pattern that looks like a star or flower. Entire Mississippian limestone beds are composed of little else: a living carpet of these animals covered Paleozoic sea floors to horizon."),

    ("Nautiloid — Cyrtoceras Orthocerid", "Erfoud, Morocco",
     "Calcite replacement",  "—", "—", "—", "—", "—",
     (22, 145),
     "Straight-shelled nautiloids — orthocerids — were among the apex predators of Ordovician and Silurian seas, reaching several meters in length. These Moroccan specimens, 380–420 million years old, are polished to reveal the internal septa (dividing walls) that the living animal used for buoyancy control, flooding chambers with gas or water as needed. Living nautiluses still use this mechanism."),

    ("Trace Fossil — Dinosaur Footprint Cast", "Connecticut Valley, Massachusetts, USA",
     "Cast of original impression",  "—", "—", "—", "—", "—",
     (55, 380),
     "The Connecticut Valley contains one of North America's richest trace fossil records — Triassic dinosaurs walking across mudflats that dried and lithified. Trace fossils record behavior, not bodies: the weight distribution of an animal in mid-stride, its pace length, whether it was running. This three-toed track was made 200 million years ago by an early theropod whose skeleton has never been found."),

    ("Coprolite — Predator Specimen", "Judith River Formation, Montana, USA",
     "Phosphatic replacement",  "—", "—", "—", "—", "—",
     (28, 165),
     "Coprolites are fossils of feces, and they are paleontology's most underappreciated resource. Analysis of what was consumed (bone fragments, scales, feathers, plant material) tells us more about ancient diets than bones alone. Montana's Judith River Formation (Cretaceous) yields coprolites from large theropods, identifiable by crushed bone content, size, and context."),

    ("Brachiopod Cluster — Spirifer", "Devonian limestone, New York, USA",
     "Calcite replacement",  "—", "—", "—", "—", "—",
     (18, 65),
     "Brachiopods look superficially like clams but are unrelated — a classic example of convergent evolution. They dominated seafloors for 300 million years. Devonian Spirifer brachiopods from New York state show the distinctive 'wings' and delicate ribbing of a filter-feeding animal that lived in dense communities on warm, shallow seafloors. The Devonian mass extinction largely ended their dominance."),

    ("Eurypterid — Sea Scorpion", "Bertie Formation, New York, USA",
     "Chitin/cuticle replacement",  "—", "—", "—", "—", "—",
     (185, 2200),
     "Eurypterids — 'sea scorpions' — were the apex predators of Silurian seas and freshwaters, some reaching 2.5 meters. This specimen, approximately 430 million years old, preserves the articulated appendages and paddle-like swimming legs of an arthropod lineage that ruled for 200 million years before dying in the Permian extinction. Their nearest living relatives are horseshoe crabs."),

    ("Horseshoe Crab — Limulus", "Green River Formation, Wyoming, USA",
     "Organic/mineral replacement",  "—", "—", "—", "—", "—",
     (165, 1800),
     "The horseshoe crab lineage has changed so little in 450 million years that Limulus today is nearly identical to Silurian relatives. This Eocene specimen from the Green River Formation (~50 million years old) is a near-perfect preservation of a 'living fossil' mid-career — the animal looked essentially like this long before humans existed, and still does. Time is a patient sculptor."),

    ("Plant Fossil — Sigillaria", "Carboniferous, Saarland, Germany",
     "Coalified compression",  "—", "—", "—", "—", "—",
     (28, 185),
     "Sigillaria was a coal-swamp tree reaching 30 meters, with a bark pattern of hexagonal leaf scars that looks like a reptile's scales. The Carboniferous forests of 310 million years ago were composed of such trees alongside giant horsetails and ferns — all now extinct genera. Their compressed remains are literally the coal seams that powered the industrial revolution."),

    ("Shark Teeth — Odontaspis Cluster", "Lee Creek Mine, North Carolina, USA",
     "Phosphatic replacement",  "—", "—", "—", "—", "—",
     (22, 145),
     "Lee Creek's Miocene (5–20 million years ago) phosphate deposits are among North America's richest fossil marine vertebrate sites. The sand tiger shark Odontaspis produced multi-rooted, needle-like teeth that formed in conveyor-belt succession — sharks shed and replace thousands of teeth in a lifetime. A cluster plate shows this biological abundance fossilized."),

    ("Mammoth Molar", "North Sea Beds, Netherlands",
     "Mineralized enamel and dentine",  "—", "—", "—", "—", "—",
     (185, 2800),
     "The North Sea was dry land during the last ice age — mammoths, woolly rhinos, and early humans walked where fishing boats now drag. Sand and gravel dredging regularly recovers Pleistocene megafauna remains up to 1.8 million years old. A mammoth molar's ridged enamel plates, evolved for grinding tough grasses on frigid steppes, is still recognizable: evolution's answer to permafrost diets."),

    ("Glyptodon Osteoderms", "Buenos Aires Province, Argentina",
     "Mineralized bone",  "—", "—", "—", "—", "—",
     (55, 380),
     "Glyptodon — an armadillo the size of a Volkswagen Beetle — roamed South America until approximately 10,000 years ago. Its rigid shell was composed of thousands of interlocking osteoderms (bone plates) hexagonal in pattern, like the shell of a turtle but evolved independently in armadillo relatives. Early humans likely hunted glyptodons; some shells show evidence of having been used as shelters."),

    ("Plesiosaurian Vertebra", "Kimmeridge Clay, Dorset, England",
     "Calcite/phosphatic replacement",  "—", "—", "—", "—", "—",
     (65, 480),
     "The Jurassic coast of Dorset — a UNESCO World Heritage Site — erodes continuously, releasing marine reptile remains from Kimmeridgian clays (155 million years old). A plesiosaurian vertebra is diagnostic: the distinctive hourglass shape, with a central channel for the notochord, identifies an animal whose lineage includes the long-necked forms that inspired the Loch Ness myth."),
]

METEORITES = [
    ("Gibeon Iron Meteorite — Etched Slice", "Gibeon, Hardap Region, Namibia",
     "Fe-Ni metal (group IVA iron)", "—", "4–5", "7.8–8.2", "Metallic", "Opaque",
     (65, 580),
     "The Widmanstätten pattern — those angular geometric bands revealed by acid etching — took one million years per millimeter to form as the Gibeon parent body cooled in the vacuum of space at approximately one degree per million years. You cannot fake this. It is the slowest signature in the universe. These irons fell across 275×100 km of Namibia, an ancient strewn field from a collision long before Earth had life."),

    ("Campo del Cielo Iron Meteorite", "Chaco Province, Argentina",
     "Fe-Ni metal (group IAB iron)", "—", "4–5", "7.8–8.1", "Metallic", "Opaque",
     (28, 280),
     "Campo del Cielo — 'Field of the Sky' — fell approximately 4,500 years ago across the Gran Chaco. Indigenous peoples knew the crater field; the first European report came in 1576 from a Spanish governor who noted 'a mass of iron.' The fall produced multiple craters; the combined mass recovered exceeds 100 tonnes, making it one of the world's largest recorded meteorite fields."),

    ("Sikhote-Alin Individual — Shrapnel", "Sikhote-Alin Mountains, Primorsky Krai, Russia",
     "Fe-Ni metal (group IIAB iron)", "—", "4–5", "7.8–8.0", "Metallic", "Opaque",
     (38, 320),
     "On February 12, 1947, witnesses in the Sikhote-Alin mountains saw a fireball brighter than the sun at 10:38 AM. The iron meteorite fragmented as it decelerated, producing a shower of sharp, angular shrapnel individuals in 23 craters across 2 km². These regmaglypts — thumb-print-like depressions from atmospheric ablation — were literally sculpted by air molecules at 15 km/s."),

    ("Chondrite Meteorite — L4 Type", "Northwest Africa (NWA)",
     "Silicates, metal, sulfide (L4 chondrite)", "—", "5.5–6.5", "3.2–3.7", "Dull to metallic on cut", "Opaque",
     (22, 185),
     "Chondrites are the oldest solid matter in the solar system — 4.56 billion years old, predating Earth by 30–40 million years. Chondrules — spherical beads visible in a fresh cut — were flash-melted from nebular dust by poorly understood events in the solar nebula. The 'L' designation means low iron; the '4' means moderate metamorphism. This is literal building material from the protoplanetary disk."),

    ("Carbonaceous Chondrite — CM2", "Northwest Africa",
     "Carbonaceous silicates, organics, presolar grains", "—", "3–4", "2.2–2.9", "Dull", "Opaque",
     (85, 850),
     "Carbonaceous chondrites are the most primitive meteorites — some contain presolar grains older than the solar system itself, including nanodiamonds and silicon carbide formed in other star systems before our Sun ignited. CM2 chondrites also contain amino acids, complex organics, and water-bearing minerals. The building blocks of life arrived by meteorite: this is no longer a metaphor."),

    ("Pallasite Meteorite — Olivine in Metal", "Brahin, Gomel Region, Belarus",
     "Fe-Ni metal + olivine (Mg,Fe)₂SiO₄", "—", "varies", "varies", "Metallic + vitreous", "Opaque + translucent",
     (185, 2800),
     "Pallasites form at the core-mantle boundary of differentiated asteroids: iron-nickel metal from the core mixed with olivine crystals from the mantle at the moment of a catastrophic collision. The result — golden olivine crystals floating in a metallic matrix, backlit like stained glass — is one of the most beautiful materials in the solar system. Brahin pallasites show exceptional olivine clarity."),

    ("Lunar Meteorite — Mare Basalt", "Northwest Africa (NWA 032 type)",
     "Pyroxene, plagioclase, ilmenite (lunar basalt)", "—", "6–7", "3.0–3.4", "Vitreous to dull", "Opaque",
     (850, 12000),
     "These were once rocks on the lunar maria — the dark volcanic plains visible with the naked eye from Earth. An asteroid impact on the Moon ejected this material with enough velocity to escape lunar gravity. It traveled through space for millions of years before entering Earth's atmosphere. You can hold the Moon."),

    ("Martian Meteorite — Shergottite", "Northwest Africa (NWA 2975 type)",
     "Pyroxene, maskelynite (shocked glass)", "—", "6–7", "3.3–3.5", "Vitreous to dull", "Opaque",
     (2800, 45000),
     "The ultimate provenance story: this rock formed on Mars in a volcanic eruption approximately 180 million years ago. A massive impact blasted it from the Martian surface with enough force to achieve escape velocity. It traveled through interplanetary space before landing on Earth. Martian origin is verified by trapped gas matching Viking lander measurements of the Martian atmosphere."),

    ("Moldavite — Czech Tektite", "Bohemia and Moravia, Czech Republic",
     "Silica glass (lechatelierite)", "—", "5.5", "2.32–2.38", "Vitreous", "Transparent",
     (65, 850),
     "15 million years ago, a 1.5-kilometer asteroid struck what is now Bavaria, generating a fireball that melted local surface silica and splashed liquid rock across Bohemia and Moravia. Moldavite is that impact glass — each piece formed in less than a second from vaporized European crust, then shaped by supersonic flight before cooling in free fall. The green color comes from iron."),

    ("Libyan Desert Glass", "Great Sand Sea, Libya/Egypt",
     "Silica glass (>99% SiO₂)", "—", "5.5–6", "2.21", "Vitreous", "Transparent",
     (45, 580),
     "Libyan desert glass — found in a 6,500 km² strewn field — is the purest natural silica glass on Earth. Its formation 29 million years ago involved temperatures exceeding 1600°C, suggesting an airburst or impact-generated thermal event so intense it flash-melted the Saharan sand. A carved Libyan desert glass scarab was found in Tutankhamun's pectoral — ancient Egyptians recognized it as extraordinary."),

    ("Australite Button", "South Australia",
     "Silica glass (tektite)", "—", "5.5", "2.38–2.40", "Vitreous", "Transparent",
     (22, 145),
     "Australites are tektites from the Australasian strewn field — impact glass formed 780,000 years ago, likely from a Southeast Asian impact. The distinctive 'button' shape — a disk with a flanged rim — formed as the glass sphere re-entered the atmosphere at an oblique angle, partially melting and being sculpted by atmospheric pressure into this aerodynamic form. They are natural atmospheric re-entry vehicles."),

    ("Darwin Glass — Tasmania", "Darwin Crater, Tasmania, Australia",
     "Silica glass (impact melt)", "—", "5.5", "2.23–2.30", "Vitreous", "Transparent",
     (28, 195),
     "Darwin glass formed 816,000 years ago when a meteorite struck western Tasmania, creating a 1.2-kilometer crater. The glass — pale green, pale grey, white, and bubbly — was melted from local quartzite and dolerite. Unlike moldavite's aerodynamic shaping, Darwin glass shows the chaos of a close-in explosion: twisted, vesicular, sometimes bubbly with trapped gas."),

    ("Iron Meteorite — Toluca", "Toluca Valley, Mexico",
     "Fe-Ni metal (group IAB iron)", "—", "4–5", "7.8", "Metallic", "Opaque",
     (35, 280),
     "The Toluca iron was first reported in 1776 and became one of the most-distributed meteorites in museums worldwide. Its Widmanstätten pattern is particularly coarse — wide bands indicating slow cooling from a large parent body. The fall likely occurred before recorded history; Aztec artifacts of meteoric iron have been found in the region."),

    ("Imilac Pallasite", "Atacama Desert, Chile",
     "Fe-Ni metal + olivine", "—", "varies", "varies", "Metallic + vitreous", "Opaque + translucent",
     (145, 2200),
     "Imilac pallasites from Chile's Atacama Desert show extraordinary olivine crystal size and clarity. The dry desert preserved the metal matrix against weathering while the olivine crystals — gem-quality peridot in composition — remained intact. Cut and polished thin sections transmit light through the olivine in warm yellow-green, while the etched metal shows Widmanstätten pattern. It is both geology and jewelry."),

    ("Seymchan Pallasite", "Magadan Oblast, Russia",
     "Fe-Ni metal + olivine", "—", "varies", "varies", "Metallic + vitreous", "Opaque + translucent",
     (95, 1600),
     "Seymchan was originally classified as an iron meteorite when first found in 1967; only later were olivine-bearing sections discovered. The Seymchan parent body was therefore caught in transition from iron meteorite to pallasite — a snapshot of asteroid differentiation in progress. It is one of meteorite science's most interesting classification ambiguities."),
]

GEOLOGICAL = [
    ("Amethyst Cathedral Geode — Half", "Rio Grande do Sul, Brazil",
     "SiO₂ (quartz)", "—", "7", "2.65", "Vitreous", "Transparent",
     (165, 2800),
     "These cathedral-shaped geodes form in basalt vesicles — gas bubbles from ancient lava flows — over millions of years as silica-rich groundwater precipitates quartz. The purple amethyst color forms in the last stage, when trace iron is present. A geode half shows the full geological biography: the outer chalcedony bands recording early mineral deposition, the amethyst crystal forest pointing inward."),

    ("Celestite Geode — Whole", "Put-in-Bay, Ottawa County, Ohio, USA",
     "SrSO₄", "—", "3–3.5", "3.97", "Vitreous", "Transparent to translucent",
     (85, 680),
     "Ohio's celestite geodes formed in Devonian limestone beds 380 million years ago, when strontium-bearing solutions replaced calcite in pre-existing voids. The result is geodes lined with pale blue to clear orthorhombic crystals — the largest geode of any kind in North America (Crystal Cave on Put-in-Bay Island) is celestite. Crack one open and find a sky."),

    ("Obsidian — Mahogany Flow", "Glass Buttes, Lake County, Oregon, USA",
     "Volcanic glass (rhyolitic)", "—", "5–5.5", "2.35", "Vitreous", "Translucent to opaque",
     (22, 145),
     "Obsidian is volcanic glass — lava that cooled so fast that atoms had no time to arrange into crystals. Mahogany obsidian from Oregon's Glass Buttes shows concentric bands of black and mahogany-brown (iron oxide) laid down as separate lava flows mingled. Indigenous peoples made obsidian blades sharp enough to outcut surgical steel by single-molecule-edge fracturing — a technology not matched by metal until the 20th century."),

    ("Fulgurite — Desert Glass Tube", "Sahara Desert, Libya",
     "Silica glass (lechatelierite)", "—", "5.5–6", "2.2", "Vitreous", "Translucent",
     (18, 95),
     "When lightning strikes sand, the 30,000°C channel fuses it into a hollow tube of silica glass in less than a second. Fulgurites record the exact path of a lightning bolt's passage: branching, tubular, with a glassy interior and sandy exterior. The longest ever found exceeded 4.9 meters, tracing a bolt that struck once and left a monument of glass."),

    ("Banded Iron Formation", "Hamersley Basin, Western Australia",
     "Hematite + chert", "—", "5.5–7", "3.0–5.0", "Dull to metallic", "Opaque",
     (28, 185),
     "These are the oldest beautiful objects on Earth. Banded iron formations (BIFs) formed between 1.8–2.5 billion years ago, when cyanobacteria — the first photosynthetic organisms — began producing oxygen that oxidized dissolved iron from seawater. The alternating iron oxide and chert bands record the rhythmic oxygenation of Earth's early oceans. This rock helped make Earth's atmosphere breathable."),

    ("Septarian Nodule — Polished Half", "Bingham, Utah, USA",
     "Calcite + aragonite + barite in clay matrix", "—", "varies", "varies", "Vitreous to waxy", "Opaque",
     (35, 280),
     "Septarian nodules form in marine muds: organic-rich sediment hardens into an oval nodule, then shrinks as it dries, cracking into a cage-like pattern ('septa') that fills with calcite, aragonite, or barite crystals. Polished in half, the resulting pattern looks like stained glass in earth tones — a natural mosaic that took millions of years to complete."),

    ("Volcanic Bomb — Breadcrust", "Stromboli, Sicily, Italy",
     "Basaltic glass and crystalline basalt", "—", "5–6", "2.7–2.9", "Dull to vesicular", "Opaque",
     (22, 145),
     "Breadcrust bombs are blobs of lava ejected from volcanoes that crack on the surface during flight — the interior continues expanding from dissolved gas while the outer skin cools and solidifies, producing the distinctive cracked-crust pattern. Stromboli has been erupting continuously for 2,000+ years; these bombs were formed in eruptions witnessed by human observers."),

    ("Pele's Tears — Hawaiian", "Kilauea, Big Island, Hawaii, USA",
     "Basaltic glass", "—", "5–5.5", "2.7–2.9", "Vitreous", "Translucent",
     (18, 65),
     "Named for the Hawaiian volcano goddess, Pele's tears are small spheroids of basaltic glass formed when lava fountains eject droplets that solidify in flight. Often connected by hair-thin threads of glass (Pele's hair), each teardrop captures a moment of volcanic energy in a perfect miniature form. The black glass is essentially identical to obsidian, formed in seconds rather than years."),

    ("Suevite — Impact Breccia", "Nördlingen Ries Crater, Bavaria, Germany",
     "Mixed silicates (impact melt + breccia)", "—", "varies", "2.4–2.6", "Dull to vitreous", "Opaque",
     (35, 245),
     "Suevite is impact breccia containing glass bombs and shocked minerals — the concrete of asteroid impact craters. Nördlingen Ries, formed 14.5 million years ago by a 1.5-km asteroid, produced suevite so abundant that the medieval city of Nördlingen was built almost entirely from it. The city's walls contain millions of microscopic diamonds formed by the impact pressure."),

    ("Shatter Cone", "Sudbury Basin, Ontario, Canada",
     "Shocked metasediment", "—", "varies", "2.6–2.8", "Dull to striated", "Opaque",
     (28, 185),
     "Shatter cones are the diagnostic proof of hypervelocity impact: concentric, striated conical fractures produced only by shock pressures exceeding 2–30 GPa. No other geological process produces them. Sudbury's shatter cones formed 1.85 billion years ago in the second-largest confirmed impact on Earth. The Sudbury crater (now eroded to a basin) is 130 km across."),

    ("Eclogite", "Bergen Arcs, Norway",
     "Pyrope garnet + omphacite (Na-Al pyroxene)", "—", "6.5–7.5", "3.4–3.6", "Vitreous", "Translucent to opaque",
     (35, 245),
     "Eclogite is crustal rock metamorphosed under extreme pressure — 30–40 km deep — as tectonic plates subduct. The diagnostic assemblage of red pyrope garnet and bright green omphacite pyroxene creates a visually striking rock that no surface process can produce. Norwegian eclogites were once part of the continental crust before being dragged down and brought back up by orogenesis."),

    ("Oolitic Limestone", "Jurassic Coast, Dorset, England",
     "Calcite ooids in calcite cement", "—", "3", "2.71", "Dull", "Opaque",
     (18, 55),
     "Oolitic limestone is made of 'ooids' — tiny calcite spheres formed in shallow, warm, agitated seawater (like the Bahamas today) where calcium carbonate accretes concentrically around a grain nucleus. Cutting and polishing reveals perfect spheres, each 0.25–2 mm, packed in a calcite mosaic. The Jurassic seas that covered England were indistinguishable from the modern tropics."),

    ("Desert Varnish Sandstone", "Colorado Plateau, Utah, USA",
     "Quartz sandstone + manganese-iron oxide varnish", "—", "7", "2.65", "Dull to waxy", "Opaque",
     (18, 65),
     "Desert varnish — the dark rind coating canyon walls and boulders throughout arid regions — is deposited by microorganisms over thousands of years. Bacteria concentrate manganese from windblown dust and bind it to rock surfaces in a manganese-iron oxide layer sometimes only micrometers thick. Ancient petroglyphs are created by scratching through varnish to expose lighter rock — the varnish dates the minimum age of the art."),

    ("Chalk with Flint Nodule", "Cretaceous chalk, Sussex, England",
     "Calcite (chalk) + chalcedony (flint)", "—", "1–7", "2.2–2.65", "Dull to waxy", "Opaque",
     (18, 55),
     "Flint nodules grew within Cretaceous chalk as silica dissolved from sponge spicules and radiolarians was reprecipitated around organic nuclei. The result is a microcrystalline silica nodule with a smooth, cream to grey exterior and a waxy, conchoidal interior. Paleolithic humans depended on flint technology for 2 million years — its predictable fracture pattern is the geological foundation of human civilization."),

    ("Garnet Schist", "Tauern Window, Austria",
     "Almandine garnet + biotite mica + quartz", "—", "5.5–7.5", "2.8–3.5", "Vitreous to pearly", "Opaque",
     (22, 145),
     "In garnet schist, the pressure and temperature of mountain building are made visible: almandine garnet porphyroblasts grew during regional metamorphism, their chemistry recording the conditions precisely enough that geologists can calculate the depth and temperature of burial. The Austrian Alps expose some of Europe's deepest metamorphic terrains — these specimens were formed at the roots of ancient mountains."),

    ("Pumice from Santorini", "Santorini (Thera), Greece",
     "Rhyolitic volcanic glass + vesicles", "—", "5.5–6", "0.25–0.9", "Dull to vitreous", "Opaque",
     (18, 55),
     "The Minoan eruption of Santorini (~1600 BCE) was one of the largest volcanic events in human history — it produced enough pumice to bury its contemporaries. Pumice is volcanic glass so thoroughly vesiculated that it floats on water. Santorini pumice has been found at the bottoms of the Nile and on the shores of Israel — tsunami evidence from the eruption that may have inspired the Atlantis legend."),

    ("Serpentinite", "Troodos Ophiolite, Cyprus",
     "Antigorite/chrysotile serpentine minerals", "—", "3–4", "2.5–2.6", "Waxy to silky", "Opaque",
     (22, 95),
     "Serpentinite is oceanic mantle rock that has reacted with seawater — the green color comes from serpentine group minerals replacing olivine and pyroxene. The Troodos ophiolite in Cyprus is a slice of ancient ocean floor uplifted by tectonic collision: these rocks formed at a spreading ridge, were hydrated on the seafloor, then thrust onto a continent. Cyprus means 'copper island' — the ancient mines worked the copper ore bodies in this very ophiolite."),

    ("Radiolarite", "Chert Melange, Marin County, California, USA",
     "Microcrystalline silica from radiolarian ooze", "—", "6.5–7", "2.65", "Waxy to dull", "Opaque",
     (18, 55),
     "Radiolarites are siliceous sedimentary rocks formed from the accumulated silica skeletons of radiolarians — single-celled marine organisms with intricate geometric glass skeletons — deposited on the deep ocean floor over millions of years. California's Marin Headlands radiolarites, now exposed as the Franciscan Complex, were formed in the middle of the Pacific and scraped off as the oceanic plate subducted under North America."),

    ("Conglomerate — Tillite", "Gowganda Formation, Ontario, Canada",
     "Mixed clasts in fine matrix", "—", "varies", "2.6–2.8", "Dull", "Opaque",
     (22, 85),
     "The Gowganda tillite (2.3 billion years old) is evidence of Earth's first global glaciation — the 'Huronian' ice age that followed the Great Oxidation Event. Glaciers transported boulders of mixed composition and deposited them in an unsorted matrix. This rock records a time when ice sheets reached the equator, long before complex life evolved."),
]

COLLECTIONS = [
    ("Geological Timeline Collection — 12 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (185, 380),
     "Twelve specimens spanning Earth's 4.56-billion-year story, one per geological era. From a 4.4-billion-year-old zircon (the oldest mineral on Earth) to a Roman volcanic glass and a modern fulgurite. Each specimen arrives with a timeline card and geological context. Start at the beginning; hold time in your hands."),

    ("Rainbow Minerals Collection — 7 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (85, 245),
     "Seven minerals, seven colors of the visible spectrum: red vanadinite, orange crocoite, yellow sulfur crystal, green malachite, blue azurite, indigo blue kyanite, violet amethyst. Each specimen represents a different chromophore mechanism — a different answer to the question 'where does color come from?' Arrives in a display case with color-coded mineral cards."),

    ("Space Rocks Starter Kit — 5 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (95, 280),
     "A curated introduction to extraterrestrial geology: one Gibeon iron meteorite slice (4.5 billion years old, Widmanstätten pattern), one chondrite individual, one Australite button tektite, one Moldavite fragment, and one pallasite olivine-bearing slice. Five objects from beyond Earth, with origin cards for each. The solar system, summarized in a small box."),

    ("Crystal Healing Skeptic's Kit — 6 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (65, 195),
     "Beautiful specimens, rigorous science: six crystals frequently cited in healing traditions, each with a card explaining the actual chemistry, crystal structure, and geological origin. Amethyst (iron in quartz, no scientific healing properties — but extraordinary to look at). Rose quartz (dumortierite inclusions). Clear quartz (piezoelectric properties are real). Malachite (genuine copper ore, handle with care). Selenite (gypsum, actually quite soft). Tourmaline (genuinely piezoelectric). Collect for beauty; understand for science."),

    ("World Tour Collection — 7 Specimens",
     "Global — one per continent",
     "Mixed", "—", "—", "—", "—", "—",
     (145, 380),
     "Seven specimens, seven continents: Gibeon meteorite (Africa/Namibia), Mount Erebus obsidian (Antarctica), Burmese ruby (Asia/Myanmar), Cornish kaolinite (Europe/England), Michigan native copper (North America), Inca rose rhodochrosite (South America/Argentina), Lightning Ridge opal (Australia). The world's mineralogical diversity in one collection."),

    ("Collector's Gemstone Rough Box — 10 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (95, 380),
     "Ten rough gem crystals as nature produced them, before the cutter's intervention: sapphire, ruby, emerald, tanzanite, spinel, garnet, tourmaline, aquamarine, topaz, and opal. Each is accompanied by a card describing what would be required to facet it and what the result might look like. Collector-grade, not gemstone-grade — chosen for scientific interest over commercial value."),

    ("Gift Set — 'The Extraordinary Earth' ($50)",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (48, 52),
     "Four carefully chosen specimens that exemplify what makes Earth's mineral kingdom extraordinary: one fluorite octahedron (perfect cubic cleavage), one labradorite freeform (labradorescence), one pyrite cube (geometric perfection), one rose quartz sphere (the most popular pink mineral). Arrives in a gift box with geological notes for each specimen. An ideal introduction to the mineral kingdom."),

    ("Gift Set — 'Wonders of Deep Time' ($150)",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (145, 155),
     "Five specimens chosen for their extraordinary ages: a 4.56-billion-year-old chondrite meteorite (older than Earth), a 2.5-billion-year-old banded iron formation (evidence of the first oxygen), a 380-million-year-old trilobite (ancient arthropod), a 50-million-year-old amber piece (Eocene resin with inclusions), and a 200-million-year-old ammonite from the Jurassic seas. Deep time made tangible."),

    ("Gift Set — 'Rarest Minerals' ($500)",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (480, 520),
     "Five specimens from the rarest mineral localities on Earth: benitoite from the single deposit in San Benito County, California; jeremejevite from Namibia; tsavorite garnet from the Kenya-Tanzania border; Ural alexandrite (color-change chrysoberyl); and red beryl from Utah's Wah Wah Mountains. Each is a mineralogical rarity that collectors actively seek. Arrives with provenance documentation."),

    ("Educational Kit — 'First Rocks' (Ages 8+)",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (38, 55),
     "Six specimens chosen for handling, examination, and education: quartz crystal (scratch test: scratches glass), calcite (fizzes in vinegar), galena (heavy!), mica (cleaves into sheets), feldspar (pink and blocky), and magnetite (magnetic). Includes a 10x loupe, mineral identification guide, and activity cards with simple experiments. Every future geologist starts somewhere."),

    ("Meteorite Collectors Set — 4 Specimens",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (125, 380),
     "Four meteorite types in one collection: one iron with Widmanstätten pattern (etched slice), one chondrite with visible chondrules, one tektite (Moldavite or Australite), and one pallasite with olivine. A representative cross-section of extraterrestrial material, from the oldest solid matter in the solar system to glass formed by impact events on Earth. Includes classification cards."),

    ("Fluorescent Mineral Set — 5 Specimens + UV Lamp",
     "Global",
     "Mixed", "—", "—", "—", "—", "—",
     (65, 185),
     "Five minerals that transform under ultraviolet light: willemite (intense green fluorescence — 90% of known willemite comes from Franklin, New Jersey), calcite (pink to orange), scheelite (blue-white), fluorite (variable colors), and hyalite opal (neon green). Includes a short-wave UV lamp. Turn off the lights: a different world appears."),
]

# ──────────────────────────────────────────────────────────────────────────────
# STORY PARAGRAPHS
# ──────────────────────────────────────────────────────────────────────────────

STORY_INTROS = [
    "There are objects in this world that carry the weight of unimaginable time.",
    "Every mineral is a story of chemistry, pressure, and patience.",
    "The universe has 13.8 billion years of history. Some of it fits in your hand.",
    "Collectors say that minerals are the universe's autobiography, written in atoms.",
    "What looks like stone is, on closer inspection, frozen time.",
    "The rarest things on Earth were formed by the most ordinary processes, repeated for eons.",
    "Consider what had to happen for this specimen to exist.",
    "Science and beauty are rarely in conflict. Here they converge.",
]

FORMATION_TEMPLATES = [
    "Formed {timeframe} in {process}, this specimen preserves a moment of geological transformation that has never been repeated in exactly this way.",
    "Over {timeframe}, {process} produced this specimen with a precision that chemistry alone, under sufficient time, can achieve.",
    "The {process} responsible for this specimen operated over {timeframe} — a geological whisper that accumulated into extraordinary mineral architecture.",
]

COLLECTOR_NOTES = [
    "Display away from direct sunlight; some minerals fade under prolonged UV exposure.",
    "Dust with a soft brush; avoid water for soft minerals (hardness below 4).",
    "Store on a padded surface; avoid contact with harder minerals.",
    "Handle with care; crystal terminations are irreplaceable once damaged.",
    "The luster is maximized by low-angle raking light — try a single spotlight.",
    "Photograph with a neutral grey background to capture true color.",
    "Best displayed where natural light can play across the surfaces at different times of day.",
]

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

CATEGORY_MAP = {
    "mineral": "Minerals",
    "gemstone": "Gemstones",
    "fossil": "Fossils",
    "meteorite": "Meteorites",
    "geological": "Geological Specimens",
    "collection": "Curated Collections",
}

def make_story(name, locality, seed_story, cat):
    intro = random.choice(STORY_INTROS)
    return (
        f"{intro} {seed_story}\n\n"
        f"This specimen originates from {locality}, one of the world's most significant "
        f"localities for this type of material. Collectors and scientists have drawn from "
        f"this region for generations, and for good reason: the combination of geological "
        f"conditions here produces specimens of exceptional quality and clarity.\n\n"
        f"Every specimen is unique. Photographs approximate the visual experience, but the "
        f"real thing — its weight, its luster under a raking light, the way it catches the "
        f"corner of your eye — can only be experienced directly."
    )

def make_formation(cat, name):
    if cat == "fossil":
        return (
            f"Fossilization is a rare event: fewer than 1 in 10,000 organisms ever become "
            f"fossils, and even fewer survive to be collected. This specimen represents a "
            f"successful preservation — chemistry, burial, and geological luck combining to "
            f"maintain structural detail across millions of years."
        )
    elif cat == "meteorite":
        return (
            f"This material formed outside Earth's atmosphere, in the early solar system. "
            f"Its arrival on Earth was the conclusion of a journey billions of years and "
            f"hundreds of millions of kilometers in the making — from protoplanetary accretion "
            f"to atmospheric entry to the ground beneath your feet."
        )
    elif cat == "collection":
        return (
            f"Each specimen in this collection was individually selected for quality and "
            f"scientific interest. The combination has been chosen to illustrate a specific "
            f"geological or mineralogical theme, with each piece complementing the others."
        )
    else:
        return (
            f"This specimen formed through geological processes operating over timescales "
            f"that dwarf human history. The specific combination of chemistry, temperature, "
            f"pressure, and time at this locality produced material of exceptional quality "
            f"that makes it a valued addition to any serious collection."
        )

def stock(price, cat):
    if cat == "collection":
        return random.randint(5, 20)
    if price > 5000:
        return random.randint(1, 2)
    elif price > 1000:
        return random.randint(1, 3)
    elif price > 200:
        return random.randint(3, 12)
    elif price > 50:
        return random.randint(8, 30)
    else:
        return random.randint(15, 50)

def make_product(template, cat, idx):
    if cat == "collection":
        name, locality, formula, crystal, mohs, sg, luster, transparency, price_range, seed = template
    else:
        name, locality, formula, crystal, mohs, sg, luster, transparency, price_range, seed = template

    price = round(random.uniform(*price_range), 2)
    qty = stock(price, cat)

    p = {
        "sku": f"TC-{cat[:3].upper()}-{idx:04d}",
        "name": name,
        "category": CATEGORY_MAP[cat],
        "subcategory": cat.title(),
        "locality": locality,
        "price": f"{price:.2f}",
        "stock": qty,
        "short_description": seed[:180] + "…" if len(seed) > 180 else seed,
        "description": make_story(name, locality, seed, cat),
        "formation": make_formation(cat, name),
        "locality_detail": f"{name} from {locality}. This locality is known for producing specimens of exceptional quality.",
        "collector_notes": random.choice(COLLECTOR_NOTES),
        "scientific": {
            "formula": formula,
            "crystal_system": crystal,
            "mohs": mohs,
            "specific_gravity": sg,
            "luster": luster,
            "transparency": transparency,
        },
        "tags": [cat, locality.split(",")[-1].strip().lower(), "geological specimen"],
    }
    return p

# ──────────────────────────────────────────────────────────────────────────────
# GENERATE
# Each category is expanded with named variants so we hit target counts.
# ──────────────────────────────────────────────────────────────────────────────

MINERAL_VARIANTS = [
    "— Specimen Grade", "— Cabinet Specimen", "— Miniature", "— Display Piece",
    "— Museum Quality",
]
GEM_VARIANTS = [
    "— Gem Rough", "— Cabinet Specimen", "— Exceptional Quality", "— Collector Grade",
    "— Natural Crystal", "— Large Example",
]
FOSSIL_VARIANTS = [
    "— Museum Replica", "— Display Grade", "— Small Specimen", "— Exceptional Preservation",
    "— Field-Collected", "— Prepared Specimen",
]
MET_VARIANTS = [
    "— Small Individual", "— Large Slice", "— Etched Section", "— Polished Face",
    "— Fragment", "— Oriented Individual",
]
GEO_VARIANTS = [
    "— Display Grade", "— Large Specimen", "— Specimen Grade", "— Polished Face",
    "— Field Specimen",
]
COLLECTION_VARIANTS = [
    "— Budget Edition", "— Standard Set", "— Premium Edition", "— Gift-Boxed",
    "— Deluxe Presentation", "— Educational Edition", "— Compact Set", "— Collector's Edition",
]


def expand_templates(base_list, variants, target_count):
    """Expand base templates using named variants until we reach target_count."""
    all_items = list(base_list)
    vi = 0
    while len(all_items) < target_count:
        variant_suffix = variants[vi % len(variants)]
        for t in base_list:
            if len(all_items) >= target_count:
                break
            name, locality, *rest = t
            all_items.append((f"{name} {variant_suffix}", locality, *rest))
        vi += 1
    return all_items


products = []
idx = 1

# Minerals → 300
all_minerals = expand_templates(MINERALS, MINERAL_VARIANTS, 300)
random.shuffle(all_minerals)
for t in all_minerals[:300]:
    products.append(make_product(t, "mineral", idx))
    idx += 1

# Gemstones → 200
all_gems = expand_templates(GEMSTONES, GEM_VARIANTS, 200)
random.shuffle(all_gems)
for t in all_gems[:200]:
    products.append(make_product(t, "gemstone", idx))
    idx += 1

# Fossils → 200
all_fossils = expand_templates(FOSSILS, FOSSIL_VARIANTS, 200)
random.shuffle(all_fossils)
for t in all_fossils[:200]:
    products.append(make_product(t, "fossil", idx))
    idx += 1

# Meteorites → 100
all_mets = expand_templates(METEORITES, MET_VARIANTS, 100)
random.shuffle(all_mets)
for t in all_mets[:100]:
    products.append(make_product(t, "meteorite", idx))
    idx += 1

# Geological → 100
all_geo = expand_templates(GEOLOGICAL, GEO_VARIANTS, 100)
random.shuffle(all_geo)
for t in all_geo[:100]:
    products.append(make_product(t, "geological", idx))
    idx += 1

# Curated Collections → 100
all_collections = expand_templates(COLLECTIONS, COLLECTION_VARIANTS, 100)
random.shuffle(all_collections)
for t in all_collections[:100]:
    products.append(make_product(t, "collection", idx))
    idx += 1

products = products[:1000]

print(f"Generated {len(products)} products.")
output_path = "import/products.json"
with open(output_path, "w") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)
print(f"Written to {output_path}")
