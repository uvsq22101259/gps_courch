import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import json

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

        # Ajouter les noeuds sur le canvas
        for noeud in liste_noeuds:
            x, y = noeud.coord
            noeud_obj = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="red", outline="white", width=2, tags="noeud")
            self.noeuds.append((noeud.nom, x, y, noeud_obj))

        # Ajouter les pistes sur le canvas
        for piste in liste_pistes:
            x1, y1 = data.get_noeud(piste.depart.nom).coord
            x2, y2 = data.get_noeud(piste.fin.nom).coord
            piste_obj = self.canvas.create_line(x1, y1, x2, y2, fill=piste.couleur, width=5, tags="piste")
            self.pistes.append((piste.nom, piste_obj))

        

    

file = json.load(open("data\data.json","r"))


class Noeuds ():
    def __init__(self, nom,coord ) -> None:
        self.nom = nom
        self.voisins = list()
        self.coord = coord

    def __repr__(self) -> str:
        return self.nom

class Pistes():
    def __init__(self,nom, couleur, noeud_d, noeud_f, longueur, coords) -> None:
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
    liste_noeuds.append(Noeuds(elem["name"],(elem["x"],elem["y"])))

liste_pistes = []
for elem in file["pistes"]:
    liste_pistes.append(Pistes(elem["name"], elem["couleur"], elem["noeud_depart"], elem["noeud_fin"], elem["longueur"], coords = elem["coords"]))
    
data = Data(liste_noeuds, liste_pistes)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
