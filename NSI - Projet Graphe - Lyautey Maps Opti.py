# -*- coding: utf-8 -*-

# @Date      : 2022-03-30 18:47:55
# @Auteur(s) : Souleimane El Qodsi et Anas Chati
# @Établissement : Lycée Lyautey de Casablanca, Maroc
# @Titre     : NSI - Projet graphe - LyauteyMaps

import os

class Lieu :
    """Classe modélisant un lieu du lycée Lyautey (sommet du graphe)
    """
    def __init__(self, nom: str):
        """Initalise les attributs d'un objet lieu

        Parameters
        ----------
        valeur : str
            Chaque sommet correspond à un endroit du lycée
            De ce fait, c'est forcément un str
        """
        self.nom = nom
        self.voisins = {} # Dictionnaire sous la forme { Voisin : Pondération }

    def addVoisin(self, voisin, ponderation: int) : 
        """Méthode pour ajouter un voisin immédiat

        Parameters
        ----------
        voisin : str
            Nom du voisin immédiat
        poids : int
            Pondération de l'arc entre les deux sommets
        """
        self.voisins[voisin] = ponderation
    
    def getVoisins(self) -> dict:
        """Guetteur pour les voisins

        Returns
        -------
        dict
            Dictionnaire avec les voisins immediats et leur pondération
        """
        return self.voisins

class Lycee :
    """Classe modélisant un graphe
    """
    def __init__(self) :
        # On crée un dictionnaire {valeur : objet sommet} pour faciliter l'iteration sur la liste de sommets
        self.sommets = {} # { nomDuSommet : Objet de la classe sommet lui correspondant }
        self.adj = {} # { nomDuSommet : [ Nom des voisins immediats ] }

    def ajoutLieu(self,nom: str) :
        """Méthode pour ajouter un sommet au graphe

        Parameters
        ----------
        valeur : str
            Nom du sommet, représentant ici un lieu
        """
        if nom not in self.sommets : # On verifie que le lieu n'existe pas déjà
            self.sommets[nom] = Lieu(nom)
        if nom not in self.adj : # On verifie que le lieu n'existe pas déjà
            self.adj[nom] = []

    def ajout_arete(self,A: str,B: str,poids: int) :
        """
            Méthode pour ajouter une arete au graphe
            Le graph n'étant pas orienté, on ajoute la connexion dans les deux sens

        Parameters
        ---------
        A : str
            Nom du lieu 1
        B : str
            Nom du lieu 2
        poids : int
            Pondération de l'arete entre A et B
        """
        self.ajoutLieu(A)
        self.ajoutLieu(B)
        self.adj[A].append(B)
        self.adj[B].append(A)
        self.sommets[A].addVoisin(self.sommets[B], poids)
        self.sommets[B].addVoisin(self.sommets[A], poids)

    def get_sommets(self) -> dict:
        """Méthode qui retourne la liste des sommets

        Returns
        -------
        dict
            Dictionnaire avec { Nom du sommet : Objet Sommet lui correspondant }
        """
        return self.sommets

    
    def getAdjPond(self) -> dict:
        """
            Méthode qui retourne un dictionnaire d'adjacence pondéré qui sera utilisé pour djikstra
            Sous la forme : { Sommet : { Voisin : Ponderation } }

        Returns
        -------
        dict
            Dictionnair d'adjacence
        """
        sommets = {}
        for nom_sommet,obj_sommet in self.sommets.items():
            voisins = obj_sommet.voisins
            sommets[nom_sommet] = {
                voisin.nom: poids for voisin, poids in voisins.items()
            }

        return sommets

    def djikstra(self, depart: str) -> dict:
        """Méthode reprenant l'algorithme de Djikstra afin de trouver le meilleur chemin 
           Pour arriver à tous les autres points à partir d'un point

        Parameters
        ----------
        depart : str
            Le poind de départ

        Returns
        -------
        dict
            {
                'precedent' : dictionnaire pour retracer le chemin pris pour trouver le deplacement optimal sous la forme {point precedent : point par lequel il faut passer}
                'distance_minimale' : distance (minimale/optimale) pour arriver à chaque point sous la forme {point : distance}
            }
        """
        precedent= {} # garde la trace des sommets par lesquels il faut passer
        non_visites = self.getAdjPond() # adjacence pondérée du graphe que l'on va parcourir

        inf = float('inf') 

        distance = {lieu: inf for lieu in non_visites}
        distance[depart] =  0 # la distance d'un point vers lui même est 0

        while len(non_visites) > 0:

            lieu_actuel = None # Lieu le plus proche par rapport aux autres

            for lieu in non_visites:
                if lieu_actuel is None or distance[lieu] < distance[lieu_actuel]:
                    lieu_actuel = lieu # On considère le premier sommet de la liste comme le plus proche
            chemins_possibles = self.getAdjPond()[lieu_actuel].items() # Soit les voisins immediats du lieu actuel "de reference"

            for voisin, ponderation in chemins_possibles: # On itere sur les voisins du lieu "de reference" actuel
                if ponderation + distance[lieu_actuel] < distance[voisin]: # Si la somme de la distance du sommet de départ au lieu actuel + la ponderation entre ce dernier 
                    distance[voisin] = ponderation + distance[lieu_actuel] # et son voisin est inferieure à la distance entre le sommet de depart et ce voisin
                    precedent[voisin] = lieu_actuel

            non_visites.pop(lieu_actuel) # Une fois que nous avons terminé avec ce lieu "de reference" on l'enleve des sommets encore à visiter

        return {'precedent' : precedent , 'distance' : distance}
    

