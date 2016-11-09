<?php
function abcd_enqueue_styles() {

    $parent_style = 'parent-style'; // This is 'twentysixteen-style' for the Twenty Sixteen theme.

    wp_enqueue_style( $parent_style, get_template_directory_uri() . '/style.css' );
    wp_enqueue_style( 'child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array( $parent_style ),
        wp_get_theme()->get('Version')
    );
}
add_action( 'wp_enqueue_scripts', 'abcd_enqueue_styles' );

// Our custom post type function
function create_posttype() {
    register_post_type( 'movies',
    // CPT Options
        array(
	    'labels' => array(
	     		'name' => __( 'Movies' ),
	      	      'singular_name' => __( 'Movie' )
	      	 ),
		'public' => true,
	    'has_archive' => true,
	    'rewrite' => array('slug' => 'movies'),
														     	       )
															       );
}
// Hooking up our function to theme setup
add_action( 'init', 'create_posttype' );
?>