<H2> Fichier de configuration </H2> 

JSON avec clé le nom de la cam et valeur l'URL

<H2> Lancement du programe </H2> 
Lancement du main avec en argument le nom de la cam
Plusieurs param de lancement  (avec ou sans visu, record)

<H2> Algorithme </H2> 
2 algo Machine Learning utilisés HOG pour détecter le corps humain et HAAS Cascade pour le visage humain

Stockage des detections dans dataframe avec colonnes (Time, Nom de la cam, type de détections)

Capture des vidéos dès detections dans <i>/videos </i>