def listToStr(toPrint):
    """
    Converts a list of elements into a string with each element separated by ' -> '.

    Args:
        toPrint: List of elements to be converted to a string.

    Returns:
        str: String representation of the elements in the list.
    """

    s = ""
    for e in toPrint:
        s+= " -> "
        s+= e
    return s


def getChemin(graph : Lycee,depart: str,arrivee: str) -> dict:
    """Fonction qui donne le chemin optimal pour aller de depart à arrivee

        Parameters
        ----------
        graph : Lycee
            Graph dans lequel on se situe (ici un lycee)

        depart : str
            Le poind de départ

        arrivee : str
            Le poind d'arrivee

        Returns
        -------
        dict
            {
                'precedent' : dictionnaire pour retracer le chemin pris pour trouver le deplacement optimal sous la forme {point precedent : point par lequel il faut passer}
                'distance_minimale' : distance (minimale/optimale) pour arriver à chaque point sous la forme {point : distance}
            }
        """

    dic = graph.djikstra(depart)
    chemin = []  # chemin le plus rapide par lequel il faut passer
    precedent = dic['precedent']
    distance = dic['distance'][arrivee]
    lieu_actuel = arrivee

    existe = True

    while lieu_actuel !=  depart: # Dans cette boucle on retrace le chemin le plus rapide
        try:    # On verifie que le chemin existe entre les deux points avec une gestion d'erreur
            chemin.insert(0,lieu_actuel)
            lieu_actuel =  precedent[lieu_actuel]
        except  KeyError:
            print ("Il n'y a pas de lien entre les deux lieux")
            existe = False
            break
    
    if existe :
        chemin.insert(0, depart)

        print(f'Le chemin optimal pour arriver à {arrivee} est{listToStr(chemin)} avec une distance de {distance} mètres.')    
        return {'distance' : distance , 'chemin' : chemin}

def entre_deux(graph: Lycee,lieu1: str,lieu2: str) :
    """Fonction pour trouver un point de rencontre entre deux sujets

    Parameters
    ----------
    graph : Lycee
        Graph étudié (Lycee dans le cas échéant)
    lieu1 : str
        Lieu ou se situe le sujet n°1
    lieu2 : str
        Lieu ou se situe le suejt n°2
    """

    dic1 = graph.djikstra(lieu1)
    dic2 = graph.djikstra(lieu2)
    distances1 = dic1['distance']
    distances2 = dic2['distance']

    difference = float('inf') # On pose comme distance de départ l'infini
    lieu_rencontre = None

    for Lieu1 in distances1 :
        if abs(distances1[Lieu1] - distances2[Lieu1]) < difference :
            lieu_rencontre = Lieu1
            difference = abs(distances1[Lieu1] - distances2[Lieu1])
    
    print(f'Le lieu de rencontre optimal pour vous est {lieu_rencontre}')
    print(f"Le sujet se situant à {lieu1} suivra :")
    getChemin(lyautey,lieu1,lieu_rencontre)
    print()
    print(f"Le sujet se situant à {lieu2} suivra :")
    getChemin(lyautey,lieu2,lieu_rencontre)


batiments = [
    'Vie scolaire Lycee',
    'Batiment K',
    'Batiment H',
    'Batiment I',
    'Batiment P',
    'Batiment G',
    'Batiment S',
    'Batiment M',
    'Batiment L',
    'Batiment D',
    'Cafeteria',
    'Preau Cantine',
    'CDI',
    'Infirmerie',
    'Batiment Delacroix'
    ]

lyautey = Lycee()

