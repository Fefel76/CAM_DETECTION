import pickle
import sys

if len(sys.argv) > 1:  # récup de l'argument pour selectionner la caméra (config du fichier)
    commande = sys.argv[1]

    if commande == 'on':
        pickle.dump("True", open("./videos/record.txt", "wb"))
    if commande == 'off':
        pickle.dump("False", open("./videos/record.txt", "wb"))

    print("Commande reçu:", commande)