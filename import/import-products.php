<?php
/**
 * Terra Collecta product importer.
 * Run via: ddev wp eval-file import/import-products.php
 *
 * Imports all 1,000 products from import/products.json into WooCommerce.
 * Idempotent: skips products whose SKU already exists.
 */

if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', dirname( __DIR__ ) . '/' );
}

$json_path = __DIR__ . '/products.json';
if ( ! file_exists( $json_path ) ) {
	WP_CLI::error( "products.json not found at $json_path" );
	exit( 1 );
}

$products = json_decode( file_get_contents( $json_path ), true );
if ( ! $products ) {
	WP_CLI::error( 'Failed to parse products.json' );
	exit( 1 );
}

WP_CLI::log( sprintf( 'Importing %d products…', count( $products ) ) );

$created  = 0;
$skipped  = 0;
$errors   = 0;
$total    = count( $products );

// Pre-build a category cache so we don't re-query repeatedly.
$cat_cache = [];

function tc_get_or_create_term( $name, $taxonomy, $parent_id = 0 ) {
	global $cat_cache;
	$key = "$taxonomy::$parent_id::$name";
	if ( isset( $cat_cache[ $key ] ) ) {
		return $cat_cache[ $key ];
	}
	$existing = get_term_by( 'name', $name, $taxonomy );
	if ( $existing ) {
		$cat_cache[ $key ] = $existing->term_id;
		return $existing->term_id;
	}
	$args = [ 'parent' => $parent_id ];
	$result = wp_insert_term( $name, $taxonomy, $args );
	if ( is_wp_error( $result ) ) {
		WP_CLI::warning( "Could not create term '$name' in '$taxonomy': " . $result->get_error_message() );
		return 0;
	}
	$cat_cache[ $key ] = $result['term_id'];
	return $result['term_id'];
}

foreach ( $products as $i => $data ) {
	$sku = $data['sku'] ?? '';

	// Skip if already imported
	if ( $sku ) {
		$existing_id = wc_get_product_id_by_sku( $sku );
		if ( $existing_id ) {
			$skipped++;
			continue;
		}
	}

	$product = new WC_Product_Simple();
	$product->set_name( $data['name'] ?? 'Unnamed Specimen' );
	$product->set_sku( $sku );
	$product->set_regular_price( $data['price'] ?? '0' );
	$product->set_description( $data['description'] ?? '' );
	$product->set_short_description( $data['short_description'] ?? '' );
	$product->set_status( 'publish' );
	$product->set_catalog_visibility( 'visible' );
	$product->set_sold_individually( false );

	// Stock
	$stock = intval( $data['stock'] ?? 10 );
	$product->set_manage_stock( true );
	$product->set_stock_quantity( $stock );
	$product->set_stock_status( $stock > 0 ? 'instock' : 'outofstock' );

	// Category hierarchy: Top-level → Subcategory
	$top_name = $data['category'] ?? 'Minerals';
	$sub_name = $data['subcategory'] ?? $top_name;

	$top_id = tc_get_or_create_term( $top_name, 'product_cat' );
	$sub_id = 0;
	if ( $sub_name && $sub_name !== $top_name ) {
		$sub_id = tc_get_or_create_term( $sub_name, 'product_cat', $top_id );
	}

	$cat_ids = array_filter( [ $top_id, $sub_id ] );
	$product->set_category_ids( $cat_ids );

	// Tags
	$tag_ids = [];
	foreach ( $data['tags'] ?? [] as $tag_name ) {
		$tag_name = trim( $tag_name );
		if ( ! $tag_name ) continue;
		$tag = tc_get_or_create_term( $tag_name, 'product_tag' );
		if ( $tag ) $tag_ids[] = $tag;
	}
	if ( $tag_ids ) $product->set_tag_ids( $tag_ids );

	// Save main product
	try {
		$product_id = $product->save();
	} catch ( Exception $e ) {
		WP_CLI::warning( "Error saving product '{$data['name']}': " . $e->getMessage() );
		$errors++;
		continue;
	}

	// Custom meta: scientific details
	$sci = $data['scientific'] ?? [];
	if ( ! empty( $sci['formula'] ) )      update_post_meta( $product_id, '_tc_formula',      $sci['formula'] );
	if ( ! empty( $sci['crystal_system'] ) ) update_post_meta( $product_id, '_tc_crystal', $sci['crystal_system'] );
	if ( ! empty( $sci['mohs'] ) )         update_post_meta( $product_id, '_tc_mohs',         $sci['mohs'] );
	if ( ! empty( $sci['specific_gravity'] ) ) update_post_meta( $product_id, '_tc_sg',        $sci['specific_gravity'] );
	if ( ! empty( $sci['luster'] ) )       update_post_meta( $product_id, '_tc_luster',       $sci['luster'] );
	if ( ! empty( $sci['transparency'] ) ) update_post_meta( $product_id, '_tc_transparency', $sci['transparency'] );

	// Custom meta: narrative fields
	if ( ! empty( $data['formation'] ) )       update_post_meta( $product_id, '_tc_formation',       $data['formation'] );
	if ( ! empty( $data['locality_detail'] ) ) update_post_meta( $product_id, '_tc_locality',         $data['locality_detail'] );
	if ( ! empty( $data['collector_notes'] ) ) update_post_meta( $product_id, '_tc_collector_notes',  $data['collector_notes'] );
	if ( ! empty( $data['locality'] ) )        update_post_meta( $product_id, '_tc_locality_short',   $data['locality'] );

	$created++;

	if ( ( $created + $skipped + $errors ) % 50 === 0 ) {
		WP_CLI::log( sprintf( '  Progress: %d/%d (created: %d, skipped: %d, errors: %d)',
			$created + $skipped + $errors, $total, $created, $skipped, $errors ) );
	}
}

WP_CLI::success( sprintf(
	'Import complete. Created: %d, Skipped: %d, Errors: %d',
	$created, $skipped, $errors
) );
