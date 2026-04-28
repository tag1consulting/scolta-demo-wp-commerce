<?php
/**
 * Swap placeholder PNGs for real JPEG images on WooCommerce products.
 * Run via: ddev wp eval-file import/attach-jpegs.php
 *
 * For each product whose SKU has a matching JPEG in uploads/terra-collecta/:
 *   1. Delete the existing PNG featured-image attachment (and its media-library copy).
 *   2. Copy the JPEG into the WP media library via wp_upload_bits().
 *   3. Set the new JPEG attachment as the featured image.
 *
 * Products without a matching JPEG keep their placeholder PNG unchanged.
 * Safe to re-run: skips products whose thumbnail is already a JPEG.
 */

require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

$source_dir = get_home_path() . 'wp-content/uploads/terra-collecta';

// Build SKU → JPEG path map from files on disk
$jpeg_map = [];
foreach ( glob( "$source_dir/*.jpg" ) as $path ) {
    $file = basename( $path );
    if ( preg_match( '/^(TC-[A-Z]{3}-\d{4})-/', $file, $m ) ) {
        $jpeg_map[ $m[1] ] = $path;
    }
}
WP_CLI::log( 'JPEG files found: ' . count( $jpeg_map ) );

// Build SKU → product ID index
WP_CLI::log( 'Building SKU → product ID index…' );
$sku_map = [];
foreach ( get_posts( [ 'post_type' => 'product', 'posts_per_page' => -1, 'fields' => 'ids' ] ) as $pid ) {
    $sku = get_post_meta( $pid, '_sku', true );
    if ( $sku ) $sku_map[ $sku ] = $pid;
}
WP_CLI::log( 'Products found: ' . count( $sku_map ) );

$updated  = 0;
$skipped  = 0;
$no_jpeg  = 0;
$errors   = 0;

foreach ( $sku_map as $sku => $product_id ) {
    if ( ! isset( $jpeg_map[ $sku ] ) ) {
        $no_jpeg++;
        continue;
    }

    // Already has a JPEG thumbnail? Skip (idempotent)
    $existing_thumb = get_post_thumbnail_id( $product_id );
    if ( $existing_thumb ) {
        $mime = get_post_mime_type( $existing_thumb );
        if ( $mime === 'image/jpeg' ) {
            $skipped++;
            continue;
        }
    }

    $jpeg_path = $jpeg_map[ $sku ];
    $filename  = basename( $jpeg_path );

    // Copy JPEG into WP media library
    $upload = wp_upload_bits( $filename, null, file_get_contents( $jpeg_path ) );
    if ( ! empty( $upload['error'] ) ) {
        WP_CLI::warning( "Upload error for $sku: {$upload['error']}" );
        $errors++;
        continue;
    }

    $wp_filetype = wp_check_filetype( $upload['file'] );
    $attachment  = [
        'post_mime_type' => $wp_filetype['type'],
        'post_title'     => get_the_title( $product_id ),
        'post_content'   => '',
        'post_status'    => 'inherit',
        'post_parent'    => $product_id,
    ];

    $attach_id = wp_insert_attachment( $attachment, $upload['file'], $product_id );
    if ( is_wp_error( $attach_id ) ) {
        WP_CLI::warning( "Attachment insert failed for $sku: " . $attach_id->get_error_message() );
        $errors++;
        continue;
    }

    $meta = wp_generate_attachment_metadata( $attach_id, $upload['file'] );
    wp_update_attachment_metadata( $attach_id, $meta );

    // Delete old PNG thumbnail attachment before setting the new one
    if ( $existing_thumb && $existing_thumb !== $attach_id ) {
        wp_delete_attachment( $existing_thumb, true );
    }

    set_post_thumbnail( $product_id, $attach_id );
    $updated++;

    if ( $updated % 100 === 0 ) {
        WP_CLI::log( "  Updated $updated…" );
    }
}

WP_CLI::success( "Done." );
WP_CLI::log( "  Updated (PNG → JPEG): $updated" );
WP_CLI::log( "  Already JPEG (skip):  $skipped" );
WP_CLI::log( "  No JPEG available:    $no_jpeg" );
WP_CLI::log( "  Errors:               $errors" );
