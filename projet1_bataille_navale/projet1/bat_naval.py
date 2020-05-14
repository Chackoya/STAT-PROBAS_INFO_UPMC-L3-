"""Etudiants: PEREIRA GAMA Gustavo /// EL BEBLAWY Rami

Ici on trouve les fonctions de la partie combinatoire, il suffit de lancer le programme et suivre les indications
du terminal pour choisir la fonction qu'on souhaite tester.

Il y a aussi les fcts d'affichages (graphiques).
Ps: pour la partie  Modélisation probabiliste du jeu , il faut aller dans le fichier "theMain.py" (on y trouve la version random, heuristique et proba simplifiée)

"""
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline, BSpline
from scipy import stats
from grille import *
from bateau import *
from bataille import *
from strategy import *
from scipy import interpolate
import time
#############################################################
#                                                           #
#               MAIN PARTIE COMBINATOIRE                    #
#                                                           #
#                                                           #
#############################################################
def mainCombinatoire():
    print("Entrez 1 pour dénombrer le nombre de façons de placer un bateau donné sur une grille vide;\nEntrez 2 pour le dénombrement d'une grille a 2 bateaux;\nEntrez 3 pour le dénombrement de 3 bateaux;\nEntrez 4 pour le dénombrement liste de bateaux;\nEntrez 5 pour essayer de trouver une grille aléatoire donnée;")
    nb = input()
    a=int(nb)
    g=grille()
    if a ==1: #DENOMBREMENT 1 BATEAU
        start_time = time.time()
        list_bat = []
        list_bat.append(bateau(5,1))
        list_bat.append(bateau(4,2))
        list_bat.append(bateau(3,3))
        list_bat.append(bateau(3,4))
        list_bat.append(bateau(2,5))

        for b in list_bat:
            res= denombre_places_bateau(g,b)
            print("Résultat pour un bateau de taille {} : {}.".format(b.getTaille(),res))
        
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    if a==2:
        start_time = time.time()
        denombre_placer_2_bateaux()
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    if a==3:
        start_time = time.time()
        denombre_placer_3_bateaux()
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    if a==4: 
        start_time = time.time()
        test()
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    if a==5:
        start_time = time.time()
        trouve_bonne_grille()
        print("Temps d execution : %s secondes ---" % (time.time() - start_time))
        
        
        
        
        
        #RESTE DES FCTS 
###############################################################################
        
def genere_grille():
    g = grille()
    list_bat = []
    list_bat.append(bateau(5,1))
    list_bat.append(bateau(4,2))
    list_bat.append(bateau(3,3))
    list_bat.append(bateau(3,4))
    list_bat.append(bateau(2,5))
    [g.place_alea(i) for i in list_bat]
    return g    
    
    
    
def denombre_places_bateau(grille, bateau):
    """
    PARTIE COMBINATOIRE Q2.
    
    Fonction qui permet de dénombrer le nombre de façons de placer
    un bateau donné sur une grille vide
    
    """
    cpt = 0
    for i in range(10):
        for j in range(10):
            if grille.peut_placer(bateau, (i,j), 1):
               cpt += 1
        
            if grille.peut_placer(bateau, (i,j), 2):
               cpt += 1
    return cpt


def denombre_placer_2_bateaux():
    """
    PARTIE COMBINATOIRE Q3 
    
    Fonction qui permet de dénombrer le nombre de façons de placer
    2bateaux sur une grille vide
    """
    
    bateaux_différents = []
    bateaux_différents.append(bateau(5,1))    
    bateaux_différents.append(bateau(4,2))    
    bateaux_différents.append(bateau(3,3))  
    bateaux_différents.append(bateau(2,5))
    g = grille()
    for b in bateaux_différents:
        for b2 in bateaux_différents:
            cpt = 0
            for i in range(10):
                for j in range(10):
                    if(g.place(b, (i,j), 1)):
                        cpt = cpt + denombre_places_bateau(g, b2)
                        g.enlever_bateau((i,j),1,b.taille)
            for i in range(10):
                for j in range(10):
                    if(g.place(b, (i,j), 2)):
                        cpt = cpt + denombre_places_bateau(g, b2) 
                        g.enlever_bateau((i,j),2,b.taille)
            print("Taille des bateaux : {} et {}, façon de le placer : {}".format(b.getTaille(), b2.getTaille(), cpt))
 

