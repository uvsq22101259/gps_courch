import json

REQUEST = 2

path_in = "./data/data7.json"
path_out = "./data/data7_copy.json"


WRITE = True
with open(path_in, "r") as f:
        dico = json.load(f)


if REQUEST == 1: # pour partager aux autres

    for i in range(len(dico["pistes"])):
        for j in range(len(dico["pistes"][i]["coords"])):
            dico["pistes"][i]["coords"][j][0] /= 3600 # width
            dico["pistes"][i]["coords"][j][1] /= 3601 # height

    for i in range(len(dico["noeuds"])):
        dico["noeuds"][i]["x"] /= 3600 # width
        dico["noeuds"][i]["y"] /= 3601 # height


elif REQUEST == 2: # lissage + dup (pistes)

    changements = 1

    while changements > 0:
        pistes = []
        changements = 0
        for i in range(len(dico["pistes"])):
            try:
                nom = dico["pistes"][i]["name"]
                nommage_auto = nom[0] == "p" and int(nom[1:])
                if nommage_auto:
                    dico["pistes"][i]["name"] = "p"+str(i+1)
                else:
                    if nom in pistes:
                        dico["pistes"][i]["name"] = input(f"nouveau nom pour '{nom}' : ")
                        changements += 1
                    else:
                        pistes.append(nom)
            except:
                pass


if WRITE:
    with open(path_out, "w") as f:
        json.dump(dico, f, indent=2)