# Draw-



Instructions élémentaires : 

Créer un curseur : 
create_cursor -> create_cursor C at x , y
      exemple : create_cursor C1 at 10,15    
      (Créer un curseur nommé C1 au point d'abcisse 10 et d'ordonnée 15)

Montrer un curseur : 
show_cursor -> show_cursor C => par défaut le curseur est visible
      exemple : show_cursor C1
      (Montrer le curseur C1)

Cacher un curseur : 
hide_cursor -> hide_cursor C 
      exemple : hide_cursor C1
      (Cacher le curseur C1)

Changer la couleur du curseur :
color_cursor -> color_cursor C to R,G,B
      ewemple : color_cursor C1 to 255,0,0
      (Changer la couleur du curseur C1 en rouge)

Changer l'épaisseur du curseur : 
thickness_cursor -> thickness_cursor C to (au choix 1,2,3,4,5) => les épaisseurs sont prédéfinies
    exemple : thickness_cursor C1 to 4
    (Changer l'épaisseur du curseur C1 pour l'épaisseur 4) 

Faire avancer un curseur (saut) :
move_cursor -> move_cursor C at x , y
      exemple : move_cursor C1 at 15,10
      (Déplacer le curseur C1 au point d'abcisse 15 et d'ordonnée 10)

Faire pivoter un curseur : 
rotate_cursor -> rotate_cursor C to x => par défaut le curseur pointe vers le haut et va pivoter vers la droite
      exemple : rotate_cursor C1 to 90
      (Faire pivoter le curseur C1 de 90 degrés)

Dessiner une ligne : 
draw_line -> C draw_line x
      exemple : C1 draw_line 20
      (A partir du curseur C1 dessiner une ligne de 20 pixels)

Dessiner un rectangle : 
draw_rectangle -> C draw_rectangle x,y => par défaut les angles se feront vers la droite
      exemple : C1 draw_rectangle 20,15
      (A partir du curseur C1 dessiner un rectangle de longueur 20 pixels et de largeur 15 pixels)

Dessiner un carré : 
draw_square -> C draw_square x => par défaut les angles se feront vers la droite
      exemple : C1 draw_square 20
      (A partir du curseur C1 dessiner un carré de coté 20 pixels)

Dessiner un cercle : 
draw_circle -> C draw_circle x
      exemple : C1 draw_circle 20
      (A partir du curseur C1 dessiner un cercle de rayon 20 pixels)

Dessiner un arc : 
draw_arc -> C draw_arc x , y / a , b 
      exemple : C1 draw_arc 10,15 / 15,10 
      (A partir du curseur C1 dessiner un arc de cercle qui ira du point d'abcisse 10 et d'ordonnée 15 jusqu'au point d'abcisse 15 et d'ordonnée 10)

Dessiner une ellipse : 
draw_ellipse -> draw_ellipse x , y
      exemple : C1 draw_ellipse 10,15
