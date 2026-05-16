<?php
$settings = get_option( 'scolta_settings', [] );
$settings['sortable_fields'] = [ 'price', 'date' ];
$settings['sortable_field_descriptions'] = [
	'price' => 'Product price in USD',
	'date'  => 'Product listing date',
];
update_option( 'scolta_settings', $settings );
