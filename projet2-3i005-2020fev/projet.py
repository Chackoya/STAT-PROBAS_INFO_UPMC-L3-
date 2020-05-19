#PEREIRA GAMA Gustavo (3301503)
#EL BEBLAWY Rami (3670209)

#fini partie 7
import math
import numpy as np
import utils
import scipy
import matplotlib.pyplot as plt
###############################################################################

#Question 1:
def getPrior(data):
    """Fonction qui  calcule la probabilité a priori de la classe  1 
    ainsi que l'intervalle de confiance à 95% pour l'estimation de
    cette probabilité
    
    Parameters
    ----------
    data : dataFrame
        DESCRIPTION: Il s'agit de nos donées qui contiennent une un attr 
        qui prend la valeur 0 ou 1.

    Returns 
    -------
    dico : dict()
        DESCRIPTION. renvoie le dico contenant l'estimation, et la min et max 
        de l'intervale confiance, ici a 95%'

    """
    dico  = dict()
    moyenne = data["target"].mean()
    
    z_score = 1.96 # valeur pr un intervalle de 95% 
    ME = z_score * math.sqrt((moyenne *(1-moyenne))/len(data["target"]))
    
    
    #print(len(data["target"]))
    
    dico["estimation"] = moyenne
    dico["min5pourcent"]= moyenne-ME
    dico["max5pourcent"]= moyenne+ME
    return dico

###############################################################################

#Question 2:
class APrioriClassifier(utils.AbstractClassifier):
    """
    un classifieur APrioriClassifier (enfant de AbstractClassifier)
    qui utilise le résultat de la question 1 pour estimer très 
    simplement la classe de chaque individu par la classe majoritaire
    """
    def __init__(self):#Constructor 
        pass
    
    
    def estimClass(self, attrs):
        """
        Ã  partir d'un dictionanire d'attributs, estime la classe 0 ou 1

        :param attrs: le  dictionnaire nom-valeur des attributs
        :return: la classe 0 ou 1 estimÃ©e
        """
        """
        d=getPrior(attrs)
        
        if d.get('estimation') > 0.5:
            
            return 1
        return 0
        """
        return 1
    
    def statsOnDF(self, df):
        """
          Ã  partir d'un pandas.dataframe, calcule les taux d'erreurs de classification 
          et rend un dictionnaire.

        :param df:  le dataframe Ã  tester
        :return: un dictionnaire incluant les VP,FP,VN,FN,prÃ©cision et rappel
        """
        res_dico=dict()
        VP=0
        VN=0
        FP=0
        FN=0
        
        
        for t in df.itertuples():
            dic = t._asdict()
            
            #print("ca={} oldpeak={} target={}".format(dic['ca'],dic['oldpeak'],dic['target']))
            
            estim = self.estimClass(dic)
            
            if dic["target"] ==1:
                if estim == 1:
                    VP=VP+1
                else:
                    FN=FN+1
            else:
                if estim ==1:
                    FP=FP+1
                else:
                    VN=VN+1
        
        
        res_dico["VP"]=VP
        res_dico["VN"]=VN
        res_dico["FP"]=FP
        res_dico["FN"]=FN
        res_dico["Précision"]= VP/(VP+FP)
        res_dico["Rappel"]= VP/(VP+FN)
        return res_dico

###############################################################################
        
#Q3.a
def P2D_l(df,attr):
    """calcule dans le dataframe la probabilité  𝑃(𝑎𝑡𝑡𝑟|𝑡𝑎𝑟𝑔𝑒𝑡)  
    sous la forme d'un dictionnaire asssociant à la valeur  𝑡  
    un dictionnaire associant à la valeur  𝑎  la probabilité  𝑃(𝑎𝑡𝑡𝑟=𝑎|𝑡𝑎𝑟𝑔𝑒𝑡=𝑡) 
    """
    res_dico = dict()
    
    keysDico = np.unique(df[attr].values) #valeurs uniques de l'attribut
    res_dico[1]= dict((k,0) for k in keysDico)
    res_dico[0]= dict((k,0) for k in keysDico)
    
    #On a res_dico[i] initialisé avec les differentes valeurs uniques de l'attribut

    nb_t1=len(df.query('target== 1')) #nb de valeurs target = 1
    nb_t0= len(df.query('target== 0'))#nb de valeurs target = 0
    
    #Iteration sur le dataframe:
    for t in df.itertuples():
        dic = t._asdict()
        
        valattr= dic[attr] # <- valattr contient juste la valeur de l'attribut qu'on cherche 
        
        if dic["target"] == 0 :
            res_dico[0][valattr]=res_dico[0][valattr]+ 1
        else:
            if dic["target"]==1:
                res_dico[1][valattr]+=1
        
    
    
    #CALCUL DES PROBAS:
    for v in res_dico[0].keys():
        res_dico[0][v] = res_dico[0][v] /nb_t0
    for v in res_dico[1].keys():
        res_dico[1][v]= res_dico[1][v] /nb_t1
    
    
    #print("resdico0",res_dico[0])
    return res_dico
    
