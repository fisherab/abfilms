<?php
/**
 * Template Name: future
 */
 $paged = ( get_query_var('page') ) ? get_query_var('page') : 1;
 $query_args = array(
  'posts_per_page' => 3,
  'paged'          => $paged,
 	'post_type'			 => 'screening',
 	'meta_key'			 => 'datetime',
 	'orderby'			   => 'meta_value_num',
 	'order'				   => 'ASC',
 	'meta_query' => array(
 		'key' => 'datetime',
 		'type' => 'numeric',
 		'value' => current_time('timestamp'),
 		'compare' => '>',
 	),
 );

$the_query = new WP_Query($query_args);

get_header(); ?>

<div id="primary" class="content-area">
	<main id="main" class="site-main" role="main">
      <h1>Future Screenings</h1>
      <?php
      while ( $the_query->have_posts() ) :
        $the_query->the_post();
        get_template_part( 'template-parts/content', 'page-screening' );
      endwhile;
      custom_pagination($the_query->max_num_pages,"",$paged);
      ?>

	</main><!-- .site-main -->

	<?php get_sidebar( 'content-bottom' ); ?>

</div><!-- .content-area -->

<?php get_sidebar(); ?>
<?php get_footer(); ?>
