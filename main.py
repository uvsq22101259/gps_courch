import json
import heapq

file = json.load(open("data\data_final.json","r"))


class Noeuds ():
    def __init__(self, nom, ) -> None:
        self.nom = nom
        self.voisins = list()

    def __repr__(self) -> str:
        return self.nom

class Pistes():
    def __init__(self,nom, couleur, noeud_d, noeud_f, longueur) -> None:
        self.nom = nom
        self.couleur = couleur
        self.depart = noeud_d
        self.fin = noeud_f
        self.longueur = longueur
    
    def __repr__(self) -> str:
        return self.nom
    
class Data():
    def __init__(self, noeuds, pistes) -> None:
        self.noeuds = noeuds
        self.pistes = pistes
        for piste in self.pistes:
            piste.depart = self.get_noeud(piste.depart)
            piste.fin = self.get_noeud(piste.fin)

    
    def get_noeud(self, nom):
        for noeud in self.noeuds:
            if noeud.nom == nom:
                return noeud
        return None

    def djikstra(self, a, b):
        pass

    def get_piste(self, a, b):
        for piste in self.pistes:
            if piste.depart == a and piste.fin == b:
                return piste
        return None
    
    def voisin(self, noeud):
        for piste in self.pistes:
            if piste.depart == noeud:
                noeud.voisins.append(piste.fin)


liste_noeuds = []
for elem in file["noeuds"]:
    liste_noeuds.append(Noeuds(elem["name"]))

liste_pistes = []
for elem in file["pistes"]:
    liste_pistes.append(Pistes(elem["name"], elem["couleur"], elem["noeud_depart"], elem["noeud_fin"], elem["longueur"]))
    
data = Data(liste_noeuds, liste_pistes)

for noeuds in data.noeuds:
    print(data.voisin(noeuds), noeuds.nom, noeuds.voisins)
   

data.djikstra("CREUX", "haut Pyramides")