def P2D_p(df,attr):
    """calcule dans le dataframe la probabilité  𝑃(𝑡𝑎𝑟𝑔𝑒𝑡|𝑎𝑡𝑡𝑟)  
    sous la forme d'un dictionnaire associant à la valeur  𝑎 
    un dictionnaire asssociant à la valeur  𝑡  la probabilité  𝑃(𝑡𝑎𝑟𝑔𝑒𝑡=𝑡|𝑎𝑡𝑡𝑟=𝑎) .
    """
    res_dico=dict()
    keysDico = np.unique(df[attr].values) #valeurs uniques de l'attribut
    
    
    for i in keysDico: #il ya au max 2 target : 0 ou 1 
        res_dico[i]=dict((k,0) for k in range(2))
        
    
    #Iteration sur le dataframe:
    for t in df.itertuples():
        dic = t._asdict()
        valattr=dic[attr]# <- valattr contient juste la valeur de l'attribut qu'on cherche 
        
        if dic["target"] == 0:
            res_dico[valattr][0] +=1
        else:
            if dic["target"]==1:
                res_dico[valattr][1]+=1
        
        
    #print("cc",res_dico)
    #CALCUL DES PROBAS:
    
    tmp=0
    for k in res_dico.keys():
        tmp= res_dico[k][0]+res_dico[k][1]
        
        
        res_dico[k][0]/=tmp
        res_dico[k][1]/=tmp

    return res_dico
        
        
###############################################################################
#Q3.B
class ML2DClassifier(APrioriClassifier):
    def __init__(self,df , attr):
        """ Initiliaser le classifier
        Parameters
        ----------
        df : le dataFrame
        attr :un attribut(str)
        
        -> cree la table avec la fct P2D_l

        """
        self.df = df
        self.attribut=attr
        
        self.table = P2D_l(self.df, self.attribut)
    
    def estimClass(self,attrs):
        """Ã  partir d'un dictionanire d'attributs, estime la classe 0 ou 1

        Parameters
        ----------
        attrs : dict
            DESCRIPTION: un dictionnaire des donnees de la n-ieme ligne. Exemple de format d'une ligne:'
                {'age': 9, 'sex': 1, 'cp': 3, 'trestbps': 9,
                 'chol': 6, 'fbs': 1, 'restecg': 0, 'thalach': 9, 'exang': 0, 
                 'oldpeak': 6, 'slope': 0, 'ca': 0, 'thal': 1, 'target': 1}
        Returns
        -------
        Estimation 0 ou 1

        """ 
        X = attrs[self.attribut] #self.attributs est l'attribut qu'on cherche (initialisé dans le classifier)
        probaZERO= self.table[0][X]
        probaONE=self.table[1][X]
        #print(probaONE)
        #print(probaZERO)
        if probaONE>probaZERO:
            return 1
        return 0  #EGALITE PROBAS -> CLASSE 0
        

#Q3.C

class MAP2DClassifier(APrioriClassifier):
    def __init__(self,df , attr):
        """ Initiliaser le classifier
        Parameters
        ----------
        df : le dataFrame
        attr : un attribut (str)

        -> crée la table avec la fct P2D_p

        """
        self.df = df 
        self.attribut = attr
        self.table = P2D_p(self.df,self.attribut)
        
    
    def estimClass(self,attrs):
        """Ã  partir d'un dictionanire d'attributs, estime la classe 0 ou 1
        
        Parameters
        ----------
        attrs : dict 
            DESCRIPTION:  un dictionnaire des donnees de la n-ieme ligne.

        Returns
        -------
        Estimation 0 ou 1
        """
        X=attrs[self.attribut]
        
        probaZERO=self.table[X][0]
        probaONE= self.table[X][1]
        
        if probaONE>probaZERO:
            return 1
        return 0


###############################################################################
#Q4.1
    
