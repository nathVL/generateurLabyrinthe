from pyscript import document
from random import *


class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    
    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire
    
    def remove_wall(self, c1, c2):
        """
        Supprime un mur entre deux cellules
        
        Arguments:
            c1 (tuple): cellule 1
            c2 (tuple): cellule 2
            
        Retour:
            Ne retourne rien        
        """
        if c2 not in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].add(c2) # on le retire
        if c1 not in self.neighbors[c2]:      # Si c3 n'est pas dans les voisines de c2
            self.neighbors[c2].add(c1) # on le retire
        return None
    
    def get_cells(self):
        """
        Renvoie une liste de tuples représentant les coordonnées de toutes les cellules de la grille
        
        Retour:
            L (list) : Liste de tuples (i,j) où i représente la ligne et j la colonne        
        """
        L = []
        for i in range (self.height):
            for j in range (self.width):
                L.append((i,j))
        return L
    
    def get_walls(self):
        """
        Renvoie une liste de tuples de cellules représentant les murs de la grille
        
        Retour:
            L (list) : Liste de tuples de cellules        
        """
        L = []
        for c in self.get_cells():
            if (c[0], c[1]+1) in self.get_cells() and (c[0], c[1]+1) not in self.neighbors[c]:
                L.append(((c[0], c[1]),(c[0], c[1]+1)))
            if (c[0]+1, c[1]) in self.get_cells() and (c[0]+1, c[1]) not in self.neighbors[c]:
                L.append(((c[0], c[1]),(c[0]+1, c[1])))
        return L
    
    def fill(self):
        """
        Ajoute tous les murs possibles dans le labyrinthe
        
        Retour:
            Ne retourne rien        
        """
        self.neighbors = {(i,j): set() for i in range(self.height) for j in range (self.width)}
        return None
    
    def empty(self):
        """
        Supprime tous les murs du labyrinthe
        
        Retour:
            Ne retourne rien
        """
        for i in range(self.height):
            for j in range(self.width):
                if j+1 < self.height:
                    self.remove_wall((i,j), (i,j+1))
                if i+1 < self.height:
                    self.remove_wall((i,j), (i+1,j))
        return None
        
    def get_contiguous_cells(self, c):
        """
        Retourne la liste des cellules contigües à c dans la grille
        
        Argument:
            c (tuple): Cellule dont on veut connaître ses cellules contigües
        
        Retour:
            lst (list): Liste des cellules contigües à c
        """
