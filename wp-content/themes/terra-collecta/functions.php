<?php
/**
 * Terra Collecta child theme functions.
 */

add_action( 'wp_enqueue_scripts', 'tc_enqueue_styles' );
function tc_enqueue_styles() {
	wp_enqueue_style(
		'tc-google-fonts',
		'https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap',
		array(),
		null
	);
	wp_enqueue_style(
		'parent-style',
		get_template_directory_uri() . '/style.css',
		array( 'tc-google-fonts' )
	);
	wp_enqueue_style(
		'terra-collecta-style',
		get_stylesheet_uri(),
		array( 'parent-style' ),
		wp_get_theme()->get( 'Version' )
	);
	wp_enqueue_script(
		'terra-collecta-modal',
		get_stylesheet_directory_uri() . '/js/checkout-modal.js',
		array(),
		'1.0.0',
		true
	);
	wp_localize_script( 'terra-collecta-modal', 'tcModal', array(
		'shopUrl' => wc_get_page_permalink( 'shop' ),
	) );
}

/* ---------------------------------------------------------------
   WooCommerce theme support
   --------------------------------------------------------------- */
add_action( 'after_setup_theme', 'tc_woocommerce_support' );
function tc_woocommerce_support() {
	add_theme_support( 'woocommerce' );
	add_theme_support( 'wc-product-gallery-zoom' );
	add_theme_support( 'wc-product-gallery-lightbox' );
	add_theme_support( 'wc-product-gallery-slider' );
}

/* ---------------------------------------------------------------
   Demo modal HTML — injected in footer
   --------------------------------------------------------------- */
add_action( 'wp_footer', 'tc_demo_modal_html' );
function tc_demo_modal_html() {
	?>
	<div id="tc-demo-overlay" role="dialog" aria-modal="true" aria-labelledby="tc-modal-title">
		<div id="tc-demo-modal">
			<span class="tc-modal-gem" aria-hidden="true">💎</span>
			<h2 id="tc-modal-title">Thank you for your impeccable taste.</h2>
			<p>
				Terra Collecta is a demonstration site for <strong>Scolta search technology</strong>.
				These specimens exist only in our carefully curated imagination — no transactions will be processed.
			</p>
			<p class="tc-modal-tagline">
				The real treasure here? The search that helped you find exactly the right rock among a thousand possibilities.
			</p>
			<a href="<?php echo esc_url( wc_get_page_permalink( 'shop' ) ); ?>" class="tc-modal-btn" id="tc-modal-close">
				Keep Exploring
			</a>
		</div>
	</div>
	<?php
}

/* ---------------------------------------------------------------
   Redirect checkout to demo modal instead of completing order
   --------------------------------------------------------------- */
add_action( 'woocommerce_checkout_order_processed', 'tc_intercept_order', 1, 3 );
function tc_intercept_order( $order_id, $posted_data, $order ) {
	// Mark order as demo, do not process payment
	$order->update_status( 'cancelled', 'Terra Collecta demo — no real transaction.' );
}

/* ---------------------------------------------------------------
   Product scientific details — custom meta rendering
   --------------------------------------------------------------- */
add_action( 'woocommerce_single_product_summary', 'tc_scientific_summary', 25 );
function tc_scientific_summary() {
	global $product;
	$fields = array(
		'_tc_formula'      => 'Chemical Formula',
		'_tc_crystal'      => 'Crystal System',
		'_tc_mohs'         => 'Mohs Hardness',
		'_tc_sg'           => 'Specific Gravity',
		'_tc_luster'       => 'Luster',
		'_tc_transparency' => 'Transparency',
	);
	$has_data = false;
	foreach ( $fields as $key => $label ) {
		if ( get_post_meta( $product->get_id(), $key, true ) ) {
			$has_data = true;
			break;
		}
	}
	if ( ! $has_data ) return;
	echo '<table class="tc-scientific-table">';
	foreach ( $fields as $key => $label ) {
		$val = get_post_meta( $product->get_id(), $key, true );
		if ( $val ) {
			printf(
				'<tr><th>%s</th><td>%s</td></tr>',
				esc_html( $label ),
				esc_html( $val )
			);
		}
	}
	echo '</table>';
}

