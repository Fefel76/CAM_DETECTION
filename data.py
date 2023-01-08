from detectionHumans import *
from run import init_config
import cv2
import sys

delai=1
boucle=5
rafale=2
if len(sys.argv) > 2:
    delai = int(sys.argv[2])

if len(sys.argv) > 3:
    boucle = int(sys.argv[3])

if len(sys.argv) > 4:
    rafale = int(sys.argv[4])

# initialisation de la caméra
src, name, visu, fps, record= init_config()


for t in range(boucle):
    cap, width, height = init_CAM(src=src, fps=fps, name=name)
    frame = read_frame(cap, name)
    photo(frame=frame, name=name)
    for i in range(int(fps)):  #lecture de 15 frames sans photo
        frame = read_frame(cap, name)
    frame = read_frame(cap, name)
    photo(frame=frame, name=name)
    cap.release()
    time.sleep(delai)


cv2.destroyAllWindows()