def denombre_placer_3_bateaux():
    """
    PARTIE COMBINATOIRE Q3
    
    Fonction qui permet de dénombrer le nombre de façons de placer
    3 bateaux sur une grille vide
    """
    bateaux_différents = []
    bateaux_différents.append(bateau(5,1))    
    bateaux_différents.append(bateau(4,2))    
    bateaux_différents.append(bateau(3,3))  
    bateaux_différents.append(bateau(2,5))
    g = grille()
    for b in bateaux_différents:
        for b2 in bateaux_différents:
            for b3 in bateaux_différents:
                cpt = 0
                for i in range(10):
                    for j in range(10):
                        if(g.place(b, (i,j), 1)):                     
                            for i2 in range(10):
                                for j2 in range(10):
                                    if(g.place(b2, (i2,j2), 1)):
                                        cpt = cpt + denombre_places_bateau(g, b3) 
                                        g.enlever_bateau((i2,j2),1,b2.taille)
                            for i2 in range(10):
                                for j2 in range(10):
                                    if(g.place(b2, (i2,j2), 2)):
                                        cpt = cpt + denombre_places_bateau(g, b3) 
                                        g.enlever_bateau((i2,j2),2,b2.taille)
                            g.enlever_bateau((i,j),1,b.taille)
                            
                for i in range(10):
                    for j in range(10):
                        if(g.place(b, (i,j), 2)):                     
                            for i2 in range(10):
                                for j2 in range(10):
                                    if(g.place(b2, (i2,j2), 1)):
                                        cpt = cpt + denombre_places_bateau(g, b3) 
                                        g.enlever_bateau((i2,j2),1,b2.taille)
                            for i2 in range(10):
                                for j2 in range(10):
                                    if(g.place(b2, (i2,j2), 2)):
                                        cpt = cpt + denombre_places_bateau(g, b3) 
                                        g.enlever_bateau((i2,j2),2,b2.taille)
                            g.enlever_bateau((i,j),2,b.taille)
                            
                print("Taille des bateaux : {} et {} et {}, façon de le placer : {}".format(b.getTaille(), b2.getTaille(), b3.getTaille(), cpt))

def test():
    """
    Q5
    """
    g2=grille()
    list_bat = []
    list_bat.append(bateau(5,1))
    list_bat.append(bateau(4,2))
    list_bat.append(bateau(3,3))
    list_bat.append(bateau(3,4))
    list_bat.append(bateau(2,5)) 
    grille_vide = grille()
    for i in list_bat:
        g2.vider()
        prob_place = denombre_places_bateau(grille_vide, i)
        g2.place_alea(i)
        for j in list_bat:
            prob_2_place = prob_place * denombre_places_bateau(g2, j)
            g2.place_alea(j)
            for k in list_bat:
                prob_3_place = prob_2_place * denombre_places_bateau(g2, k)
                g2.place_alea(k)
                for l in list_bat:
                    prob_4_place = prob_3_place * denombre_places_bateau(g2, l)
                    g2.place_alea(l)
                    for m in list_bat:
                        print("Taille des bateaux : {} et {} et {} et {} et {}, façon de le placer : {}".format(i.getTaille(), j.getTaille(), k.getTaille(), l.getTaille(), m.getTaille(), prob_4_place * denombre_places_bateau(g2, m)))
                        
    """                    
def trouve_bonne_grille():
    g1 = genere_grille()
    cpt = 1
    g2 = genere_grille()
    while not(g1.equals(g2)):
        g2 = genere_grille()
        cpt = cpt +1
        print(cpt)
    return cpt"""

def trouve_bonne_grille():
    """PARTIE COMBINATOIRE Q4
    Fonction qui genere 1 premiere grille g1 et qui ensuite va generer plusieurs grilles g2 jusqu'a retomber sur une égale a g1.
    Return le nombre de grilles generés jusqu'a trouver la bonne
    """
    g1 = genere_grille()#genere 1 ere grille
    cpt = 1
    L = g1.trouver_coord() #trouve les coord de la grille g1 et compare ces coord a la grille g2 
    g2 = genere_grille()
    while not(g2.equals2(L)):
        g2 = genere_grille()
        cpt = cpt +1
        print(cpt)
    return cpt
###############################################################################
#AFFICHAGES GRAPHIQUES:
###############################################################################

#from matplotlib.ticker import PercentFormatter
def percentage(part, whole):
  return 100 * float(part)/float(whole)

