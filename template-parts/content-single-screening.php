<?php
/**
 * The template part for displaying single-screening posts
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<header class="entry-header">
		<?php
		$tit = '';
    if (get_field('aka')) {
			$tit = $tit . ' <em>(' . get_field('aka') . ')</em>';
		}

		the_title( '<h1 class="entry-title">', $tit . '</h1>' ); ?>
	</header><!-- .entry-header -->

	<?php twentysixteen_excerpt(); ?>

	<?php twentysixteen_post_thumbnail(); ?>

	<div class="entry-content">
		<?php

			$tim =  date_i18n('H:i', get_field('datetime'));
			if ($tim == '00:00') {
				  $fmt = 'j/m/Y';
			} else {
				  $fmt = 'j/m/Y H:i';
			}

      if (get_field('location)')) {
				$loc = ' at ' . get_field('location');
			} else {
				$loc = '';
			}
			echo '<em>' . date_i18n($fmt, get_field('datetime')) . $loc . '.</em>';
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
					$votes = get_field('as') + get_field('bs') + get_field('cs') + get_field('ds') + get_field('es');
					if ($votes) {
						echo '<h2>Scores</h2>';
						echo 'A:' . get_field('as') . ', ';
						echo 'B:' . get_field('bs') . ', ';
						echo 'C:' . get_field('cs') . ', ';
						echo 'D:' . get_field('ds') . ', ';
						echo 'E:' . get_field('es');

						$num = (get_field('as')*100 + get_field('bs')*75 + get_field('cs')*50 +  get_field('ds') *25) / $votes;
						echo ' to give ' . round($num, 0) . '%';
						if (get_field('total')) {
					    echo ' from ' . round($votes*100/get_field('total'),1) . '% of those present.';
						}
				 }
			}

		?>
	</div><!-- .entry-content -->

	<footer class="entry-footer">
		<?php twentysixteen_entry_meta(); ?>
		<?php
			edit_post_link(
				sprintf(
					/* translators: %s: Name of current post */
					__( 'Edit<span class="screen-reader-text"> "%s"</span>', 'twentysixteen' ),
					get_the_title()
				),
				'<span class="edit-link">',
				'</span>'
			);
		?>
	</footer><!-- .entry-footer -->
</article><!-- #post-## -->
