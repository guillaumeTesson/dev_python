################################################################################
#script qui prend un fichier présent dans le dossier en paramètre et change l'utilisateur et les droits pour que seul root puisse y accéder 
################################################################################

import os, sys, subprocess

if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--help"):
	print("le programme doit s'exécuter de cette façon: su -- root -c 'python3 change_droit.py arg'")
else:
	if sys.argv[1] in os.listdir('/home/user/python/tp2/'): #si le fichier en paramètre est présent dans le dossier
		file = "/home/user/python/tp2/"+sys.argv[1]
		#changement d'utilisateur et de droits sur le fichier
		os.system(f"chown root:root {file}")
		os.system(f"chmod 0700 {file}")
		#utilisation de subprocess pour l'exécution de la commande : ls -ld example_file.txt
		result = subprocess.run(
			['ls', '-ld', file],
			capture_output = True,
			text = True
		)
		print(result.stdout)
	else:
		print("le fichier n'est pas présent")
