<?php
/**
 * Scolta content indexing configuration for Terra Collecta.
 *
 * Terra Collecta is a product catalog demo. Only WooCommerce products
 * should appear in search results. Static pages (About, Cart, Checkout,
 * My Account, etc.) contain site chrome and marketing copy that would
 * contaminate product searches.
 *
 * This mu-plugin overrides the post_types setting so only 'product'
 * is indexed, regardless of what is saved in the admin. It applies at
 * runtime via the options filter — no database change is needed, and
 * it survives a database reset.
 *
 * It also enriches each product's indexed content with structured data
 * (price, category, SKU, stock) so that pricing queries like "what is
 * the most expensive stone?" can be answered by the AI layer.
 */

add_filter( 'option_scolta_settings', 'tc_restrict_scolta_post_types' );

/**
 * Restrict Scolta indexing to WooCommerce products only.
 *
 * @param mixed $settings Raw value from get_option( 'scolta_settings' ).
 * @return mixed Settings with post_types forced to ['product'].
 */
function tc_restrict_scolta_post_types( $settings ) {
	if ( is_array( $settings ) ) {
		$settings['post_types'] = array( 'product' );
	}
	return $settings;
}

add_filter( 'scolta_content_item', 'tc_enrich_product_content_item', 10, 2 );

/**
 * Inject WooCommerce product structured data into the Scolta index.
 *
 * Appends price, category, SKU, and stock status to each product's
 * indexed body so that:
 *   - AI queries about pricing ("most expensive", "cheapest") have
 *     price data available in the retrieved excerpts.
 *   - Search result snippets surface price alongside the description.
 *
 * The appended block is plain text wrapped in a <div> so Pagefind
 * indexes it without treating it as navigation or boilerplate.
 *
 * @param \Tag1\Scolta\Export\ContentItem $item The content item about to be indexed.
 * @param \WP_Post                        $post The WordPress post object.
 * @return \Tag1\Scolta\Export\ContentItem Enriched content item.
 */
function tc_enrich_product_content_item( $item, $post ) {
	if ( $post->post_type !== 'product' || ! function_exists( 'wc_get_product' ) ) {
		return $item;
	}

	$product = wc_get_product( $post->ID );
	if ( ! $product ) {
		return $item;
	}

	$lines = array();

	// Price — use raw numeric value with explicit currency label so the AI
	// can compare prices across results without parsing HTML entities.
	$price = $product->get_price();
	if ( $price !== '' && $price !== null ) {
		$currency       = get_woocommerce_currency_symbol();
		$currency_plain = html_entity_decode( $currency, ENT_HTML5, 'UTF-8' );
		$lines[]        = 'Price: ' . $currency_plain . number_format( (float) $price, 2 );
	}

	// Regular / sale distinction gives the AI enough context to mention sales.
	$regular = $product->get_regular_price();
	$sale    = $product->get_sale_price();
	if ( $sale !== '' && $sale !== null && $regular !== '' && $sale !== $regular ) {
		$currency_plain = isset( $currency_plain )
			? $currency_plain
			: html_entity_decode( get_woocommerce_currency_symbol(), ENT_HTML5, 'UTF-8' );
		$lines[] = 'Regular price: ' . $currency_plain . number_format( (float) $regular, 2 );
		$lines[] = 'Sale price: ' . $currency_plain . number_format( (float) $sale, 2 );
	}

	// WooCommerce category.
	$terms = get_the_terms( $post->ID, 'product_cat' );
	if ( $terms && ! is_wp_error( $terms ) ) {
		$cat_names = wp_list_pluck( $terms, 'name' );
		$lines[]   = 'Category: ' . implode( ', ', $cat_names );
	}

	// SKU.
	$sku = $product->get_sku();
	if ( $sku ) {
		$lines[] = 'SKU: ' . $sku;
	}

	// Stock status.
	if ( $product->is_in_stock() ) {
		$qty     = $product->get_stock_quantity();
		$lines[] = 'Availability: In Stock' . ( $qty !== null ? ' (' . (int) $qty . ' available)' : '' );
	} else {
		$lines[] = 'Availability: Out of Stock';
	}

	if ( empty( $lines ) ) {
		return $item;
	}

	$structured_html = '<div class="tc-product-structured-data">'
		. '<p>' . implode( '</p><p>', array_map( 'esc_html', $lines ) ) . '</p>'
		. '</div>';

	return $item->cloneWith(['bodyHtml' => $item->bodyHtml . $structured_html]);
}
