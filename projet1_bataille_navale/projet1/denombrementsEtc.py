def denombre_places_bateau(grille, bateau):
    cpt = 0
    for i in range(10):
        for j in range(10):
            if grille.peut_placer(bateau, (i,j), 1):
               cpt += 1
        
            if grille.peut_placer(bateau, (i,j), 2):
               cpt += 1
    return cpt


def denombre_placer_2_bateaux():
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
