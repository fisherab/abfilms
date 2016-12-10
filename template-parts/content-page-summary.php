<li>
  <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a><em>
 <?php if (get_field('aka'))   {echo '(' . get_field('aka') . ') ';}
 echo date_i18n('M j, Y', get_field('datetime'));	?>
</em>
</li>