/* ---------------------------------------------------------------
   Disable reviews (optional — keep product pages clean for demo)
   --------------------------------------------------------------- */
add_filter( 'woocommerce_product_tabs', 'tc_remove_reviews_tab' );
function tc_remove_reviews_tab( $tabs ) {
	unset( $tabs['reviews'] );
	return $tabs;
}

/* ---------------------------------------------------------------
   Show stock on product page (adds realism)
   --------------------------------------------------------------- */
add_filter( 'woocommerce_get_availability_text', 'tc_availability_text', 10, 2 );
function tc_availability_text( $text, $product ) {
	if ( $product->is_in_stock() ) {
		$qty = $product->get_stock_quantity();
		if ( $qty !== null && $qty <= 3 ) {
			$text = sprintf( 'Only %d available — a rare find.', $qty );
		}
	}
	return $text;
}

/* ---------------------------------------------------------------
   Custom product tab: Formation & Locality
   --------------------------------------------------------------- */
add_filter( 'woocommerce_product_tabs', 'tc_add_formation_tab' );
function tc_add_formation_tab( $tabs ) {
	global $product;
	$formation = get_post_meta( $product->get_id(), '_tc_formation', true );
	$locality  = get_post_meta( $product->get_id(), '_tc_locality', true );
	$collector = get_post_meta( $product->get_id(), '_tc_collector_notes', true );

	if ( $formation || $locality || $collector ) {
		$tabs['tc_formation'] = array(
			'title'    => 'Formation & Locality',
			'priority' => 20,
			'callback' => 'tc_formation_tab_content',
		);
	}
	return $tabs;
}

function tc_formation_tab_content() {
	global $product;
	$id        = $product->get_id();
	$formation = get_post_meta( $id, '_tc_formation', true );
	$locality  = get_post_meta( $id, '_tc_locality', true );
	$collector = get_post_meta( $id, '_tc_collector_notes', true );

	if ( $formation ) {
		echo '<h3 class="tc-section-heading">Formation</h3>';
		echo '<p>' . wp_kses_post( $formation ) . '</p>';
	}
	if ( $locality ) {
		echo '<h3 class="tc-section-heading">Locality</h3>';
		echo '<p>' . wp_kses_post( $locality ) . '</p>';
	}
	if ( $collector ) {
		echo '<h3 class="tc-section-heading">Collector Notes</h3>';
		echo '<p>' . wp_kses_post( $collector ) . '</p>';
	}
}

/* ---------------------------------------------------------------
   Category badge on shop/archive product cards
   --------------------------------------------------------------- */
add_action( 'woocommerce_before_shop_loop_item_title', 'tc_show_category_badge', 15 );
function tc_show_category_badge() {
	global $product;
	$terms = get_the_terms( $product->get_id(), 'product_cat' );
	if ( $terms && ! is_wp_error( $terms ) ) {
		// Skip the uncategorized default
		$cats = array_filter( $terms, fn( $t ) => 'uncategorized' !== $t->slug );
		if ( $cats ) {
			$cat = reset( $cats );
			printf( '<span class="tc-category-badge">%s</span>', esc_html( $cat->name ) );
		}
	}
}

/* ---------------------------------------------------------------
   Key scientific detail on shop/archive product cards
   --------------------------------------------------------------- */
add_action( 'woocommerce_after_shop_loop_item_title', 'tc_show_key_detail', 15 );
function tc_show_key_detail() {
	global $product;
	$mohs = get_post_meta( $product->get_id(), '_tc_mohs', true );
	if ( $mohs ) {
		printf( '<span class="tc-key-detail">Mohs hardness: %s</span>', esc_html( $mohs ) );
		return;
	}
	$crystal = get_post_meta( $product->get_id(), '_tc_crystal', true );
	if ( $crystal ) {
		printf( '<span class="tc-key-detail">%s</span>', esc_html( $crystal ) );
	}
}

