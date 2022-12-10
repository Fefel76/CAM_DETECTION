<H2> Fichier de configuration </H2> 
Créer un fichier cam.conf pour précier l'URL RSTP
JSON avec clé le nom de la cam et valeur l'URL


 # Variable d'environnement
    'CAM_VISU' : True affiche la vidéo
    'CAM_RECORD': True enregistre la vidéo si detection

<H2> Lancement du programe </H2> 
Lancement du run.py avec en argument le nom de la cam
1 script - 1 cam
==> cf fichier Dockerfile
<h3>BUILD IMAGE et VOLUME</h3>
sudo docker build http://github.com/Fefel76/reconnaissanceVideo.git -t recolog --no-cache
sudo docker volume create videos  
sudo docker volume create log
<h3>RUN CONTAINER</h3>
sudo docker run -e pwd -v videos:/videos -v log:/log -d --restart=unless-stopped recolog 

<H2> Algorithme </H2> 
2 algo Machine Learning utilisés HOG pour détecter le corps humain et HAAS Cascade pour le visage humain

Stockage des detections dans dataframe avec colonnes (Time, Nom de la cam, type de détections)

Capture des vidéos dès detections dans <i>/videos </i>