def tracer_courbe(L):
    
    
    x=np.asarray(L)
    #x_smooth=np.linspace(x.min(),x.max(),len(L))
    
    #print(x_smooth)
    
    xs=np.sort(x)
    
    y=np.linspace(0,len(L),len(L))
    #print(len(y))
    
    for i in range(len(y)): #CONVERSION Y Axis en % 
        y[i] = percentage(y[i], len(y))
        
    
    #f = interpolate.interp1d(xs, y) #zz
    
    
    
    #plt.yaxis.set_major_formatter(PercentFormatter())
    plt.xlabel("Nombre de coups")
    plt.ylabel("Nombre de parties terminées en %")
    plt.plot(xs ,y)
    
    plt.show()
def tracer_histo(L):
    
    x=np.asarray(L)
    np.sort(x)
    
    plt.xlabel("Nombre de coups")
    plt.ylabel("Nombre de parties terminées")
    
    plt.hist(x)
    plt.show()

def tracer_courbe_ttes_les_strat(L1,L2,L3):
    x1= np.asarray(L1)
    x2= np.asarray(L2)
    x3= np.asarray(L3)
    
    xs1 = np.sort(x1)
    xs2 = np.sort(x2)
    xs3 = np.sort(x3)
    
    
    y= np.linspace(0,len(L1),len(L1))
    plt.xlabel("Nombre de coups")
    plt.ylabel("Nombre de parties terminées en %")
    for i in range(len(y)): #CONVERSION Y Axis en % 
        y[i] = percentage(y[i], len(y))
    plt.plot(xs1,y)
    plt.plot(xs2,y)
    plt.plot(xs3,y)
    plt.show()
    
def tracer_histo_ttes_les_strat(L1,L2,L3):
    x1=np.asarray(L1)
    x2=np.asarray(L2)
    x3=np.asarray(L3)
    colors = ['b','g','r']
    plt.xlabel("Nombre de coups")
    plt.ylabel("Nombre de parties terminées")
    plt.hist([x1,x2,x3],color=colors)
    #plt.hist(x2)
    plt.show()


    
if __name__ == '__main__':
    mainCombinatoire()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
###############################################################################
"""
g=grille()
b = bateau(4,2)
res1=denombre_places_bateau(g,b)
print("Resultat :",res1)
#denombre_placer_2_bateaux()
#denombre_placer_3_bateaux()
r=trouve_bonne_grille()
print(r)

"""
"""  
def main():
    nbParties=100
    print("Entrez 1 pour Version Random , 2 pour Version Heuristique et 3 pour Version proba:")
    nb=input()
    a=int(nb)
     
    
    if a==1:
        ###########################Version Random#######################
        totalRandom=0
        tabRandom=[]
        for i in range (nbParties):    
            grilleRandom= genere_grille()
            battle = Bataille(grilleRandom)
            player = RandomPlayer(battle)
            compteur = player.joueCoup()
            totalRandom+= compteur
            tabRandom.append(compteur)
        print("len tabrand",len(tabRandom))
            
        print("total de coups joués par randomplayer :",round(totalRandom/nbParties))
        tracer_histo(tabRandom)
        tracer_courbe(tabRandom)
    
    ######################Version Heuristique################
    if a==2:
        tabHeur=[]
        totalHeure=0
        for i in range (nbParties):   
            grilleRandom= genere_grille()
            battle = Bataille(grilleRandom)
            player = HeuresticPlayer(battle)
            compteur = player.joueCoup()
            totalHeure+= compteur
            tabHeur.append(compteur)
        print("len tabheur",len(tabHeur))
        print("total de coups joués par heuristiclayer :",round(totalHeure/nbParties))
        
        tracer_histo(tabHeur)
        tracer_courbe(tabHeur)
    
    
    #######################Version PROBA###################
    if a == 3:
        totalProbaSimp=0
        tabProbaSimp=[]
        for i in range (nbParties):    
            grilleProbaSimp= genere_grille()
            battle = Bataille(grilleProbaSimp)
            player = ProbaPlayer(battle)
            compteur = player.joueCoup()
            totalProbaSimp+= compteur
            tabProbaSimp.append(compteur)
        
        print("total de coups joués par ProbaSimplifiéePlayer :",round(totalProbaSimp/nbParties))
        
        tracer_histo(tabProbaSimp)
        tracer_courbe(tabProbaSimp)

"""