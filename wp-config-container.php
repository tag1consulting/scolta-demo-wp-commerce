<?php
/** Database charset to use in creating database tables. */
defined( 'DB_CHARSET' ) || define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
defined( 'DB_COLLATE' ) || define( 'DB_COLLATE', '' );

/** Authentication Unique Keys and Salts. */
defined( 'AUTH_KEY' ) || define( 'AUTH_KEY', getenv( 'WP_AUTH_KEY' ) );
defined( 'SECURE_AUTH_KEY' ) || define( 'SECURE_AUTH_KEY', getenv( 'WP_SECURE_AUTH_KEY' ) );
defined( 'LOGGED_IN_KEY' ) || define( 'LOGGED_IN_KEY', getenv( 'WP_LOGGED_IN_KEY' ) );
defined( 'NONCE_KEY' ) || define( 'NONCE_KEY', getenv( 'WP_NONCE_KEY' ) );
defined( 'AUTH_SALT' ) || define( 'AUTH_SALT', getenv( 'WP_AUTH_SALT' ) );
defined( 'SECURE_AUTH_SALT' ) || define( 'SECURE_AUTH_SALT', getenv( 'WP_SECURE_AUTH_SALT' ) );
defined( 'LOGGED_IN_SALT' ) || define( 'LOGGED_IN_SALT', getenv( 'WP_LOGGED_IN_SALT' ) );
defined( 'NONCE_SALT' ) || define( 'NONCE_SALT', getenv( 'WP_NONCE_SALT' ) );

/** Absolute path to the WordPress directory. */
defined( 'ABSPATH' ) || define( 'ABSPATH', dirname( __FILE__ ) . '/' );

defined( 'DB_NAME' ) || define( 'DB_NAME', getenv( 'DB_NAME' ) );
defined( 'DB_USER' ) || define( 'DB_USER', getenv( 'DB_USERNAME' ) );
defined( 'DB_PASSWORD' ) || define( 'DB_PASSWORD', getenv( 'DB_PASSWORD' ) );
defined( 'DB_HOST' ) || define( 'DB_HOST', getenv( 'DB_HOST' ) );
defined( 'WP_HOME' ) || define( 'WP_HOME', getenv( 'WP_HOME' ) );
defined( 'WP_SITEURL' ) || define( 'WP_SITEURL', getenv( 'WP_SITEURL' ) );
defined( 'WP_DEBUG' ) || define( 'WP_DEBUG', filter_var( getenv( 'WP_DEBUG' ), FILTER_VALIDATE_BOOLEAN ) );

if ( ! isset( $table_prefix ) || empty( $table_prefix ) ) {
	// phpcs:disable WordPress.WP.GlobalVariablesOverride.Prohibited
	$table_prefix = 'wp_';
	// phpcs:enable
}
