<<?php
/**
 * Template Name: past-by-date
 */
 $paged = ( get_query_var('paged') ) ? get_query_var('paged') : 1;
 $query_args = array(
  'posts_per_page' => 30,
  'paged'          => $paged,
 	'post_type'			 => 'screening',
 	'meta_key'			 => 'datetime',
 	'orderby'			   => 'meta_value_num',
 	'order'				   => 'DESC',
 	'meta_query' => array(
 		'key' => 'datetime',
 		'type' => 'numeric',
 		'value' => current_time('timestamp'),
 		'compare' => '<',
 	),
 );

$the_query = new WP_Query($query_args);

get_header(); ?>

<div id="primary" class="content-area">
	<main id="main" class="site-main" role="main">
		<?php
		// Start the loop.
    while ( $the_query->have_posts() ) : $the_query->the_post();
    get_template_part( 'template-parts/content', 'page-summary' );
		// End of the loop.
		endwhile;

		?>
<?php if ($the_query->max_num_pages > 1) { // check if the max number of pages is greater than 1  ?>
  <nav class="prev-next-posts">
    <div class="prev-posts-link">
      <?php echo get_next_posts_link( 'Older screenings', $the_query->max_num_pages ); // display older posts link ?>
    </div>
    <div class="next-posts-link">
      <?php echo get_previous_posts_link( 'Newer screenings' ); // display newer posts link ?>
    </div>
  </nav>
<?php } ?>

	</main><!-- .site-main -->

	<?php get_sidebar( 'content-bottom' ); ?>

</div><!-- .content-area -->

<?php get_sidebar(); ?>
<?php get_footer(); ?>
