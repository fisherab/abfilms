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
	     ),
	     'public' => true,
	     'has_archive' => true,
	     'rewrite' => array('slug' => 'screenings'),
             'register_meta_box_cb' => 'add_screening_metaboxes',
       )
       );
}

function add_screening_metaboxes() {
    add_meta_box('wpt_events_location', 'Location', 'wpt_screening_location', 'screening', 'side', 'default');
}

// The Screening Location Metabox
function wpt_screening_location() {
	 global $post;
	 
	 // Noncename needed to verify where the data originated
	 echo '<input type="hidden" name="eventmeta_noncename" id="eventmeta_noncename" value="' . 
	 wp_create_nonce( plugin_basename(__FILE__) ) . '" />';
	 
	 // Get the location data if its already been entered
	 $location = get_post_meta($post->ID, '_location', true);
	 
	 // Echo out the field
	 echo '<input type="text" name="_location" value="' . $location  . '" class="widefat" />';
}

// Save the Metabox Data
function wpt_save_events_meta($post_id, $post) {

         if( $post->post_type == 'revision' ) return; // Don't store custom data twice
	 
	 // verify this came from the our screen and with proper authorization,
	 // because save_post can be triggered at other times
	 if ( !wp_verify_nonce( $_POST['eventmeta_noncename'], plugin_basename(__FILE__) )) {
            return $post->ID;
	 }

	 // Is the user allowed to edit the post or page?
	 if ( !current_user_can( 'edit_post', $post->ID )) {
	    return $post->ID;
         }

	 $events_meta['_location'] = $_POST['_location'];
	       
	 foreach ($events_meta as $key => $value) {
	        $value = implode(',', (array)$value); 
	     	if(get_post_meta($post->ID, $key, FALSE)) {
	           update_post_meta($post->ID, $key, $value);
	        } else {
                   add_post_meta($post->ID, $key, $value);
 	        }
		if(!$value) delete_post_meta($post->ID, $key);
         }
}

add_action('save_post', 'wpt_save_events_meta', 1, 2); // save the custom fields

// Hooking up our function to theme setup
add_action( 'init', 'create_posttype' );
?>