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
