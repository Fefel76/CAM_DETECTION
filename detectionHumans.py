import cv2
import os
import time
import logging
import pandas as pd
import smtplib

logging.basicConfig(filename='./log/detectionHumans.log',level=logging.DEBUG,format='%(asctime)s -- %(funcName)s -- %(process)d -- %(levelname)s -- %(message)s')

def scanCAM(src=0, name='CAM', width=320, height=240, fps=45, visu=False, record=False, freq_delay=0.3):
    """
    Scrute un flux vidéo pour réaliser une détection , enregistrer et visualiser
    :param src: 0 par défaut pour la webcam sinon adresse rstp://login:mdp@IP
    :param name: Nom de la caméra
    :param width: largeur de l'image => à réduire pour optimiser
    :param height: longueur de l'image
    :param fps: défilement de l'analyse doit être supérieur au FPS de la video
    :param visu: False par défaut, True pour afficher l'image
    :param freq_detect: analyse toutes les images à la fréquence indiquée
    :return: N/A
    """
    print("controle : src,  name,  visu, record == ", src, name, visu, record)
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

    if src != 0:
        cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
    else:
        cap= cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Erreur ouverture camera")
        exit()


    print('Images par secondes :', cap.get(cv2.CAP_PROP_FPS) , 'FPS par défaut versus', str(fps),  "FPS configuré")

    width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Taille (W,H): ",width,height)

    logging.info(name + " : Scan démarré ")

    t=time.time()  # compteur de trames
    alertes=pd.DataFrame(columns=("Time","Humains", "Visages")) # Historisation des detections pour remonter les alertes


    while True:

        # itération par image capturée
        try:
            ret, frame = cap.read()
            if not ret:
                logging.error(name + " : Erreur dans la lecture du stream..." + ret)
                break
        except:

            logging.error(name + " : Erreur de récupération du flux")
            break

        if time.time()-t>freq_delay:    # régulation des détections tous les freq_delay
            humains, visages = detection(frame)
            t = time.time()
            if (humains+visages)>0:
                #logging.info("Detection : "+humains+visages)
                if record:
                    photo(frame=frame, name=name)  # sauvegarde sur disque de la photo
                    #capture(cap=cap,frame=frame, name=name, t_capture=time.time(), fps=fps,width=width, height=height)

                a = pd.DataFrame({"Nom": [name], "ID": [time.time()], "Time": [time.strftime("%d/%m/%y %H:%M:%S")],"Humains": [humains], "Visages": [visages]})
                #alertes=pd.concat([a,alertes],ignore_index=True)

                a.to_csv('./videos/alertes_'+name+'.csv', mode='a', index=False, header=False, encoding='utf-8')


        # Display the resulting frame
        #if visu:
            #cv2.imshow('frame', frame)

        if cv2.waitKey(int(1000 / fps)) == ord('q'):
            break
    # When everything done, release the capture


    cap.release()
    cv2.destroyAllWindows()



def detection(frame,detections=0, face=False):
    """
    Analyse une image pour déterminer si il y a un corps
    :param frame: image à analyser
    :param detections: nombre d'humain détectés
    :param face: nombre de visage
    :return: nombre d'humains et visages
    """

    # Traitement de l'image récupérée
    t=time.time()
    frame, detections = detectionHOG(frame)  # detection HOG
    frame, face = detection_face_HAAS(frame)  # detection HAAS Face
    #print("Perf detection = ", time.time()-t, detections, face)

    return detections, face

def photo(frame,name):
    """

    :param frame: image à sauvegarder
    :param name: nom de la caméra
    :return:
    """
    file = "./videos/" + name + "_" + time.strftime("%d-%b-%Y_%HH%Mm%Ss") + '.jpg'
    try:
        cv2.imwrite(file, frame)
        logging.info(name + ": Enregistrement de la photo " + file)
    except:
        logging.error(name + ': Erreur pour ouvrir le fichier de sauvegarde')


def capture(cap, frame, name, t_capture, d_capture=1, width=640, height=480, fps=15):
    """
    Enregistre le flux vidéo pedant une durée déterminée
    :param cap: flux vidéo à enregistrer
    :param t_capture: début du temps de la vidéo
    :param d_capture: durée de la vidéo à enregistrer
    :return: True/False
    """
    file = "./videos/"+name+"_"+time.strftime("%d-%b-%Y_%HH%Mm%Ss") + '.mp4'

    try:
        writer = cv2.VideoWriter(file, fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=fps, frameSize=(int(width), int(height)))
    except:
        logging.error(name + ': Erreur pour ouvrir le fichier de sauvegarde')

    while (time.time()-t_capture<d_capture):
        writer.write(frame)


        # itération par image capturée
        try:
            ret, frame = cap.read()
            if not ret:
                logging.error(name + " : Erreur dans la lecture du stream...")
                break
        except:

            logging.error(name + " : Erreur de récupération du flux")
            break


    logging.info(name + ": Enregistrement de la vidéo " + file)

    try:
        writer.release()
        return True
    except:
        logging.error(name +':Erreur pour fermer le fichier de sauvegarde')
        return False

def detectionHOG(frame, winStride=(8,8), padding=(3,3), scale=1.21):
    """

    :param frame: image à analyser
    :return: image avec les rectangles de détection, nombre d'humains détectés
    """
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     #Optimisation de la détection
    winStride = (8, 8)
    padding = (4, 4)
    scale = 1.1

    (humans, _) = hog.detectMultiScale(gray,winStride=winStride,padding=padding,scale=scale)

    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)
    return frame, len(humans)


def detection_face_HAAS(frame):
    """

    :param frame: image à analyser
    :return: image avec les rectangles de détection, nb détection
    """
    faceCascade = cv2.CascadeClassifier('./IAModel/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=10, #5
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame, len(faces)

"""
def detection_body_HAAS(frame):
    classifier = cv2.CascadeClassifier('./IAModel/haarcascade_upperbody.xml')
    body = classifier.detectMultiScale(frame, 1.1, 8)
    for (x, y, w, h) in body:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

"""



