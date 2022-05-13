"""
script qui va extraire les informations d'un fichier de log apache et les intégrer dans un fichier json
"""
# importation des librairies re, json
import re, json

#création du dictionnaire final contenant les informations finales:
#- adresse IP en clé
#- code retour et le nombre de fois trouvé contenu dans un petit dictionnaire
dict_fin = dict()

#ouverture du fichier de log en lecture
with open("access.log", 'r') as f:
    text = f.read()

##\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} => ((?:\d{1,3}\.){3}\d{1,3})
#création de la regex pour récupérer l'adresse IP et le code retour HTTP
reg = re.compile(r"((?:\d{1,3}\.){3}\d{1,3}).+\" (\d{3}) ")
#recherche de la regex sur le fichier access.log
res = reg.findall(text)

#création d'un dictionnaire temporaire avec les adresses IP en clé
#et une liste contenant les codes retours
dict_aux = {}
#parcours de l'ensemble des listes trouvées
for i in res:
    ip = i[0]
    #création de la liste des codes retour
    ip1 = [j[1] for j in res if ip in j]
    dict_aux[ip]= ip1

#parcours du dictionnaire temporaire
for key in dict_aux.keys():
    d = dict() #dictionnaire de comptage des codes retour
    #parcours de la valeur associé à la key
    for i in dict_aux[key]:
        #test conditionnel permettant de compter les codes retour
        if i not in d:
            d[i] = 1
        else:
            d[i] += 1
    #affectation du dictionnaire valeur pour l'adresse IP en clé
    dict_fin[key]=d

#création du fichier json final

with open("ip.json", "w") as fp:
  json.dump(dict_fin, fp , indent = 4)