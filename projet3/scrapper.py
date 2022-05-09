#################################################################
#script qui extrait des données publiques depuis un site Internet et les ajoute dans un fchier json
#################################################################

import requests

req = requests.get("https://www.frameip.com/liste-des-ports-tcp-udp/?plage=1")
with open("temp1.txt",'w', encoding='utf-8') as f:
    f.write(req.text)
#print(req.text)