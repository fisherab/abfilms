<<?php
/**
 * Template Name: future
 */
 $posts = get_posts(array(
 	'posts_per_page'	=> -1,
 	'post_type'			=> 'screening',
 	'meta_key'			=> 'datetime',
 	'orderby'			  => 'meta_value_num',
 	'order'				  => 'DESC',
 	'meta_query' => array(
 		'key' => 'datetime',
 		'type' => 'numeric',
 		'value' => current_time('timestamp'),
 		'compare' => '<',
 	),
 ));

get_header(); ?>

<div id="primary" class="content-area">
	<main id="main" class="site-main" role="main">
		<?php
		// Start the loop.
		foreach( $posts as $post ):
			setup_postdata( $post );

			// Include the page content template.
			get_template_part( 'template-parts/content', 'page-screening' );

			// End of the loop.
		endforeach;

		wp_reset_postdata();
		?>

	</main><!-- .site-main -->

	<?php get_sidebar( 'content-bottom' ); ?>

</div><!-- .content-area -->

<?php get_sidebar(); ?>
<?php get_footer(); ?>
