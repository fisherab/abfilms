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
    register_post_type('screening',
    // CPT Options
          array(
	           'labels' => array(
     		        'name' => __( 'Screenings' ),
      	        'singular_name' => __( 'Screening' ),
                'edit_item' => __('Edit Screening'),
                'view_item' => __('View Screening'),
                'add_new_item' => __('Add New Screening'),
	             ),
	           'public' => true,
	           'has_archive' => true,
	           'rewrite' => array('slug' => 'screenings'),
           )
       );
}

// Hooking up our function to theme setup
add_action( 'init', 'create_posttype' );
?>
