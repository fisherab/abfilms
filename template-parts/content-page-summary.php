<li>
  <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
 <?php if (get_field('aka'))   {echo '(' . get_field('aka') . ') ';}
 echo ' - ' . date_i18n('j/m/Y', get_field('datetime'));
 if (get_field('as')) {

 $num = (get_field('as')*100 + get_field('bs')*75 + get_field('cs')*50 +  get_field('ds') *25) / (get_field('as') + get_field('bs') + get_field('cs') + get_field('ds') + get_field('es'));
 echo ' - Score:' . round($num, 1) . '%';
 }

 ?>

</li>
