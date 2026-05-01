<?php
/**
 * #ddev-generated: Automatically generated WordPress settings file.
 * ddev manages this file and may delete or overwrite the file unless this comment is removed.
 * It is recommended that you leave this file alone.
 *
 * @package ddevapp
 */

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/** Authentication Unique Keys and Salts. */
define( 'AUTH_KEY', 'gDvtMgBIatZeLsnNmZllJChbxKqCpcdSNsGoDfUqDOdvqnJoQoIJhIILbwvRDCiP' );
define( 'SECURE_AUTH_KEY', 'uMzYkAGtWSRflPjZnPfXRoysbuxVaNhQsBgkjxXtKNfsXJPpptSOjUCKkVDutzMG' );
define( 'LOGGED_IN_KEY', 'xpJQnecDVPrsvzUrjSLyaKZhuQlvBkaQvmZgHfHtNEIajUsrrMPhRoMCqIEyKgCx' );
define( 'NONCE_KEY', 'IijXvgjiBxzHBpREPEraWfbgOsOZFhaTBRuVJLJOaFpZjAuNHcFeHoBTFPbYROXb' );
define( 'AUTH_SALT', 'oHNbGiflzpeNcvvsjAebciHlHVOyBETBiaQrEILNDfEyOngrvuFcBAWJBHXTeyRN' );
define( 'SECURE_AUTH_SALT', 'KByqhKqQKBLRcboPUrLsRaITObaaAZJEqSnoSRKsNhWaOUchIVZUujdNoaZYtWNz' );
define( 'LOGGED_IN_SALT', 'pMzpdceUUcLXBdgWqKjAkqQlZvpVOLCOyXdymXvdrfiJvxUKyAbstgCwpyizHqkb' );
define( 'NONCE_SALT', 'PdNsXdvTARPDQPSakaAXpIQlnIPSGpKExZCFFmWlZVLSdyeQBJkNlOyazEpSfTCa' );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
defined( 'ABSPATH' ) || define( 'ABSPATH', dirname( __FILE__ ) . '/' );

// Include for settings managed by ddev.
$ddev_settings = __DIR__ . '/wp-config-ddev.php';
if ( ! defined( 'DB_USER' ) && getenv( 'IS_DDEV_PROJECT' ) == 'true' && is_readable( $ddev_settings ) ) {
	require_once( $ddev_settings );
}

// Include for settings sourced from the container environment.
$container_settings = __DIR__ . '/wp-config-container.php';
if ( is_readable( $container_settings ) ) {
	require_once( $container_settings );
}

/** Include wp-settings.php */
if ( file_exists( ABSPATH . '/wp-settings.php' ) ) {
	require_once ABSPATH . '/wp-settings.php';
}