/* ---------------------------------------------------------------
   Randomised default sort — shop looks different each visit
   --------------------------------------------------------------- */
add_filter( 'woocommerce_default_catalog_orderby', function() {
	return 'rand';
} );

add_filter( 'woocommerce_catalog_orderby', function( $options ) {
	return array_merge( array( 'rand' => 'Surprise Me' ), $options );
} );

/* ---------------------------------------------------------------
   Rich Scolta search result cards

   Two halves. The filter below puts a product's thumbnail and its
   display price into the search index, next to the price, stock and
   category metadata the Scolta plugin already writes for a WooCommerce
   product. The assets loaded under it paint a card from that metadata,
   so a result list of twelve products costs zero extra server calls.
   --------------------------------------------------------------- */

/**
 * Image size the search result card's thumbnail uses.
 *
 * woocommerce_thumbnail is the 300x300 crop the shop grid already
 * generates for every product, so the card introduces no new derivative
 * and every image it asks for is already on disk. It is roughly twice
 * the 140px box the card paints, which keeps it sharp on a 2x display.
 */
const TC_SCOLTA_CARD_IMAGE_SIZE = 'woocommerce_thumbnail';

/**
 * Adds the per-product data the search result cards paint.
 *
 * The Scolta plugin's own WooCommerce mapping already writes regular_price,
 * sale_price, sku, stock_status and product_cat into the item's metadata,
 * and price into sortable. Two things it cannot know are added here: which
 * image to show, and how this shop wants a price written.
 *
 * Metadata costs only the bytes of its own keys in each fragment, unlike
 * sortable, which writes a corpus-wide pf_meta entry. The keys "title" and
 * "date" are deliberately avoided: they lose to the built-in values on a
 * collision.
 *
 * @param \Tag1\Scolta\Export\ContentItem $item The item about to be indexed.
 * @param \WP_Post                        $post The post it came from.
 * @return \Tag1\Scolta\Export\ContentItem The item, possibly with metadata added.
 */
add_filter( 'scolta_content_item', 'tc_scolta_card_metadata', 10, 2 );
function tc_scolta_card_metadata( $item, $post ) {
	if ( 'product' !== $post->post_type ) {
		return $item;
	}

	$metadata = $item->metadata;

	$image = tc_scolta_card_image( $post->ID );
	if ( null !== $image ) {
		$metadata['image'] = $image['url'];
		if ( '' !== $image['alt'] ) {
			$metadata['image_alt'] = $image['alt'];
		}
	}

	$price = tc_scolta_card_price( $post->ID );
	if ( array() !== $price ) {
		$metadata = array_merge( $metadata, $price );
	}

	if ( $metadata === $item->metadata ) {
		return $item;
	}

	return $item->cloneWith( array( 'metadata' => $metadata ) );
}

/**
 * Resolves a product's featured image to a card thumbnail URL and alt text.
 *
 * The URL is made root-relative. WordPress stores an absolute one built from
 * home_url(), and this site's stored home_url is https while DDEV also serves
 * it over http, so an absolute URL in the index means every card on a plain
 * http visit requests a different origin than the page it is on. Root-relative
 * sidesteps that and makes the committed index portable between the DDEV site
 * and the container image, which do not share a hostname either.
 *
 * @param int $post_id The product.
 * @return array{url: string, alt: string}|null Thumbnail data, or null when the
 *   product has no usable featured image. Null simply means the fragment
 *   carries no "image" key and the card renders without a thumbnail.
 */
function tc_scolta_card_image( int $post_id ): ?array {
	$attachment_id = get_post_thumbnail_id( $post_id );
	if ( ! $attachment_id ) {
		return null;
	}

	$src = wp_get_attachment_image_src( $attachment_id, TC_SCOLTA_CARD_IMAGE_SIZE );
	if ( ! is_array( $src ) || empty( $src[0] ) ) {
		return null;
	}

	$url  = (string) $src[0];
	$home = wp_parse_url( home_url(), PHP_URL_HOST );
	$path = wp_parse_url( $url, PHP_URL_PATH );
	$host = wp_parse_url( $url, PHP_URL_HOST );
	if ( is_string( $path ) && '' !== $path && ( null === $host || $host === $home ) ) {
		$url = $path;
	}

	return array(
		'url' => $url,
		'alt' => trim( (string) get_post_meta( $attachment_id, '_wp_attachment_image_alt', true ) ),
	);
}

