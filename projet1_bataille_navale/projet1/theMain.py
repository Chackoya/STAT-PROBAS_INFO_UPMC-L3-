"""Etudiants: PEREIRA GAMA Gustavo /// EL BEBLAWY Rami

Ici on trouve les fonctions de la  Modélisation probabiliste du jeu, il suffit de lancer le programme et suivre les indications
du terminal pour choisir la fonction qu'on souhaite tester.


Ps: pour la partie combinatoire, il faut aller dans le fichier "bat_naval.py" (on y trouve les fcts de dénombrements,trouver des grilles aléatoires etc)

"""
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from scipy import stats
from grille import *
from bateau import *
from bataille import *
from strategy import *
from bat_naval import *

def main():
    nbParties=100 #MODIFIER ICI POUR CHOISIR LE NOMBRE DE PARTIES.
    
    print("Entrez 1 pour tester la version Random;\nEntrez 2 pour test la version Heuristique;\nEntrez 3 pour tester la version probabiliste simplifiée;\nEntrez 4 si vous souhaitez générer les 3 strats sur un seul graphique;")
    nb=input()
    a=int(nb)
     
    #########################Version Random####################################
    if a==1:
        
        totalRandom=0
        tabRandom=[]
        for i in range (nbParties):    
            grilleRandom= genere_grille()
            battle = Bataille(grilleRandom)
            player = RandomPlayer(battle)
            compteur = player.joueCoup()
            totalRandom+= compteur
            tabRandom.append(compteur)
            
        print("-->Nombre de coups joués en moyenne par RandomPlayer: {} sur un pool de {} parties.".format(round(totalRandom/nbParties),nbParties))
        print("-->Voici quelques graphiques :")
        tracer_histo(tabRandom)
        tracer_courbe(tabRandom)
    
    ######################Version Heuristique##################################
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
        print("-->Nombre de coups joués en moyenne par HeuresticPlayer: {} sur un pool de {} parties.".format(round(totalHeure/nbParties),nbParties))
        print("-->Voici quelques graphiques :")
        tracer_histo(tabHeur)
        tracer_courbe(tabHeur)
    
    
    #####################Version ProbaSimplifiée###############################
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
        
        print("-->Nombre de coups joués en moyenne par ProbaSimplifiéePlayer: {} sur un pool de {} parties.".format(round(totalProbaSimp/nbParties),nbParties))
        print("-->Voici quelques graphiques :")
        tracer_histo(tabProbaSimp)
        tracer_courbe(tabProbaSimp)
    
    
    if a==4: #CODE POUR GENERER LES 3 COURBES EN MEME TEMPS
        totalRandom=0
        tabRandom=[]
        for i in range (nbParties):    
            grilleRandom= genere_grille()
            battle = Bataille(grilleRandom)
            player = RandomPlayer(battle)
            compteur = player.joueCoup()
            totalRandom+= compteur
            tabRandom.append(compteur)
            
        tabHeur=[]
        totalHeure=0
        for i in range (nbParties):   
            grilleRandom= genere_grille()
            battle = Bataille(grilleRandom)
            player = HeuresticPlayer(battle)
            compteur = player.joueCoup()
            totalHeure+= compteur
            tabHeur.append(compteur)
           
        totalProbaSimp=0
        tabProbaSimp=[]
        for i in range (nbParties):    
            grilleProbaSimp= genere_grille()
            battle = Bataille(grilleProbaSimp)
            player = ProbaPlayer(battle)
            compteur = player.joueCoup()
            totalProbaSimp+= compteur
            tabProbaSimp.append(compteur)
        
        tracer_courbe_ttes_les_strat(tabRandom,tabHeur,tabProbaSimp)
        tracer_histo_ttes_les_strat(tabRandom,tabHeur,tabProbaSimp)
    
    
if __name__ == '__main__':
    main()