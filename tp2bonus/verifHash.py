import argparse, os, time, json #import des modules systèmes

import checksum, checkRec #import des modules personnels

def dir_path(path): #fonction de vérification d'existence d'un répertoire
	if os.path.exists(path):
		return path
	else:
		return "Ce n'est pas un répertoire valide"
		exit

if __name__ == '__main__':
	tp1 = time.time()
	tp2 = 0
    #########################################
    #Mise en place du parser d'arguments et ajout de paramètre à utiliser au lancement du script
	parser = argparse.ArgumentParser(description="script de calcul de hash utilisant les binaires intégrés à Linux dans le répertoire /bin", conflict_handler='resolve')
	parser.add_argument("path", help='Dossier où sont contenus les fichiers', type=dir_path)
	parser.add_argument('-R','--recursive', dest='rec',action="store_true", required=False)
	parser.add_argument('-j', dest='fic', help="indiquer le chemin/nom du fichier sans l'extension .json", required=False)
	arg = parser.parse_args()
    ##########################################
	dictionnaire = {}
	if arg.rec == False:
		print("scritp exécuté dans le répertoire renseigné")
		dictionnaire = checksum.checksum(arg.path)
	else:
		print("script exécuté de façon récursive dans le répertoire et les sous-répertoires")
		dictionnaire = checkRec.checksum_recursif(arg.path)

    #si un nom de fichier est renseigné dans les arguments passés à la commande d'exécution
	if arg.fic:
		with open(f'{arg.fic}.json', "w") as fp:
			json.dump(dictionnaire, fp, indent=3)
		tp2 = time.time()
	else:
        #création d'un fichier ou réécriture dans un fichier présent fic.json
		with open("fic.json", 'w') as fp:
			json.dump(dictionnaire,fp, indent=3)
		tp2 = time.time()
	print(f"Le script s'est exécuté en {tp2 - tp1:.2F}s.") #affichage du temps d'exécution total du script
