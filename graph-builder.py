import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
from math import atan2, cos, sin, sqrt
import json


def draw_arrow(canvas:tk.Canvas, x1, y1, x2, y2, couleur:str):
        # Dessiner une flèche isocèle entre les points (x1, y1) et (x2, y2)
        arrow_width = 5
        arrow_length = 10
        dx = x2 - x1
        dy = y2 - y1
        angle = atan2(dy, dx)
        x3 = x2 - arrow_length * cos(angle)
        y3 = y2 - arrow_length * sin(angle)
        x4 = x3 + arrow_width * sin(angle)
        y4 = y3 - arrow_width * cos(angle)
        x5 = x3 - arrow_width * sin(angle)
        y5 = y3 + arrow_width * cos(angle)
        id_line = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=5, fill=couleur)
        id_poly = canvas.create_polygon(x2, y2, x4, y4, x5, y5, fill=couleur)
        return id_line, id_poly


class Noeud():
    nombre_noeuds = 0
    names = []
    def __init__(self, x, y, name:str):
        Noeud.nombre_noeuds += 1
        self.x = x
        self.y = y
        self.name = name
        Noeud.names.append(name)
        self.sorties = []
        self.entrees = []
    
    def descriptor(self):
        """renvoi un dictionnaire decrivant le noeud"""
        dico = {}
        dico["name"] = self.name
        dico["x"] = self.x
        dico["y"] = self.y
        return dico
    
    def add_sortie(self, piste:"Piste"):
        self.sorties.append(piste)

    def add_entree(self, piste:"Piste"):
        self.entrees.append(piste)
    
    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        self.canvas_id.append(canvas.create_oval(self.x-7, self.y-7, self.x+7, self.y+7, fill="#ff00ff", activefill="yellow"))
        self.canvas_id.append(canvas.create_text(self.x, self.y-15, text=self.name, font=("Arial", 10)))
    
    def __str__(self) -> str:
        output = "\n#<"+self.name + ">#\nSorties :\n"
        for piste in self.sorties:
            output += piste.__str__()
        output += "\nEntrées :\n"
        for piste in self.entrees:
            output += piste.__str__()
        return output


class Piste():
    nombre_pistes = 0
    names = []
    def __init__(self, noeud_depart:Noeud, couleur:str):
        Piste.nombre_pistes += 1
        self.noeud_depart = noeud_depart
        self.couleur = couleur
        self.noeud_fin = None
        self.coords = [(self.noeud_depart.x, self.noeud_depart.y)]
        self.canvas_id = []
        self.longueur = 0
        self.name = None
    
    def set_name(self, name):
        self.name = name
        Piste.names.append(name)

    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        for i in range(1, len(self.coords)):
            x1, y1 = self.coords[i-1]
            x2, y2 = self.coords[i]
            self.canvas_id.append(draw_arrow(canvas, x1, y1, x2, y2, self.couleur))
    
    def descriptor(self):
        dico = {}
        dico["name"] = self.name
        dico["couleur"] = self.couleur
        dico["noeud_depart"] = self.noeud_depart.name
        dico["noeud_fin"] = self.noeud_fin.name
        dico["longueur"] = self.longueur
        dico["coords"] = self.coords
        return dico
    
    def add_chemin(self, xy:tuple, canvas:tk.Canvas):
        self.coords.append(xy)
        self.canvas_id.append(draw_arrow(canvas, self.coords[-2][0], self.coords[-2][1], self.coords[-1][0], self.coords[-1][1], self.couleur))
        self.longueur += int(sqrt((self.coords[-1][0] - self.coords[-2][0]) ** 2 + (self.coords[-1][1] - self.coords[-2][1]) ** 2))
    
    def rm_chemin(self, canvas:tk.Canvas):
        id1, id2 = self.canvas_id[-1]
        canvas.delete(id1)
        canvas.delete(id2)
        self.longueur -= int(sqrt((self.coords[-1][0] - self.coords[-2][0]) ** 2 + (self.coords[-1][1] - self.coords[-2][1]) ** 2))
        del self.coords[-1]
        del self.canvas_id[-1]
    
    def set_noeud_fin(self, noeud_fin:Noeud, canvas:tk.Canvas):
        self.noeud_fin = noeud_fin
        self.coords.append((self.noeud_fin.x, self.noeud_fin.y))
        self.canvas_id.append(draw_arrow(canvas, self.coords[-2][0], self.coords[-2][1], self.coords[-1][0], self.coords[-1][1], self.couleur))
        self.longueur += int(sqrt((self.coords[-1][0] - self.coords[-2][0]) ** 2 + (self.coords[-1][1] - self.coords[-2][1]) ** 2))
        self.noeud_depart.add_sortie(self)
        self.noeud_fin.add_entree(self)
    
    def __str__(self) -> str:
        if self.couleur != "yellow":
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' < nom_piste : {self.name}, difficulté : {self.couleur}, longueur : {self.longueur} >\n"
        else:
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' via remontée {self.name} de longueur {self.longueur}\n"


