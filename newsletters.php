<<?php
/**
 * Template Name: newsletters
 */
 $paged = ( get_query_var('paged') ) ? get_query_var('paged') : 1;
 $query_args = array(
  'posts_per_page' => 20,
  'paged'          => $paged,
 	'category_name'	 => 'newsletters',
 	'orderby'			   => 'date',
 	'order'				   => 'DESC',
 );

$the_query = new WP_Query($query_args);

get_header(); ?>

<div id="primary" class="content-area">
	<main id="main" class="site-main" role="main">
    <header class="entry-header">
      <h1 class="entry-title">Newsletters</h1>
		<?php
    while ( $the_query->have_posts() ) : $the_query->the_post();
      ?>
      <div class="entry-content>"
        <li>
          <a href="<?php the_permalink(); ?>"><?php the_date(); ?></a>
        </li>
      </div>
    <?php
		endwhile;
    custom_pagination($the_query->max_num_pages,"",$paged);
    ?>
    </header>

	</main><!-- .site-main -->

	<?php get_sidebar( 'content-bottom' ); ?>

</div><!-- .content-area -->

<?php get_sidebar(); ?>
<?php get_footer(); ?>
