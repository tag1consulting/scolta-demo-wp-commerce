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