#         assert c[0] < self.width and c[1] < self.height, f"Erreur avec {c} : les coordonnées ne sont pas dans la grille"
        lst = []
        if c[0] > 0:
            lst.append((c[0]-1,c[1]))
        if c[0] < self.height-1:
            lst.append((c[0]+1,c[1]))
        if c[1] > 0:
            lst.append((c[0],c[1]-1))
        if c[1] < self.width-1:
            lst.append((c[0],c[1]+1))
        return lst
    
    def get_reachable_cells(self, c):
        """
        Renvoie la liste des cellules accessibles depuis c
        
        Argument:
            c (tuple): Cellule dont on veut connaître ses cellules accessibles
        
        Retour:
            Liste de cellules        
        """
        return [cell for cell in self.neighbors[c]]
      
    @classmethod
    def gen_btree(cls, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes à partir d'un arbre binaire
        
        Arguments:
            cls: classe à laquelle cette méthode appartient
            h (int): hauteur du labyrinthe
            w (int): largeur du labyrinthe
            
        Retour:
            laby (Maze): instance de classe du labyrinthe
        """
        laby = Maze(h,w)
        for cell in laby.neighbors:
            if cell[0] < laby.height-1 and cell[1] < laby.width-1:
                temp = randint(0,1)
                if temp == 0:
                    laby.remove_wall(cell,(cell[0]+1,cell[1]))
                if temp == 1:
                    laby.remove_wall(cell,(cell[0],cell[1]+1))
            elif cell[0] < laby.height-1:
                laby.remove_wall(cell,(cell[0]+1,cell[1]))   
            elif cell[1] < laby.width-1:
                laby.remove_wall(cell,(cell[0],cell[1]+1))
        return laby
    
    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de construction sidewinder
        
        Arguments:
            cls: classe à laquelle cette méthode appartient
            h (int): hauteur du labyrinthe
            w (int): largeur du labyrinthe
            
        Retour:
            labySW (Maze): instance de classe du labyrinthe
        """
        labySW = Maze(h, w)
    
        for i in range(0, h-1):
            seq = []
        
            for j in range (0, w-1):
                seq.append((i,j))
                res = randint(0,1)
                if res == 0:
                    labySW.remove_wall((i,j), (i,j+1))
                if res == 1:
                    cell = randint(0, len(seq)-1)
                    labySW.remove_wall(seq[cell], (seq[cell][0]+1,seq[cell][1]))
                    seq = []
                
            seq.append((i,j))
            cell = randint(0, len(seq)-1)
            labySW.remove_wall(seq[cell], (seq[cell][0]+1,seq[cell][1]))
        
        for k in range(0, w-1):
            labySW.remove_wall((h-1,k), (h-1,k+1))
    
        return labySW
    
    @classmethod
    def gen_fusion(cls, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes avec l'algorithme de fusion de chemin
        
        Arguments:
            cls: classe à laquelle cette méthode appartient
            h (int): hauteur du labyrinthe
            w (int): largeur du labyrinthe
        
        Retour:
            laby (Maze): instance de classe du labyrinthe
        """
        laby = Maze(h, w)
        # label
        label = laby.neighbors.copy()
        a = 0
        for cell in label:
            label[cell] = a
            a += 1
        # liste de tous les murs
        lstMur = laby.get_walls()
        shuffle(lstMur)
        # creer laby
        for mur in lstMur:
            if label[mur[0]] != label[mur[1]]:
                laby.remove_wall(mur[0],mur[1])        
                old = label[mur[1]]
                new = label[mur[0]]
                for cell in label:
                    if label[cell] == old:
                        label[cell] = new
        return laby
    
    @classmethod
    def gen_exploration(cls, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de génération par exploration
        
        Arguments:
            cls: classe à laquelle cette méthode appartient
            h (int): hauteur du labyrinthe
            w (int): largeur du labyrinthe
            
        Retour:
            labyExp (Maze): instance de classe du labyrinthe
        """
        # Création du labyrinthe
        labyExp = Maze(h,w)
        labyExp.fill()

        # Initialisation
        lst_cells = labyExp.get_cells()
        rand_cell = lst_cells[randint(0,len(lst_cells)-1)]
        visite = [rand_cell]
        pile = [rand_cell]

        while pile:
            top = pile.pop()
            contiguous_cells = labyExp.get_contiguous_cells(top)
            contiguous_cells_not_visited = []
            
            #Liste les cellules voisines
            for cell in contiguous_cells:            
                if cell not in visite:
                    contiguous_cells_not_visited.append(cell)
            
            if contiguous_cells_not_visited:
                pile.append(top)
                rand_contig_cell_not_visited = contiguous_cells_not_visited[randint(0, len(contiguous_cells_not_visited)-1)]
                labyExp.remove_wall(rand_contig_cell_not_visited, top)
                visite.append(rand_contig_cell_not_visited)
                pile.append(rand_contig_cell_not_visited)

        return labyExp
    
    @classmethod
    def gen_wilson(cls, h, w):
        """
        Génère un labyrinthe à h lignes et w colonnes en utilisant l'algorithme de Wilson
        
        Arguments:
            cls: classe à laquelle cette méthode appartient
            h (int): hauteur du labyrinthe
            w (int): largeur du labyrinthe
        
        Retour:
            laby (Maze): instance de classe du labyrinthe
        """
        laby = Maze(h, w)
        # Choisir une cellule au hasard sur la grille et la marquer
        marquage = {i : False for i in laby.get_cells()}
        cell = choice(laby.get_cells())
        marquage[cell] = True
        # Tant qu’il reste des cellules non marquées : 
        cellulesMarque = False
        while cellulesMarque == False:
            cellulesMarque = True
            for i in marquage:
                if marquage[i] == False:
                    cellulesMarque = False
            # Choisir une cellule de départ au hasard, parmi les cellules non marquées
            cellNonMarque = []
            for i in marquage:
                if marquage[i] == False:
                    cellNonMarque.append(i)
            if cellNonMarque != []:
                nextCell = choice(cellNonMarque)
            # Effectuer une marche aléatoire jusqu’à ce qu’une cellule marquée soit atteinte
            marche = []
            while marquage[nextCell] == False:
                marche.append(nextCell)
                nextCell = choice(laby.get_contiguous_cells(nextCell))
                # en cas de boucle «couper» la boucle formée
                if nextCell in marche:
                    new = []
                    i = 0
                    while marche[i] != nextCell:
                        new.append(marche[i])
                        i+=1
                    marche = new
            marche.append(nextCell)
            # Marquer chaque cellule du chemin
            for i in marche:
                marquage[i] = True
            #  casser tous les murs rencontrés
            for z in range(len(marche)-1):
                    laby.remove_wall(marche[z],marche[z+1])
        return laby
    
    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            #content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    
    def solve_dfs(self, start, stop):
        """
        Résoudre un labyrinthe et afficher le resultat sur le labyrinthe
        Résout le labyrinthe en parcourant en profondeur
        
        Arguments:
            start (tuple): cellule de départ
            stop (tuple): cellule de fin
        
        Retour:
            path (dict): dictionnaire du chemin resultat
        """
        # Initialisation 
        path = {}
        # Placer D dans la struture d’attente ou et marquer D
        pile = [start]
        marquage = {i : False for i in self.get_cells()}
        # Mémoriser l’élément prédécesseur de D comme étant D
        pred = {i : None for i in self.get_cells()}
        pred[start] = start
        # Tant qu’il reste des cellules non-marquées :
        cellulesMarque = False
        trouver = False
        while trouver == False and cellulesMarque == False:
            cellulesMarque = True
            for i in marquage:
                if marquage[i] == False:
                    cellulesMarque = False
            # Prendre la « première » cellule et la retirer de la structure (appelons c, cette cellule)
            c = pile[-1]
            marquage[c] = True
            del pile[-1]
            # Si c correspond à A 
            if c == stop:
                trouver = True
            else:
                for i in self.get_reachable_cells(c):
                    if not marquage[i]:
                        marquage[i] = True
                        pile.append(i)
                        pred[i] = c
        # Reconstruction du chemin à partir des prédécesseurs
        c = stop
        while c != start:
            path[c] = '*'
            c = pred[c]
        path[start] = 'D'
        path[stop] = 'A'
        return path
    
    def solve_bfs(self, start, stop):
        """
        Résoudre un labyrinthe et afficher le resultat sur le labyrinthe
        Résout le labyrinthe en parcourant en largeur
        
        Arguments:
            start (tuple): cellule de départ
            stop (tuple): cellule de fin
        Retour:
            path (dict): dictionnaire du chemin resultat
        """
        # Initialisation 
        path = {}
        # Placer D dans la struture d’attente file et marquer D
        file = [start]
        marquage = {i : False for i in self.get_cells()}
        # Mémoriser l’élément prédécesseur de D comme étant D
        pred = {i : None for i in self.get_cells()}
        pred[start] = start
        # Tant qu’il reste des cellules non-marquées :
        cellulesMarque = False
        trouver = False
        while trouver == False and cellulesMarque == False:
            cellulesMarque = True
            for i in marquage:
                if marquage[i] == False:
                    cellulesMarque = False
            # Prendre la « première » cellule et la retirer de la structure (appelons c, cette cellule)
            c = file[0]
            marquage[c] = True
            del file[0]
            # Si c correspond à A 
            if c == stop:
                trouver = True
            else:
                for i in self.get_reachable_cells(c):
                    if not marquage[i]:
                        marquage[i] = True
                        file.append(i)
                        pred[i] = c
        # Reconstruction du chemin à partir des prédécesseurs
        c = stop
        while c != start:
            path[c] = '*'
            c = pred[c]
        path[start] = 'D'
        path[stop] = 'A'
        return path
    
    def solve_rhr(self, start, stop):
        # Initialisation 
        path = {}
        cell = start
        chemin = []
        depart = True
        while cell != stop:
            if depart:
                depart = False
                cellPred = start
                cells = laby.get_reachable_cells(start)
                if (start[0]+1,start[1]) in cells:
                    cell = (start[0]+1,start[1])
                elif (start[0],start[1]+1) in cells:
                    cell = (start[0],start[1]+1)
                chemin.append(cell)
            temp = cell
            cells = laby.get_reachable_cells(cell)
            # dessus
            if cellPred[0]-cell[0] == 1:
                if (cell[0],cell[1]+1) in cells:
                    cell = (cell[0], cell[1]+1)
                elif (cell[0]-1,cell[1]) in cells:
                    cell = (cell[0]-1, cell[1])
                elif (cell[0],cell[1]-1) in cells:
                    cell = (cell[0], cell[1]-1)
                elif (cell[0]+1, cell[1]) in cells:
                    cell = (cell[0]+1,cell[1])
            # dessous
            elif cellPred[0]-cell[0] == -1:
                if (cell[0],cell[1]-1) in cells:
                    cell = (cell[0],cell[1]-1)
                elif (cell[0]+1,cell[1]) in cells:
                    cell = (cell[0]+1,cell[1])
                elif (cell[0],cell[1]+1) in cells:
                    cell = (cell[0],cell[1]+1)
                elif (cell[0]-1,cell[1]) in cells:
                    cell = (cell[0]-1,cell[1])
            # droite
            elif cellPred[1]-cell[1] == -1:
                if (cell[0]+1,cell[1]) in cells:
                    cell = (cell[0]+1,cell[1])
                elif (cell[0],cell[1]+1) in cells:
                    cell = (cell[0],cell[1]+1)
                elif (cell[0]-1,cell[1]) in cells:
                    cell = (cell[0]-1,cell[1])
                elif (cell[0],cell[1]-1) in cells:
                    cell = (cell[0],cell[1]-1)
            # gauche
            elif cellPred[1]-cell[1] == 1:
                if (cell[0]-1,cell[1]) in cells:
                    cell = (cell[0]-1,cell[1])
                elif (cell[0],cell[1]-1) in cells:
                    cell = (cell[0],cell[1]-1)
                elif (cell[0]+1,cell[1]) in cells:
                    cell = (cell[0]+1,cell[1])
                elif (cell[0],cell[1]+1) in cells:
                    cell = (cell[0],cell[1]+1)
            chemin.append(cell)              
            cellPred = temp
        for c in chemin:
            path[c] = '*'
        path[start] = 'D'
        path[stop] = 'A'
        return path
    
    def dead_end_number(self):
        culSac = 0
        neig = laby.neighbors
        for i in neig:
            if len(self.get_reachable_cells(i)) == 1:
                culSac += 1
        return culSac
    
    def dead_end_number(self):
        culSac = 0
        neig = laby.neighbors
        for i in neig:
            if len(self.get_reachable_cells(i)) == 1:
                culSac += 1
        return culSac
    
    def distance_geo(self, c1, c2):
        return len(self.solve_bfs(c1, c2))-1
    
    def distance_man(self, c1, c2):
        return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])
    
    def worst_path_len(self, depart):
        neig = laby.neighbors
        culSac = []
        for i in neig:
            if len(self.get_reachable_cells(i)) == 1:
                culSac.append(i)
        distance = 0
        for i in culSac:
            if self.distance_geo((depart), i) > distance:
                distance = self.distance_geo((depart), i)
        return distance


def afficherLabWilson(event):
    output_div = document.querySelector("#output")
    height = document.querySelector("#labHeight").value
    width = document.querySelector("#labWidth").value
    
    laby = Maze.gen_wilson(int(height),int(width))
    if document.querySelector("#resoudre").checked :
        path = laby.solve_bfs((0,0),(int(height)-1,int(width)-1))
        output_div.innerText = f"Le labyrinthe : \n{laby.overlay(path)}"
    else:
        output_div.innerText = f"Le labyrinthe : \n{laby}"