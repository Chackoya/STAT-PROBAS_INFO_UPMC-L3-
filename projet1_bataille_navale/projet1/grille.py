import numpy as np
import random
import matplotlib.pyplot as plt

class grille():
    def __init__(self):
        self.tab = np.zeros([10,10])
        self.list_bat = []
        
    def eq(self ,grilleB):
        return (np.array_equal(self.tab, grilleB.tab))
        
    def peut_placer(self, bateau, position, direction):
        """ direction : 1 pour horizontal, 2 pour vertical """
        taille = bateau.getTaille()
        i = position[0]
        j = position[1]
        if direction == 1:
            if taille + j > 10:
                return False
            while taille > 0:
                if(self.tab[i,j] != 0):
                    return False
                taille -= 1
                j += 1
                
        else :
            if taille + i > 10:
                return False
            while taille > 0:
                if(self.tab[i,j] != 0):
                    return False
                taille -= 1
                i += 1
            
        return True
    def peut_placerV2(self, bateau, position, direction):
        """ direction : 1 pour horizontal, 2 pour vertical """
        taille = bateau.getTaille()
        i = position[0]
        j = position[1]
        if direction == 1:
            if taille + j > 10:
                return False
            while taille > 0:
                if(self.tab[i,j] != 0 ):
                    return False
                taille -= 1
                j += 1
                
        else :
            if taille + i > 10:
                return False
            while taille > 0:
                if(self.tab[i,j] != 0):
                    return False
                taille -= 1
                i += 1
            
        return True
    
            
        
        
    
    def affiche(self) :
        plt.imshow(self.tab)
        plt.show()
    
    def place_alea(self, bateau):
        direction = random.randint(1,2)
        position = (random.randint(0,9), random.randint(0,9))
        while(not(self.place(bateau, position, direction))) :
            direction = random.randint(1,2)
            position = (random.randint(0,9), random.randint(0,9))
        
    
    def place(self, bateau, position, direction):
        """ Renvoie True si on a placé le bateau, false sinon """
        if not(self.peut_placer(bateau, position, direction)):
            return False
        
        taille = bateau.getTaille()
        i = position[0]
        j = position[1]
        list_coord = []
        self.list_bat.append(bateau)
        if direction == 1:
            while taille > 0:
                list_coord.append((i,j))
                self.tab[i][j] += bateau.type_bat
                taille -= 1
                j += 1
                
        else :
            while taille > 0:
                list_coord.append((i,j))
                self.tab[i][j] += bateau.type_bat
                taille -= 1
                i += 1
        
        bateau.placer(list_coord, len(self.list_bat) -1) 
        return True
    
    def vider(self):
        for i in range(10):
            for j in range(10):
                self.tab[i][j] = 0
                
    def equals(self,g2):
        for i in range(10):
            for j in range(10):
                if (self.tab[i][j] != g2.tab[i][j]):
                    return False
        return True
    
    def equals2(self,L1):
        for coord in L1:
            (i, j) = coord[0]
            if not(self.tab[i][j] == coord[1]):
                return False
        return True
        
        
    def trouver_coord(self):
        """
        Trouve les coordonnées ( tuples ) des bateaux. Rend une liste de Tuples 
        """
        L=[]
        for i in range(10):
            for j in range(10):
                if self.tab[i][j]!=0:
                    L.append(((i,j),self.tab[i][j]))        
        return L
    
    def enlever_bateau(self, position, direction, taille):
        i = position[0]
        j = position[1]
        if direction == 1:
            while taille > 0:
                self.tab[i][j] = 0
                taille -= 1
                j += 1
                
        if direction == 2:
            while taille > 0:
                self.tab[i][j] = 0
                taille -= 1
                i += 1

    def getTotalHp(self):
        cpt = 0
        for b in self.list_bat :
            cpt += b.hp
        return cpt