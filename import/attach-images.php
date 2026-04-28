<?php
/**
 * Attach placeholder images to WooCommerce products.
 * Run via: ddev wp eval-file import/attach-images.php
 *
 * Matches each PNG in wp-content/uploads/terra-collecta/ to a product by SKU
 * prefix, imports it into the media library, and sets it as the product's
 * featured image.
 */

$uploads_dir   = get_home_path() . 'wp-content/uploads/terra-collecta';
$attached      = 0;
$skipped       = 0;
$errors        = 0;

if ( ! is_dir( $uploads_dir ) ) {
	WP_CLI::error( "Image directory not found: $uploads_dir" );
	exit( 1 );
}

// Build SKU → product_id map once (faster than per-product wc_get_product_id_by_sku)
WP_CLI::log( 'Building SKU → product ID index…' );
$sku_map = [];
$product_ids = get_posts( [
	'post_type'      => 'product',
	'posts_per_page' => -1,
	'fields'         => 'ids',
] );
foreach ( $product_ids as $pid ) {
	$sku = get_post_meta( $pid, '_sku', true );
	if ( $sku ) {
		$sku_map[ $sku ] = $pid;
	}
}
WP_CLI::log( sprintf( 'Found %d products.', count( $sku_map ) ) );

// Scan image directory
$files = glob( $uploads_dir . '/*.png' );
sort( $files );
WP_CLI::log( sprintf( 'Processing %d images…', count( $files ) ) );

require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

foreach ( $files as $filepath ) {
	$filename = basename( $filepath );

	// Extract SKU from filename: TC-MIN-0001-amethyst-cluster-...png
	if ( ! preg_match( '/^(TC-[A-Z]{3}-\d{4})/', $filename, $m ) ) {
		$skipped++;
		continue;
	}
	$sku = $m[1];

	if ( ! isset( $sku_map[ $sku ] ) ) {
		$skipped++;
		continue;
	}
	$product_id = $sku_map[ $sku ];

	// Skip if already has a featured image
	if ( has_post_thumbnail( $product_id ) ) {
		$skipped++;
		continue;
	}

	// Copy file into WP uploads and create attachment
	$upload = wp_upload_bits( $filename, null, file_get_contents( $filepath ) );
	if ( $upload['error'] ) {
		WP_CLI::warning( "Upload error for $filename: {$upload['error']}" );
		$errors++;
		continue;
	}

	$wp_filetype = wp_check_filetype( $upload['file'] );
	$attachment  = [
		'post_mime_type' => $wp_filetype['type'],
		'post_title'     => preg_replace( '/\.[^.]+$/', '', $filename ),
		'post_content'   => '',
		'post_status'    => 'inherit',
		'post_parent'    => $product_id,
	];

	$attach_id = wp_insert_attachment( $attachment, $upload['file'], $product_id );
	if ( is_wp_error( $attach_id ) ) {
		WP_CLI::warning( "Attachment error for $filename: " . $attach_id->get_error_message() );
		$errors++;
		continue;
	}

	$attach_data = wp_generate_attachment_metadata( $attach_id, $upload['file'] );
	wp_update_attachment_metadata( $attach_id, $attach_data );
	set_post_thumbnail( $product_id, $attach_id );

	$attached++;

	if ( $attached % 100 === 0 ) {
		WP_CLI::log( sprintf( '  Attached: %d (skipped: %d, errors: %d)', $attached, $skipped, $errors ) );
	}
}

WP_CLI::success( sprintf(
	'Image attachment complete. Attached: %d, Skipped: %d, Errors: %d',
	$attached, $skipped, $errors
) );