links = [
    ['Batiment Delacroix','Batiment G', 40],
    ['Batiment G','Infirmerie', 40],
    ['Batiment Delacroix','Batiment I', 80],
    ['Batiment G','Batiment D', 60],
    ['Batiment D','CDI',80],
    ['Batiment S','Batiment D', 65],
    ['Batiment S','Batiment M', 20],
    ['Batiment M','Batiment D', 90],
    ['Batiment M','CDI', 60],
    ["Vie scolaire Lycee", "Bâtiment H" , 50],
    ["Bâtiment I", "Vie scolaire Lycee", 70],
    ["Preau Cantine", "Bâtiment I", 24],
    ["Cafeteria", "Preau Cantine", 20],
    ["Batiment H", "Preau Cantine", 90],
    ["Batiment K", "Batiment H", 20],
    ["Batiment L", "Batiment K", 70],
    ["Batiment M", "Batiment L", 70],
    ["Batiment P", "Batiment L", 40],
    ['Vie Scolaire Lycee', 'Batiment P', 80]
]

for a,b,pond in links :
    lyautey.ajout_arete(a,b,pond)

def clearConsole():
    """
    Clears the console screen based on the operating system.

    Returns:
        None
    """

    os.system('cls' if os.name in {'nt', 'dos'} else 'clear')

def menu():  
    """
    Displays a menu for interacting with "Lyautey Maps" and performs corresponding actions based on user input.

    Returns:
        None
    """

    try:
        actions = [
            '1 - Trouver le chemin optimal à partir d\'un point',
            '2 - Trouver un point de rencontre optimal pour se rejoindre avec un camarade',
            '3 - Consulter la liste des lieux',
            '4 - Consulter les differentes connexions existantes',
            '5 - Ajouter un lieu',
            '6 - Ajouter un chemin entre deux lieux',
            '0 - Pour quitter le menu cliquez simultanement sur Ctrl-C'
        ]
        while True:
            clearAndPrint(
                'Bienvenue sur "Lyautey Maps" ',
                "Trouver le meilleur chemin, c'est la réussite de demain !",
            )
            for action in actions : print(action)
            choix = int(input('Quelle action voulez vous effectuer ? : '))
            if choix in {1, 2, 3, 4, 5, 6, 7}:
                clearConsole()
                if choix == 1:
                    print("Veuillez indiquer un lieu de départ et d'arrivée")
                    print("Réferez-vous à la liste des lieux en tapant 3 au menu précédent en cas de besoin")
                    depart = input('Depart : ')
                    arrivee = input('Arrivee : ')

                    if depart in batiments and arrivee in batiments:
                        getChemin(lyautey,depart,arrivee)
                    else:
                        print("Un des lieux n'existe pas ou a été mal orthographié")
                    input('Cliquez sur entrée pour retourner au menu')
                elif choix == 2:
                    print("Veuillez indiquer où se trouvent les personnes 1 et 2")
                    print("Référez vous à la liste des lieux en tapant 3 au menu précédent en cas de besoins")
                    sujet1 = input('Personne 1 : ')
                    sujet2 = input('Personne 2 : ')
                    entre_deux(lyautey, sujet1, sujet2)
                    input('Cliquez sur Entrée pour retourner au menu')
                elif choix == 3:
                    print('Bâtiments :')
                    for bat in batiments :
                        print(f"- {bat}")
                    input('Cliquez sur Entrée pour retourner au menu')
                elif choix == 4:
                    print('Voici les différentes connexions :')
                    for bat in batiments :
                        for voisin in lyautey.adj[bat] : print(f"{bat} <-> {voisin} ")
                    input('Cliquez sur Entrée pour retourner au menu')
                elif choix == 5:
                    print('Veuiller renseigner le nom du lieu')
                    nom = input('Nom : ')
                    lyautey.ajoutLieu(nom)
                    batiments.append(nom)
                    print('Lieu ajouté !')
                    input('Cliquez sur entrée pour retourner au menu')
                elif choix == 6:
                    print('Veuillez renseigner le nom des lieux à relier et la pondération')
                    lieu1 = input('Lieu 1 : ')
                    lieu2 = input('Lieu 2 : ')
                    pond = int(input('Pondération : '))
                    if lieu1 not in batiments :
                        batiments.append(lieu1)
                    if lieu2 not in batiments :
                        batiments.append(lieu2)
                    lyautey.ajout_arete(lieu1,lieu2,pond)
                    print('Lien ajouté !')
                    input('Cliquez sur entrée pour retourner au menu')
    except KeyboardInterrupt:
        clearAndPrint(
            "Merci d'avoir utilisé Lyautey Maps",
            "Au plaisir de vous revoir le plus vite possible pour vous orienter",
        )

def clearAndPrint(arg0, arg1):
    """
    Prints the given arguments after clearing the console.

    Args:
        arg0: The first argument to be printed.
        arg1: The second argument to be printed.

    Returns:
        None
"""
    clearConsole()
    print(arg0)
    print(arg1)

menu()