/**
 * Formats a product's price the way this shop writes prices.
 *
 * Formatted here rather than in the browser because the currency symbol, its
 * position, the thousands separator and the decimal count are all WooCommerce
 * settings, and a renderer that reinvented them would drift from the price on
 * the product page the card links to. wc_price() returns markup, so the
 * amounts go through wc_format_decimal() and the currency symbol is decoded
 * from the entity WooCommerce stores it as; the renderer escapes both.
 *
 * A sale writes a second key rather than a marked-up string, so the card can
 * strike the old price rather than print "was" inside a sentence. No product
 * in the current catalogue is on sale, so price_was is dormant on this data
 * and correct the moment one is.
 *
 * @param int $post_id The product.
 * @return array<string, string> Zero, one or two metadata keys.
 */
function tc_scolta_card_price( int $post_id ): array {
	if ( ! function_exists( 'wc_get_product' ) ) {
		return array();
	}
	$product = wc_get_product( $post_id );
	if ( ! $product ) {
		return array();
	}

	$symbol = html_entity_decode( get_woocommerce_currency_symbol(), ENT_QUOTES | ENT_HTML5, 'UTF-8' );
	$format = static function ( $amount ) use ( $symbol ): string {
		if ( '' === $amount || null === $amount ) {
			return '';
		}
		$number = wc_price( $amount, array( 'currency' => get_woocommerce_currency() ) );
		// wc_price() is markup and carries the symbol as an entity; strip both
		// and rebuild the plain string the renderer will escape.
		$plain = trim( html_entity_decode( wp_strip_all_tags( $number ), ENT_QUOTES | ENT_HTML5, 'UTF-8' ) );
		return '' !== $plain ? $plain : $symbol . wc_format_decimal( $amount, wc_get_price_decimals() );
	};

	$out   = array();
	$price = $format( $product->get_price() );
	if ( '' !== $price ) {
		$out['price_display'] = $price;
	}
	if ( $product->is_on_sale() ) {
		$was = $format( $product->get_regular_price() );
		if ( '' !== $was && $was !== $price ) {
			$out['price_was'] = $was;
		}
	}

	return $out;
}

/**
 * Loads the result-card renderer and its stylesheet.
 *
 * Hooked to wp_footer rather than wp_enqueue_scripts, and gated on the Scolta
 * handle actually being enqueued. The plugin's shortcode enqueues scolta.js
 * while the page content renders, which is after wp_enqueue_scripts has run,
 * so at that earlier hook the handle does not exist yet and a dependency on it
 * would be silently dropped. By wp_footer it is registered, the dependency
 * takes, and both the script and the stylesheet land after the bundle's own —
 * which is what the renderer needs (window.Scolta must exist when this file
 * executes) and what the stylesheet needs (it redeclares Scolta's documented
 * custom properties at the same specificity, so it has to be second).
 *
 * Priority 5 puts it before wp_print_footer_scripts at 20.
 */
add_action( 'wp_footer', 'tc_scolta_rich_results_assets', 5 );
function tc_scolta_rich_results_assets(): void {
	if ( ! wp_script_is( 'scolta-search', 'enqueued' ) ) {
		return;
	}

	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	$js = $dir . '/js/scolta-rich-results.js';
	if ( file_exists( $js ) ) {
		wp_enqueue_script(
			'tc-scolta-rich-results',
			$uri . '/js/scolta-rich-results.js',
			array( 'scolta-search' ),
			(string) filemtime( $js ),
			true
		);
	}

	$css = $dir . '/css/scolta-rich-results.css';
	if ( file_exists( $css ) ) {
		wp_enqueue_style(
			'tc-scolta-rich-results',
			$uri . '/css/scolta-rich-results.css',
			array( 'scolta-search' ),
			(string) filemtime( $css )
		);
	}
}
