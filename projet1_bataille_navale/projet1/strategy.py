import random
import numpy as np
import time
###############################################################################
class Strategy(object): 
    """Class strategy qui represente la strategie pr gagner en trouvant les 17cases des bateaux, 
    toutes les autres vont hériter des attributs suivants: un tableau pour contenir les coordonnées ratés(miss) ,
    un autre pour les cases touchés(hits) et ainsi que une bataille
    """
    def __init__(self, bataille):
        self.miss = []        #TAB de tirs ratés 
        self.hits = []        #TAB de tirs réussis
        self.total = bataille.totalHp # c'est 17 pour notre jeu
        self.bataille = bataille #class bataille contenant la grille etc
        
###############################################################################
        
        
"""
        ##################
        #JOUEUR ALEATOIRE#
        ##################
"""

class RandomPlayer(Strategy):
    """Strat aléatoire: On commence avec 1 grille aléatoire et a chaque tour on joue un coup random
    """
    def __init__(self, bataille):
        super().__init__(bataille)
        
    def joueCoup(self):
        """Joue une partie et retourne le nombre de coups ratés + coups reussis pr obtenir la victoire(moyenne de 95 coups)
        """
        
        coupsPossibles=coupsPossiblesGrille() ## LISTE DES COUPS possibles en début de partie(cette liste va évoluer au cours de la partie)
        
        while (len(self.hits) < self.total):#condition de fin de jeu, on a pas fini la partie tant que le tab de hits ne contient pas 17 elements
            
            coord_a_Jouer = random.choice(coupsPossibles) # selectionne un coup aleatoire de la liste
            coupsPossibles.remove(coord_a_Jouer) # enleve ce coup de la liste des coupsPossibles
            
            if (self.bataille.joue(coord_a_Jouer)) :#si le tir est reussi on ajoute dans le tableau des hits sinon dans celui des miss
                self.hits.append(coord_a_Jouer)
            else:
                self.miss.append(coord_a_Jouer)
                
            
            #self.bataille.grilleAlea.affiche()
            
        #self.bataille.grilleAlea.affiche()
        
        #Return la somme des miss et hits (c'est notre nombre de coups)
        return len(self.hits) + len(self.miss)
    
    
###############################################################################

"""
        #####################
        #JOUEUR HEURISITIQUE#
        #####################
"""

class HeuresticPlayer(Strategy):
    """ Strat avec regles(exploiter coup precedent):
        1) Jouer random tant que on touche rien( c'est a dire mode hunt = true) )
        2) Qd on touche un bateau, on explore les cases connexes
            (c'est a dire mode hunt = false et on passe a un mode plus aggressif pour couler les cases)
    
    
    """
    
    
    def __init__(self, bataille):
        super().__init__(bataille) # heriter de la classe Strategy et de ses attributs
        
        self.hunt = True # boolean pour décrire le mode dans lequel on se trouve
        
        
    def joueCoup(self):
        """
        Joue une partie entiere et retourne le nombre de coups nécessaires a finir la partie (moyenne de 68 coups)
        """
        coupsPossibles = coupsPossiblesGrille() ## LISTE DES COUPS possibles en début de partie(cette liste va évoluer au cours de la partie)
        stackCoups = [] # une stack pour les cases voisines qui seront prioritaires 
        
        while(len(self.hits) < self.total):#condition de fin de jeu, on a pas fini la partie tant que le tab de hits ne contient pas 17 elements
            
                if(self.hunt): #mode de recherche aléatoire, on change de mode si on touche un bateau
                    move = random.choice(coupsPossibles)
                    coupsPossibles.remove(move)
                    
                    if(self.bataille.joue(move)):#si on a touché un bateau:
                        self.hits.append(move)# ajout a la liste des coups reussis
                        
                        #on regarde les cases voisines a celle du coup joué et on le mets dans stack qui sera regardé en mode aggro(hunt = false)
                        vo = casesVoisines(move)
                        
                        for x in range(len(vo)):
                            (i,j)= vo[x]
                            if( (i,j) in self.hits ) :#juste quelques verifs
                                continue
                                
                            elif(((i,j) in self.miss)):
                                continue
                            else:
                                stackCoups.append((i,j))#ajout dans le stack les cases des voisins de move qui ne sont pas déja jouées...
                        
                        
                        self.hunt=False #changement de mode
                    
                    
                    else: #si on a raté le tir
                        self.miss.append(move)
                        
                #Exploration des voisins:
                else:
                    while(len(stackCoups)>0): # tant qu'il reste des coups de voisins
                        move=random.choice(stackCoups)
                        if (move) in coupsPossibles:#simple verif
                            #maj des coups:
                            coupsPossibles.remove(move)
                            stackCoups.remove(move) 
                            
                            if(self.bataille.joue(move)): # si on a touché un bateau:
                                self.hits.append(move)

                                #update de la stack des nouvelles cases connexes:
                                vo = casesVoisines(move)
                                for x in range(len(vo)):
                                    (i,j)= vo[x]
                                    if( (i,j) in self.hits ) :
                                        continue
                                        
                                    elif(((i,j) in self.miss)):
                                        continue
                                    
                                    else:
                                        stackCoups.append((i,j))
                                        
                                        
                            else: #si on a raté le tir:
                                self.miss.append(move)
                        else:#code pour enlever les coups repetés 
                            stackCoups.remove(move)
                            continue
                    
                    self.hunt=True #Retour en mode hunt (c-a-d mode de recherche aléatoire)
                    
        #Return la somme des miss et hits (c'est notre nombre de coups jouées au total)
        return len(self.hits) + len(self.miss)

