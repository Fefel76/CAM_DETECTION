from detectionHumans import *
from run import init_config
import cv2
import sys

delai=1
boucle=5
if len(sys.argv) > 2:
    delai = int(sys.argv[2])

if len(sys.argv) > 3:
    boucle = int(sys.argv[3])

# initialisation de la caméra
src, name, visu, fps, record= init_config()
cap, width, height = init_CAM(src=src, fps=fps, name=name)

for t in range(boucle):
    frame = read_frame(cap,name)
    photo(frame=frame, name=name)
    time.sleep(delai)


cap.release()
cv2.destroyAllWindows()