def nbParams(df , listeA=None) :
    """ Calcul de la taille en mémoire des tables P(target|attr1 ..., attrk)
    en supposant qu'un float représente 8 octets et étant donné 2 parametres:
        
    Parameters
    ----------
    df : dataFrame
    
    listeA : liste str
        DESCRIPTION: liste content les attributs
        ex:['target','age','thal','sex','exang','slope','ca','chol']

    Returns
    -------
    affiche taille mémoire

    """
    if listeA == None:
        listeA = list(df.columns)
    
    tailleFloat = 8
    res_octets=1 #resultat final taille mem(a convertir si >= 1024)

    for attribut in listeA: 
    
        res_octets = res_octets* len(np.unique(df[attribut]))
        #print(">>print:",len(np.unique(df[attribut])))
        
    res_octets *=tailleFloat
    
    string=""
    if res_octets>=1024:##conversion:
        string= "= "+convert_bytes(res_octets)
    print("{} variable(s) : {} octets {}".format(len(listeA),res_octets,string))
    

    

def convert_bytes(num, L=['o', 'ko', 'mo', 'go','to']):
    """
    

    Parameters
    ----------
    num : int 
        DESCRIPTION: Nombre de octets 
        
    L : List str, optional
        DESCRIPTION. The default is ['o', 'ko', 'mo', 'go','to'].

    Returns
    -------
    res : chaine 

    """
    step_unit = 1024.0
    res=""
    for x in L:
        if num == 0:
            res = res + str(int(num)) + x
            break
        
        if num < step_unit:

            res= str(int(num))+""+ str(x)
            
            b= num - int(num) #valeur apres la virgule
            
            if x == 'to':
                res = res +" "+ str(convert_bytes(b*(1024**4),L[:4]))
                break
            if x == 'go':

                res = res +" "+ str(convert_bytes(b *(1024**3), L[:3]))
                break
            elif x=='mo':
                res = res +" " +str(convert_bytes(b*(1024**2),L[:2]))
                break
            elif x=='ko':
                res = res +" " +str(convert_bytes(b*1024,L[:1]))
                break
            
        num /= step_unit

    return res 

###############################################################################
#Q4.2
    
def nbParamsIndep(df):
    
    listeA = list(df.columns)
    tailleFloat=8#
    res_octets=0
    
    
    #print(listeA)
    
    for attribut in listeA:
        #print(df[attribut])
        tmp=(np.unique(df[attribut].values))

        res_octets = res_octets + len(tmp)*tailleFloat
    string=""
    if res_octets>=1024:
        string= "= "+convert_bytes(res_octets)
    print("{} variable(s) : {} octets {}".format(len(listeA),res_octets,string))
    


###############################################################################
#Q5.3
    
def drawNaiveBayes(df , colClass):
    """Dessine un graphique à partir à partir d'un dataframe et d'une colonne de class

    Parameters
    ----------
    df : dataFrame
    col :str  
        DESCRIPTION: c'est la classe "target"

    Returns
    -------
    Image graphe

    """
    listeA = list(df.columns)
    
    #print(listeA)
    
    arcs =""
    for attr in listeA:
        if attr!=colClass:
            arcs=arcs+ colClass+"->"+attr+";"
        
    return utils.drawGraph(arcs)
        
    
