#################################################################
#script qui extrait des données publiques depuis le site de FrameIP sur les ports TCP UDP et les ajoute dans un fchier json
#################################################################

import requests, re, json
from bs4 import BeautifulSoup

# Pour le script, il sera nécessaire d'utiliser 3 dictionnaires
# dictionnaire final (niv0) pour l'injection dans le json comprenant :
# - clé : num_port 
# - valeur : un dictionnaire pour renseigner les protocoles 
# dictionnaire protocole (niv1) comprenant :
# - clé : le protocole (TCP ou UDP)
# - valeur : un dictionnaire de renseignement
# dictionnaire renseignement (niv2) comprement :
# - clé : nom du service
# - valeur : description associée
dictFinal = {}

###################################################
titre = "<title>(.+)<\/title>"
bloc = "<li>.+<\/li>"

regBloc = re.compile(bloc)
regTitle = re.compile(titre)
req = requests.get("https://www.frameip.com/liste-des-ports-tcp-udp/")
resBloc = regBloc.findall(req.text)
resTitre = regTitle.findall(req.text)
print(resTitre[0])

addr = resTitre[0]
addr = addr.split('-')[0]
addr = addr[:-1].replace(" ","-")

address = "\w{4,5}\:\/\/.+"+addr+".plage\=\d"
regADDR = re.compile(address,re.IGNORECASE)
regSujet = re.compile(".+>(.+)<\/a.+")

#boucle itérative qui récupère l'adresse d'une page et le sujet abordé
for b in resBloc:
    resADDR = regADDR.findall(b)
    resSujet = regSujet.findall(b)
    print("adresse trouvée :",resADDR[0])
    print("sujet :", resSujet[0])

    #parcours de la page à l'adresse dans la variable resADDR[0]
    req1 =  requests.get(resADDR[0])
    soup = BeautifulSoup(req1.content,"html.parser")
    tableau = soup.find('table') #récupération du tableau de la page contenu entre les balises html <table> et </html>
    ligne = tableau.find_all('tr') # récupération séparées des lignes du tableau 

#regex pour la recherche du numéro de port, du protocole, du service et de la description du service 
    regPort = re.compile('.+>(\d+).+')
    regProtocol = re.compile('.+>(TCP|UDP).+')
    regNom = re.compile('[A-Za-z0-9\-]+')
    regDesc = re.compile('[A-Za-z0-9 ]+')

#boucle de remplissage des dictionnaires
    for i in ligne[1:] :
        #récupération des balises de paragraphe contenu dans une ligne du tableau
        paras = i.find_all('p')
        nom = regNom.findall(str(paras[0].string))[0]
        numPort = regPort.findall(str(paras[1]))[0]
        prot = regProtocol.findall(str(paras[2]))[0]
        description = regDesc.findall(str(paras[-1].string))[0]
        #test de vérification d'une entrée pour le numéro de port et initialisation des dictionnaires internes
        if numPort in dictFinal:
            dict1 = dictFinal[numPort]
        else:
            dict1 = {}
        if prot in dict1:
            dict2 = dict1[prot]
        else:
            dict2 = {}
        dict2[nom] = description
        dict1[prot] = dict2
        dictFinal[numPort] = dict1

#        print(f"Le port n°\033[1m{resPort}\033[0m a comme service associé \033[1m{nom}\033[0m sur le protocole \033[1m{prot}\033[0m. Sa description est \033[1m{description}\033[0m.")


#enregistrement dur dictionnaire final dans le fichier json
with open("port.json", "w") as fp:
    json.dump(dictFinal, fp, indent=2)