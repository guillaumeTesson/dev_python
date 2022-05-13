import os, subprocess

#fonction de checksum qui parcourt les sous-répertoires en vue de récupérer les fichiers
def checksum_recursif(path):
	method = [ x for x in os.listdir('/bin') if x.endswith("sum") and x != "sum" and not x.startswith("inno")] # récupération des binaires finissant par sum
	#dictionnaire contenant le chemin vers le binaire associé à une méthode de checksum
	dict_method = {}
	for i in method:
		dict_method[i] = os.path.join("/bin",i)
	#########################################
	#création du dictionnaire contenant le nom d'un fichier
	dict_fic = {}
	#########################################
	#test d'un argument passé dans la ligne de commande et que le dossier existe
	fic = []
	for root, dirs, files in os.walk(path):
		for name in files:
			fic.append(os.path.join(root,name))
		for d in dirs:
			pass
	########################################
	#utilisation du dictionnaire avec les méthodes pour créer la commande de checksum
	for i in fic:
		dict_hash = {}
		for j in dict_method:
			cm = [dict_method[j], i]
			#création du subprocess qui va exécuter la commande et récupérer la valeur retour
			res = subprocess.run(
				cm,
				capture_output=True,
				text=True)
			dict_hash[j] = res.stdout.split()[0]
		dict_fic[i] = dict_hash

	return dict_fic