def nbParamsNaiveBayes(df, colClass, listeAttr=None):
    """
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    colClass : TYPE
        DESCRIPTION.
    listeAttr : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    if listeAttr==None:
        listeAttr= list(df.columns)
    
    
    tailleFloat=8  #float : 8octets
    res_octets=0
    nbUniqueVals= len((np.unique(df[colClass].values))) #nb de vals de colClass (binaire ici)
    
    #print("len:,",len(listeAttr))
    if len(listeAttr)==0:
        res_octets= nbUniqueVals*tailleFloat
        
    #print("nombre de variables",uniqueVals_colClass)
    else:
        
        for attribut in listeAttr:
            if attribut != colClass:
                tmp=(np.unique(df[attribut].values)) #tmp : tableau des valeurs uniques de l'attribut et on prend la len ensuite de tmp
                
                res_octets=res_octets + len(tmp)* tailleFloat* nbUniqueVals
                
            else:#qd la valeur d'attribut est la meme que la colClass("target"):
                res_octets=res_octets + nbUniqueVals*tailleFloat
    string =""
    #Conversion si besoin:
    if res_octets>=1024:
        string= "= "+convert_bytes(res_octets)
    print("{} variable(s) : {} octets {}".format(len(listeAttr),res_octets,string))
    
    
    
    
    
###############################################################################
#Q5.4:
class MLNaiveBayesClassifier(APrioriClassifier):
    """
    classifier qui utilise le maximum de vraisemblance (ML)
    """
    def __init__(self,df):
        """ Initiliaser le classifier -> calcule les parametres du NaiveBayes
        Parameters
        ----------
        df : le dataFrame
        """
        self.df = df 
        self.listeA=list(df.columns)
        self.dict_probas=dict() 
        
        for attribut in self.listeA:
            self.dict_probas[attribut]= P2D_l(df, attribut)
        #print(self.dict_probas)
        
        
    def estimProbas(self,dicoIndividu):
        """ Calcule les probas classe 0 et classe 1 

        Parameters
        ----------
        dicoIndividu : dict 
            DESCRIPTION. dict d'attributs d'un individu

        Returns
        -------
        dict avec dict[0] la proba de 0 et dict[1] la proba de 1

        """
        res_probas= dict() #dictionnaire resultat 
        res_probas[0]=1
        res_probas[1]=1
        #print(res_probas)
        for attr in self.dict_probas:#parcourir tt le dico de probas -> attr c'est la clef
            #print(">>")
            #print("ATTRIBUT:",attr)
            if attr!= "target":
                dic_tmp=self.dict_probas[attr] #valeur correspondant a la clef: dico; 
                #dict_tmp cotient donc le dictionnaire correspondant a attr
                
                valAttrIndividu=dicoIndividu[attr] # valeur int correspondant a l'attribut par exemple: 9 pr l'age 
                #print("valind",attr,valAttrIndividu)
                
                #print("dic",dic_tmp[0][valAttrIndividu])

                #PROBLEME KEY ERROR 0 dans l'ensemble de TEST, valeur pr l'attribut
                #oldpeak 0 existe pas donc on ajoute une verif que ça existe vrmt:
                if valAttrIndividu not in dic_tmp[0] or valAttrIndividu not in dic_tmp[1] :
                    res_probas[0]=0 
                    res_probas[1]=0
                    return res_probas #on sort direct en renvoyant les proba a 0 car ça existe pas
                
                #Mult des probas:
                res_probas[0]= res_probas[0] * dic_tmp[0][valAttrIndividu]
                res_probas[1]= res_probas[1] * dic_tmp[1][valAttrIndividu]
                
        return res_probas
                
    def estimClass(self, attrs):
        """a partir d'un dictionanire d'attributs, estime la classe 0 ou 1, fait appel
        a estimProbas pr l'estimation
        
        Parameters
        ----------
        attrs : Dico
            DESCRIPTION: le  dictionnaire nom-valeur des attributs

        Returns
        -------
        la classe : 0 ou 1
        """
        prob_estim = self.estimProbas(attrs)
        
        if prob_estim[1]>prob_estim[0]:
            return 1
        return 0
###############################################################################
#MAPNAIVEBAYES cLASSIFIER:
class MAPNaiveBayesClassifier(APrioriClassifier):
    """classifier qui utilise le max a posteriori(MAP)"""
    
    def __init__(self,df):
        
        self.df=df
        self.listeA=list(df.columns)


        self.dict_probas=dict()
        for attribut in self.listeA:
            self.dict_probas[attribut] = P2D_l(df,attribut)
        #print("dicMAP",self.dict_probas)
        
        
    def estimProbas(self,dicoIndividu):
        res_probas=dict()#dico resultat
        res_probas[1]=  self.df["target"].mean()# % de 1 dans target
        res_probas[0]=1 - res_probas[1]#    % de 0 dans target  -> complément
        
        #print(">>",res_probas)
        
        for attr in self.dict_probas:
            
            if attr != "target":
                dic_tmp = self.dict_probas[attr]
                #print("DICOTMP",attr,dic_tmp)
                valAttrIndividu= dicoIndividu[attr]
                
                
                #print("attribut:",attr, valAttrIndividu)
                if valAttrIndividu not in dic_tmp[0] or valAttrIndividu not in dic_tmp[1] :
                    res_probas[0]=0 
                    res_probas[1]=0
                    return res_probas #on sort direct en renvoyant les proba a 0 car ça existe pas
                
                #print("DICTEMP>>",dic_tmp[])
                #if valAttrIndividu not in dic_tmp[0] and valAttrIndividu not in dic_tmp[1]:
               
                res_probas[0]=res_probas[0] * dic_tmp[0][valAttrIndividu]
                res_probas[1]=res_probas[1] * dic_tmp[1][valAttrIndividu]
        #print(">>",res_probas)
        tmp=res_probas[0]
        res_probas[0]= tmp/(tmp+res_probas[1])
        res_probas[1]= res_probas[1]/(tmp+res_probas[1])
        
        return res_probas
    
    def estimClass(self, attrs):
        """a partir d'un dictionanire d'attributs, estime la classe 0 ou 1, fait appel
        a estimProbas pr l'estimation
        
        Parameters
        ----------
        attrs : Dico
            DESCRIPTION: le  dictionnaire nom-valeur des attributs

        Returns
        -------
        la classe : 0 ou 1
        """
        prob_estim = self.estimProbas(attrs)
        
        if prob_estim[1]>prob_estim[0]:
            return 1
        return 0
    
    
###############################################################################
#Q6

def isIndepFromTarget(df,attr,x):
    """ isIndepFromTarget(df,attr,x) vérifie si attr est indépendant de target au seuil de x%


    Parameters
    ----------
    df : TYPE: dataFrame

    attr : str 
        DESCRIPTION. un attribut 
        
    x : float
        DESCRIPTION. seuil 

    -------
    """
    
    uniqVals = np.unique(df[attr])
    table = np.zeros((2,len(uniqVals)))
    
    
    for i in range(0,len(df)):
        table[df.iloc[i]["target"],np.where(uniqVals==df.iloc[i][attr])] +=1
        
        
    stat, p, dof, expected = scipy.stats.chi2_contingency(table)
    
    return p > x
    

###############################################################################
#Classifier Reduced ML -> herite de MLNAIVEBAYES , on modifie le constructor pr les test d'indep
"""
ReducedMLNaiveBayesClassifier et ReducedMAPNaiveBayesClassifier
 qui utilisent le maximum de vraisemblance (ML) et le maximum a posteriori (MAP)
 pour estimer la classe d'un individu sur un modèle Naïve Bayes qu'ils auront
 préalablement optimisé grâce à des tests d'indépendance au seuil de  𝑥% 