###############################################################################
"""
    #########################
    #JOUEUR PROBA SIMPLIFIEE#
    #########################
"""

class ProbaPlayer(Strategy):
    def __init__(self, bataille):
        super().__init__(bataille) #Heritage des attributs de la class Strategy
        self.hunt = True #mode de jeu hunt pour 
        self.shipsLeft = list(bataille.grilleAlea.list_bat) #liste de bateaux restants
        self.probas = np.zeros([10,10]) # un array10x10 contenant des 0 , elle va servir nous servir pour examiner les cases les plus probables

    def joueCoup(self):
        """Joue une partie entiere avec la version probabiliste simplifiée:
        Résumé bref de l'algo
        Tant que la partie est pas finie:
            En mode hunt=true : -on va chercher les cases qui ont le plus de potentiel(selon le nombre de possibilités de placer un bateau dessus)
                                -on prend un coup qui a le potentiel le plus grand
                                -on le joue et on regarde si on a touché un bateau et on prend les voisins du coup joué pour passer au mode aggro(hunt = false)
                                
            En mode hunt=false: tant que stack contient un coup:
                                -on joue un coup qui est dans une stack prioritaire (des cases voisines a celle joué avant en mode hunt recherche proba)
                                
        Return nb de coups joués 
        
        -----------------------------------------------------------------------
        -> Résultats obtenus avec cette méthode par rapport a la version heuristique pour 1000 parties:
            Moyenne heuristique     :68 coups 
            Moyenne probaSimplifiée : 59 coups
            Il y a donc une nette amélioration...Presque 10 coups en moyenne avec une stratégie qui utilise les probas.
        

        """
        stackCoups=[]
        while(len(self.hits) < self.total):#condition de fin de jeu, on a pas fini la partie tant que le tab de hits ne contient pas 17 elements

                self.probas=np.zeros([10,10])#reset
                if(self.hunt):#Mode de recherche case selon les probas
                    #nouveau plateau pr verifier les possibilités de positionnement en tenant compte des cases deja visitées
                    newPlateauCheck= grilleModif(self.hits, self.miss)
                    
                    # on regarde a chaque tour chaque bateau: 
                    for b in range(len(self.shipsLeft)):
                        bateau_courant = self.shipsLeft[b]
                        for i in range(10):#Parcours du plateau
                            for j in range(10):

                            #Calculs probas horizontal et vertical(on incremente la table selon le nb de posisions pr chaque case )
                            #on ajoute a self.probas[i][j] +1 a chaque fois qu'une position est possible pr le bateau(on regarde pr ttes les directions possibles)
                                if peut_placerRightLeft(newPlateauCheck,bateau_courant,(i,j),1,1): # param 1 pour horizontal et droite
                                    for z in range (bateau_courant.getTaille()):
                                        self.probas[i][j+z] += 1  #on ajoute +1 pr ttes les cases que le bateau occupe
                                if peut_placerRightLeft(newPlateauCheck,bateau_courant,(i,j),1,2):#horizontal gauche
                                    for z in range (bateau_courant.getTaille()):
                                        self.probas[i][j-z] += 1
                                if peut_placerRightLeft(newPlateauCheck,bateau_courant,(i,j),2,1):#VERTICAL bas
                                    for z in range (bateau_courant.getTaille()):
                                        self.probas[i+z][j] += 1
                                if peut_placerRightLeft(newPlateauCheck,bateau_courant,(i,j),2,2):#vertical haut
                                    for z in range (bateau_courant.getTaille()):
                                        self.probas[i-z][j] += 1
                                        
                    #Dans le cas ou il y a des cases dans l'array "probas" a probabilité égale on va prendre un max au hasard
                    listMovesMax = calculListMaxMatrix(self.probas)
                    move= random.choice(listMovesMax) # choix au hasard 
                    xMax,yMax = move[1]
                    
                    #print(self.probas)
                    #time.sleep(10)
                    
                    if ((xMax,yMax) in self.hits or (xMax,yMax) in self.miss): #juste une verif
                        print("This is fine...")
                        time.sleep(10)
                    
                    if(self.bataille.joue((xMax,yMax))): #si on a touché un bateau
                        
                        self.hits.append((xMax,yMax))
                        
                        ######Verif si c'est coulé on l'enleve de la liste des bateaux restants
                        sunkedShip = self.bataille.grilleAlea.tab[xMax][yMax]
                        
                        for sunkedShip in self.shipsLeft:
                            if sunkedShip.isDead(): # s'il est coulé,(comme quand on annonce qu'un bateau est coulé si touché)
                                self.shipsLeft.remove(sunkedShip)
                            
                        ########
                        vo = casesVoisines((xMax,yMax)) # regarde les cases voisines ,
                        for x in range(len(vo)):
                            (i,j)= vo[x]
                            if( (i,j) in self.hits ) :
                                continue
                            elif(((i,j) in self.miss)):
                                continue
                            else:
                                stackCoups.append((i,j))#j'ai mnt un tas avec les coups voisins qui sont pas deja jouées
                        self.hunt=False # passage mode aggro

                    else:
                        self.miss.append((xMax,yMax))
                        
                else:#mode target qui va verifier les cases autour
                    while(len(stackCoups)>0): # tant qu'il reste des coups de voisins
                        move=random.choice(stackCoups)
                        if( move in self.hits) or( move in self.miss):#simple verif
                            stackCoups.remove(move)

                        else:#si c'est pas un coup deja joué (verif)
                            stackCoups.remove(move)
                            if(self.bataille.joue(move)):#si touché 
                                self.hits.append(move)
                                vo = casesVoisines(move)#check cases voisines et les prochains coups seront consacrés a ces cases 
                                for x in range(len(vo)):
                                    (i,j)= vo[x]
                                    if( (i,j) in self.hits ) :
                                        continue
                                    elif(((i,j) in self.miss)):
                                        continue
                                    else:
                                        stackCoups.append((i,j))
                            else:# si on a raté le bateau : 
                                self.miss.append(move)
                                
                    self.hunt=True#on repasse en mode recherche avec probas
                    
        #Return la somme des miss et hits (c'est notre nombre de coups jouées au total)
        return len(self.hits) + len(self.miss)

