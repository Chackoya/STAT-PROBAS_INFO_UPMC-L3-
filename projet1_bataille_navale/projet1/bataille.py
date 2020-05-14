

class Bataille ():
    def __init__(self , grilleAlea):
        self.grilleAlea = grilleAlea
        self.totalHp = grilleAlea.getTotalHp()
        self.hpNow = self.totalHp
    
    
    
    def joue(self,position): 
        """Joue un coup dans les coordonnées du tuple position, si ça touche on rend true 
            sinon false
        """
        i,j = position
        if self.grilleAlea.tab[i][j] > 0 :
            self.grilleAlea.tab[i][j] = -1 # On a touché la case
            self.hpNow -= 1
            b = self.trouve_bateau(position)
            b.toucher(position)
            return True
        # rien touché
        return False
    
    def jouev2(self,position): 
        """Joue un coup dans les coordonnées du tuple position, si ça touche on rend true 
            sinon false
        """
        i,j = position
        if self.grilleAlea.tab[i][j] > 0 :
            self.grilleAlea.tab[i][j] = -1 # On a touché la case
            self.hpNow -= 1
            b = self.trouve_bateau(position)
            b.toucher(position)
            return True,b
        # rien touché
        return False

    def victoire(self):
        """
        Rend true si tt les bateaux sont coulés, false s'il en reste des bateaux a detruire
        """
        if self.hpNow == 0:
            return True
        return False

    def trouve_bateau(self, position):
        for b in self.grilleAlea.list_bat:
            for c in b.coord:
                if c == position:
                    return b
        raise EOFError
        
    
    
    def get(self, position) :
        x, y = position
        return self.grille[x][y]
    def getGrille(self):
        return self.grilleAlea
    