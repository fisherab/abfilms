<?php
/**
 * Template Name: fred
 */
$posts = get_posts(array(
	'posts_per_page'	=> -1,
	'post_type'			=> 'screening'
));

if( $posts ): ?>

	<ul>

	<?php foreach( $posts as $post ):

		setup_postdata( $post )

		?>
		<li>
			<a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
		</li>

	<?php endforeach; ?>

	</ul>

	<?php wp_reset_postdata(); ?>

<?php endif; ?>