def calculListMaxMatrix(L):
    """calcule les max issus de L et ses index et le mets dans un tableau res"""
    res=[]
    max = 0
    for i in range(len(L)):
        for j in range (len(L)):
           if L[i][j]>= max:
               max = L[i][j]
               
               
    for i in range(len(L)):
        for j in range(len(L)):
            if L[i][j] == max :
                res.append((max,(i,j)))
                
            
    return res
    
    
def peut_placerRightLeft(tab,bateau,position,direction, RL):# 1 pour horizontal , 2 pr vertical , 1 pr droite(ou bas) 2 pr gauche(ou haut)
    """Fonction pr verifier les placements dans les differents direction horizontales / verticales
    """
    taille=bateau.getTaille()
    i = position[0]
    j = position[1]
    
    if direction == 1 and RL == 1 :#horizontl droite
        if taille + j > 10:
            return False
        while taille > 0:
            if (tab[i,j]!=0):
                return False
            taille -=1
            j+=1
    if direction == 1 and RL == 2 :#horizontal gauche
        if j - taille < 0:
            return False
        while taille >0:
            if(tab[i,j]!=0):
                return False
            taille -=1
            j-=1
            
    if direction == 2 and RL == 1 :#vertical bas
        if taille +i > 10:
            return False
        while taille > 0:
            if (tab[i,j]!=0):
                return False
            taille -=1
            i+=1
    if direction == 2 and RL == 2 :#vertical haut
        if i-taille < 0:
            return False
        while taille > 0:
            if (tab[i,j]!=0):
                return False
            taille -=1
            i-=1
    
    return True
            
    
    
    
def grilleModif(L1,L2):
        """Va prendre 2 lists en parametres , logiquement la liste des miss et les hits et va 
        retourner un plateau de jeu modifié adapté a ces lists
        """
        
        newPlateau = np.zeros([10,10])
        
        for i in range (len(L1)):
            x,y = L1[i]
            newPlateau[x][y]=-9
            
        for i in range(len(L2)):
            x,y = L2[i]
            newPlateau[x][y]=-9
        return newPlateau    

def probasCalculator(grille, bateau ):
    MatrixProba =np.zeros([10,10])
    
    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille.peut_placer(bateau,(i,j),1):
                MatrixProba[i][j]+= 1
                
            if grille.peut_placer(bateau,(i,j),2):
                MatrixProba[i][j]+= 1
    
    return MatrixProba
    
    
    
    
def coupsPossiblesGrille():
    """FCT auxiliaire pr generer les coups possibles en debut de partie sous forme de liste contenant des tuples:
    """
    coupsPossibles=[]
    for i in range(10):
            for j in range (10):
                coupsPossibles.append( (i,j) )
    return coupsPossibles

def casesConnexes(grille, position):
    taille = len(grille.tab)
    i,j = position
    list_coord_i = [i-1,i+1]
    list_coord_j = [j-1,j+1]
    [list_coord_i.remove(i) for i in list_coord_i if i>taille-1 or i < 0]
    [list_coord_j.remove(j) for j in list_coord_j if j>taille-1 or j < 0]
    return [(i2,j) for i2 in list_coord_i] + [(i,j2) for j2 in list_coord_j]



def casesVoisines(move):
    """
    Return les cases voisines d'un coup
    """
    x,y=move
    neighbors =[(x+a[0], y+a[1]) for a in 
                    [(-1,0), (1,0), (0,-1), (0,1)] 
                    if ( (0 <= x+a[0] < 10) and (0 <= y+a[1] < 10))]
                               
    return neighbors 