class App():
    def __init__(self, root: tk.Tk):
        self.noeuds = []
        self.pistes = []
        self.diff = "green" # attribu automatique de la difficulté de la piste (en cours)
        self.historique = [] # utile dans le câdre de la fonction undo (en cours)
        # 0 = placement noeud; 1 = draw_piste; 2 = piste
        self.mode = "noeud" # mode d'édition par défaut

        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("Createur de graph")
        self.image_path = askopenfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="black", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import JSON", command=self.import_json)
        file_menu.add_command(label="Export JSON", command=self.export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menu_bar.add_cascade(label="Settings", menu=file_menu)
        menu_bar.add_command(label="Undo", command=self.undo)
        menu_bar.add_command(label="Print", command=self.print)

        # Ajouter des barres de défilement
        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Binding de différentes actions utilisateur
        self.canvas.bind("<Button-1>", self.left_clic)
        self.root.bind("<d>", self.set_diff)
        self.canvas.bind("<Motion>", self.canvas_cursor)
        self.canvas.bind("<Control-Button-1>", self.left_clic_ctrl)
    
    def print(self):
        for noeud in self.noeuds:
            print(noeud)
    
    def left_clic_ctrl(self, event):
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        if self.mode == "noeud":
            self.rm_noeud(self.overlapping(cursor), False)

    def canvas_cursor(self, event):
        self.root.config(cursor="crosshair")
    
    def left_clic(self, event):
        """left_clic a différent comportement selon la valeur que prend self.mode"""
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        noeud = self.overlapping(cursor)
        if self.mode == "noeud":
            if noeud != None:
                # Mode piste !
                print(f"Mode de selection en cours de developpement <{noeud.name}>")
                self.canvas.itemconfigure(noeud.canvas_id[0], fill="orange")
                self.mode = "piste"
                self.pistes.append(Piste(noeud, self.diff))
            else: 
                # Création de noeuds !
                nom_noeud = ""
                while nom_noeud in Noeud.names or nom_noeud == "":
                    nom_noeud = askstring(f"Noeud nommé n°{Noeud.nombre_noeuds+1}", "Saisir nom")
                    if nom_noeud == "":
                        nom_noeud = "n"+str(Noeud.nombre_noeuds+1)
                if nom_noeud != None:
                    self.noeuds.append(Noeud(cursor[0], cursor[1], nom_noeud))
                    self.noeuds[-1].show(self.canvas)
                    self.historique.append(0)
        elif self.mode == "piste":
            if noeud == None:
                self.pistes[-1].add_chemin(cursor, self.canvas)
                self.historique.append(1)
            elif noeud == self.pistes[-1].noeud_depart:
                self.rm_piste(self.pistes[-1], False)
                while self.historique[-1] == 1:
                    del self.historique[-1]
                self.canvas.itemconfigure(noeud.canvas_id[0], fill="#ff00ff")
                self.mode = "noeud"
            else:
                self.pistes[-1].set_noeud_fin(noeud, self.canvas)
                nom_piste = ""
                while nom_piste in Piste.names or nom_piste == "":
                    nom_piste = askstring(f"Piste n°{Piste.nombre_pistes}", "Saisir nom")
                    if nom_piste == "":
                        nom_piste = "p"+str(Piste.nombre_pistes)
                self.pistes[-1].set_name(nom_piste)
                self.canvas.itemconfigure(self.pistes[-1].noeud_depart.canvas_id[0], fill="#ff00ff")
                self.mode = "noeud"
                self.historique.append(2)


    def overlapping(self, xy:tuple):
        """Regarde si le curseur est sur un noeud/..."""
        if self.mode == "noeud" or self.mode == "piste": # cas ou xy correspond au coordonnées du curseur utilisateur
            for noeud in self.noeuds:
                if 0 <= abs(noeud.x-xy[0]) <= 15 and 0 <= abs(noeud.y-xy[1]) <= 15:
                    return noeud
        return None
    
    def set_diff(self, _=None):
        """Permet de définir la difficulté des pistes créées"""
        self.diff = askstring("Choisir difficulté","green/blue/red/black/yellow")
    
    def rm_piste(self, p:Piste|int, deleted:bool=True):
        """Prend la piste ou son indice dans self.pistes
        puis l'efface du canvas et de la data"""
        if type(p) == int:
            p = self.pistes[p]
        for (id1, id2) in p.canvas_id:
            self.canvas.delete(id1)
            self.canvas.delete(id2)
        if not deleted:
            for i in range(len(self.pistes)):
                if self.pistes[i] == p:
                    del self.pistes[i]
                    Piste.nombre_pistes -= 1
                    break

    def rm_noeud(self, noeud:Noeud, deleted:bool=True):
        if type(noeud) == Noeud:
            offset = 0
            for i in range(len(self.pistes)):
                i -= offset
                if noeud == self.pistes[i].noeud_depart or noeud == self.pistes[i].noeud_fin:
                    self.rm_piste(self.pistes[i], False)
                    offset += 1
            for canvas_id in noeud.canvas_id:
                self.canvas.delete(canvas_id)
            if not deleted:
                for i in range(len(self.noeuds)):
                    if noeud == self.noeuds[i]:
                        del self.noeuds[i]
                        Noeud.nombre_noeuds -= 1
                        break

    def undo(self):
        """Fonction de retour arrière (à approfondir)"""
        if len(self.historique) > 0:
            action = self.historique.pop()
            if self.mode == "noeud":
                if action == 0: # undo noeud
                    self.rm_noeud(self.noeuds.pop())
                elif action == 2: # undo piste
                    self.rm_piste(self.pistes.pop())
                    while self.historique[-1] == 1:
                        del self.historique[-1]
            elif self.mode == "piste":
                if action == 1: # undo draw piste
                    self.pistes[-1].rm_chemin(self.canvas)
    
    def export_json(self):
        """exporte tout le contexte de la session courante"""
        dico = {"noeuds":[],"pistes":[]}
        for noeud in self.noeuds:
            dico["noeuds"].append(noeud.descriptor())
        for piste in self.pistes:
            dico["pistes"].append(piste.descriptor())
        dico["details"] = {"canvas_width":self.image.width,
                           "canvas_height":self.image.height,
                           "nombre_noeuds":Noeud.nombre_noeuds,
                           "nombre_pistes":Piste.nombre_pistes}
        with open(asksaveasfilename(defaultextension=".json"), "w") as f:
            json.dump(dico, f, indent=2)
    
    def import_image(self):
        self.image_path = askopenfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def import_json(self):
        """importe tout le contexte contenu dans un json fait
        par la fonction App.export_json()"""
        self.canvas.delete("all")
        self.import_image()
        self.pistes = []
        self.noeuds = []
        self.historique = []
        with open(askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")]),"r") as f:
            dico = json.load(f)
        for noeud in dico["noeuds"]:
            self.noeuds.append(Noeud(noeud["x"], noeud["y"],noeud["name"]))
        for piste in dico["pistes"]:
            for noeud in self.noeuds:
                if piste["noeud_depart"] == noeud.name:
                    self.pistes.append(Piste(noeud, piste["couleur"]))
                    self.pistes[-1].coords = piste["coords"]
                    self.pistes[-1].longueur = piste["longueur"]
                    self.pistes[-1].set_name(piste["name"])
                    noeud.add_sortie(self.pistes[-1])
                    for noeud in self.noeuds:
                        if piste["noeud_fin"] == noeud.name:
                            self.pistes[-1].noeud_fin = noeud
                            self.pistes[-1].show(self.canvas)
                            noeud.add_entree(self.pistes[-1])
        for noeud in self.noeuds:
            noeud.show(self.canvas)
            

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