"""
class ReducedMLNaiveBayesClassifier(MLNaiveBayesClassifier):
    def __init__(self, df ,x):
        self.df= df 
        self.x=x
        self.listeA= list(df.columns)
        
        self.listeA.remove("target")
        self.dict_probas= dict()
        
        for attribut in self.listeA:#on enleve de la liste par rapport au resultat de isIndepFromTarget
            if isIndepFromTarget(df, attribut, x):
                self.listeA.remove(attribut) 
        
        for attribut in self.listeA:
            self.dict_probas[attribut] = P2D_l(df, attribut)
        
        
    def draw(self):
        
        arcs =""
        for attr in self.listeA:
        
            arcs=arcs+ "target"+"->"+attr+";"
        
        return utils.drawGraph(arcs)
    

###############################################################################
#Classifier Reduced MAP -> herite de MAPNAIVEBAYES
class ReducedMAPNaiveBayesClassifier(MAPNaiveBayesClassifier):
    def __init__(self, df ,x):
        self.df= df 
        self.x=x
        self.listeA=list(df.columns)
        self.listeA.remove("target")
        
        self.dict_probas= dict()
        
        for attribut in self.listeA:
            if isIndepFromTarget(df, attribut, x):
                self.listeA.remove(attribut)
        
        for attribut in self.listeA:
            self.dict_probas[attribut] = P2D_l(df, attribut)
        
        
    def draw(self):
        
        arcs =""
        for attr in self.listeA:
        
            arcs=arcs+ "target"+"->"+attr+";"
        
        return utils.drawGraph(arcs)
    
    
###############################################################################

#Q7.2 
def mapClassifiers(dic,df):
    """
    dessine le graph des classifieurs a partir d'un dataFrame et d'un dict contenant des instance
    de classifieurs

    Parameters
    ----------
    dic : dict 
        DESCRIPTION. Dico des instances de classifiers
    df : dataFrame
    
    Returns
    -------
    Dessine le graphique

    """
    X_precision=[]
    Y_rappel=[]
    
    for key in dic.keys():
        stat = dic[key].statsOnDF(df) #statOnDf return un dico contenant les info precision et rappel
        
        #print(stat["Précision"])
        X_precision.append( stat["Précision"])
        Y_rappel.append( stat["Rappel"])
    fig=plt.figure()
    ax1=fig.add_subplot(1,1,1)
    ax1.grid(True)
    plt.plot(X_precision,Y_rappel,'x', color='red')

    i=0
    for key in dic.keys():
        ax1.annotate(key,(X_precision[i],Y_rappel[i]))#fct pr mettre les numeros des classifiers a coté du pt
        
        
        #print("Pour",key,"-> X:",X_precision[i],"Y:",Y_rappel[i])
        i=i+1
    plt.show()
    
    
    
###############################################################################
#Q8.1
"""
def MutualInformation(df,X,Y):


  """ 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    