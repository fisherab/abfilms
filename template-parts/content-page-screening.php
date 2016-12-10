<?php
/**
 * The template used for displaying page-screening content
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<header class="entry-header">
			<?php the_title( '<h1 class="entry-title">', ' <em> Cert: ' . get_field('certificate') .'</em></h1>' ); ?>
	</header><!-- .entry-header -->

	<?php twentysixteen_post_thumbnail(); ?>

	<div class="entry-content">
		<?php
		$time =  date_i18n('H:i', get_field('datetime'));

		echo '<em>' . date_i18n('M j, Y H:i', get_field('datetime')) . ' at ' . get_field('location'). '</em>';

		the_content();

		if (get_field('notes')) {
				echo '<h2>Programme Notes</h2>';
				echo get_field('notes');
		}

		if (get_field('comments')) {
				echo '<h2>Comments</h2>';
				echo get_field('comments');
				echo '<br/>';
				echo '<br/>';
				echo 'A:' . get_field('as') . ', ';
				echo 'B:' . get_field('bs') . ', ';
				echo 'C:' . get_field('cs') . ', ';
				echo 'D:' . get_field('ds') . ', ';
				echo 'E:' . get_field('es');
		}

		?>
	</div><!-- .entry-content -->

	<?php
		edit_post_link(
			sprintf(
				/* translators: %s: Name of current post */
				__( 'Edit<span class="screen-reader-text"> "%s"</span>', 'twentysixteen' ),
				get_the_title()
			),
			'<footer class="entry-footer"><span class="edit-link">',
			'</span></footer><!-- .entry-footer -->'
		);
	?>

</article><!-- #post-## -->
