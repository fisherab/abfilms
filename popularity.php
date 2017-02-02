<<?php
/**
 * Template Name: popularity
 */
 $paged = ( get_query_var('paged') ) ? get_query_var('paged') : 1;
 $post_per_page = 20;
 $offset = ($paged - 1)*$post_per_page;

 $sql="select SQL_CALC_FOUND_ROWS wp_posts.id AS a from wp_posts,
 (select num.pid, round(num.tot/denom.n) as score from
 (select pid , sum(tot) as tot from (select wp_postmeta.post_id as pid, wp_postmeta.meta_value*100 as tot from wp_postmeta where wp_postmeta.meta_key = 'as'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value*75 from wp_postmeta where wp_postmeta.meta_key = 'bs'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value*50 from wp_postmeta where wp_postmeta.meta_key = 'cs'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value*25 from wp_postmeta where wp_postmeta.meta_key = 'ds') as tot group by pid) as num,
 (select pid , sum(tot) as n from (select wp_postmeta.post_id as pid, wp_postmeta.meta_value as tot from wp_postmeta where wp_postmeta.meta_key = 'as'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value from wp_postmeta where wp_postmeta.meta_key = 'bs'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value from wp_postmeta where wp_postmeta.meta_key = 'cs'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value from wp_postmeta where wp_postmeta.meta_key = 'ds'
 union all select wp_postmeta.post_id, wp_postmeta.meta_value from wp_postmeta where wp_postmeta.meta_key = 'es') as n group by pid) as denom
 where num.pid = denom.pid)
 as meta where wp_posts.id = meta.pid and meta.score is not null order by meta.score desc LIMIT ".$offset.", ".$post_per_page;

 $sql_result = $wpdb->get_results( $sql, OBJECT);
 $sql_posts_total = $wpdb->get_var( "SELECT FOUND_ROWS()" );
 $max_num_pages = ceil($sql_posts_total / $post_per_page);

get_header(); ?>

<div id="primary" class="content-area">
	<main id="main" class="site-main" role="main">
    <header class="entry-header">
      <h1 class="entry-title">Past Screenings by Poularity</h1>
		<?php
    foreach ($sql_result as $row) {
        $post = get_post($row->a);
        get_template_part( 'template-parts/content', 'page-summary' );
    }
    custom_pagination($max_num_pages,"",$paged);
    ?>
    </header>

	</main><!-- .site-main -->

	<?php get_sidebar( 'content-bottom' ); ?>

</div><!-- .content-area -->

<?php get_sidebar(); ?>
<?php get_footer(); ?>
