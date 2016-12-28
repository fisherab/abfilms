<?php
/**
 * The template used for displaying page-screening content
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<header class="entry-header">
			<?php
			$tit = '';
			if (get_field('aka')) {
				$tit = $tit . ' <em>(' . get_field('aka') . ')</em>';
			}

			the_title( '<h2 class="entry-title">', $tit . '</h2>' ); ?>

	</header><!-- .entry-header -->

	<?php twentysixteen_post_thumbnail(); ?>

	<div class="entry-content">
		<?php
		$tim =  date_i18n('H:i', get_field('datetime'));
		if ($tim == '00:00') {
				$fmt = 'j/m/Y';
		} else {
				$fmt = 'j/m/Y H:i';
		}

		echo '<em>' . date_i18n($fmt, get_field('datetime')) . ' at ' . get_field('location') . '.</em>';
		if (get_field('certificate')) {
			echo '<br/>Cert ' . get_field('certificate');
		}

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
