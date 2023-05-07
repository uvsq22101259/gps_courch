import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import json
import heapq

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("Createur de graph")
        self.image_path = askopenfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="black", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)
        
    

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.noeuds = []
        self.pistes = []
        self.chemins = []

        # Ajouter les noeuds sur le canvas
        for noeud in liste_noeuds:
            x, y = noeud.coord
            noeud_obj = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="red", outline="red", width=2, tags="noeud")
            self.noeuds.append(noeud)
            noeud.point = noeud_obj

        # Ajouter les pistes sur le canvas
        for piste in liste_pistes:
            x1, y1 = data.get_noeud(piste.depart.nom).coord
            x2, y2 = data.get_noeud(piste.fin.nom).coord
            piste_obj = self.canvas.create_line(x1, y1, x2, y2, fill=piste.couleur, width=5, tags="piste")
            self.pistes.append((piste.nom, piste_obj))
            piste.segment = piste_obj

        # Ajouter les chemins sur le canvas
        self.canvas.bind("<Button-1>", self.clic_droit)

    def find_noeud(self, x, y):
        """ retourne le noeud sur lequel on a cliqué, ou None si on n'a pas cliqué sur un noeud"""
        for noeud in self.noeuds:
            x1,y1,x2,y2= self.canvas.coords(noeud.point)
            if x1  < x <  x2 and y1  < y < y2:
                return noeud
        return None


    def clic_droit(self,event):
        """ gère le clic droit de la souris: si on a cliqué sur un noeud, on l'ajoute à la liste des chemins, sinon on affiche un message d'erreur"""
        if len(self.chemins) % 2 == 1 or len(self.chemins) == 0:
            x, y = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
            noeud = self.find_noeud(x, y)
            if noeud is not None:
                self.chemins.append(noeud)
            else:
                print("Aucun noeud trouvé")
        if len(self.chemins) % 2 == 0 and len(self.chemins) != 0:
            self.trajet()

    def trajet(self,):
        """ gère l'affichage du trajet entre deux noeuds"""
    
        a = self.chemins[0]
        b = self.chemins[1]
        self.dijkstra(a,b)
        
     





    def dijkstra(self, depart, arrivee):
        """Calcule le plus court chemin entre deux noeuds avec l'algorithme de Dijkstra"""

        # Initialisation
        if depart == arrivee:
            return "vous êtes déjà sur place"
        
        for noeud in self.noeuds:
            noeud.distance = float("inf")
            noeud.precedent = None
        
        for vois in depart.voisins:
            longueur = data.get_piste(depart, vois).longueur
            vois.distance = longueur
            vois.precedent = depart

        depart.distance = 0
        file = []
        
        # Boucle principale
        while True:
            self.noeuds.sort(key = lambda x: x.distance)
            noeud = self.noeuds.pop(0)
            file.append(noeud)
            if noeud == arrivee:
                print("Arrivée", noeud.precedent)
                break
            for vois in noeud.voisins:
                    
                    longueur = data.get_piste(noeud, vois).longueur
                    
                    if noeud.distance + longueur < vois.distance:
                        vois.distance = noeud.distance + longueur
                        vois.precedent = noeud
                        

        # Affichage du chemin
        noeud = arrivee

        while noeud.precedent is not None:
            
            self.canvas.itemconfig(noeud.point, fill="yellow", outline="yellow", width=4)
            piste = data.get_piste(noeud.precedent, noeud)
            
            self.canvas.itemconfig(piste.segment, fill="yellow", width=4 )
            print(piste.nom, piste.longueur)
            noeud = noeud.precedent
        self.canvas.itemconfig(noeud.point, fill="yellow", outline="yellow", width=4)
        for noeud in file:
            self.noeuds.append(noeud)
        self.chemins = []
        

        
       
        

    

file = json.load(open("data\data.json","r"))


class Noeuds ():
    def __init__(self, nom,coord, point = None ) -> None:
        self.nom = nom
        self.voisins = list()
        self.coord = coord
        self.point = point

    def __repr__(self) -> str:
        return self.nom

class Pistes():
    def __init__(self,nom, couleur, noeud_d, noeud_f, longueur, coords, segment = None) -> None:
        self.nom = nom
        self.couleur = couleur
        self.depart = noeud_d
        self.fin = noeud_f
        self.longueur = longueur
        self.coords = coords
        self.segment = segment
    def __repr__(self) -> str:
        return self.nom
    
class Data():
    def __init__(self, noeuds, pistes) -> None:
        self.noeuds = noeuds
        self.pistes = pistes
        for piste in self.pistes:
            piste.depart = self.get_noeud(piste.depart)
            piste.fin = self.get_noeud(piste.fin)
        for noeud in self.noeuds:
            self.voisin(noeud)

    
    def get_noeud(self, nom):
        for noeud in self.noeuds:
            if noeud.nom == nom:
                return noeud
        return None


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
    liste_noeuds.append(Noeuds(elem["name"],(elem["x"],elem["y"])))

liste_pistes = []
for elem in file["pistes"]:
    liste_pistes.append(Pistes(elem["name"], elem["couleur"], elem["noeud_depart"], elem["noeud_fin"], elem["longueur"], coords = elem["coords"]))
    
data = Data(liste_noeuds, liste_pistes)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
