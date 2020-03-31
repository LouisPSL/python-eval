# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:07:35 2020

@author: Perrotin
"""


class TreeBuilder:

    '''
    Dans cette classe, on va représenter les noeuds de l'arbre binaire avec ces données :
    symbol : lettre de l'alphabet à encoder
    freq : représentation de sa fréquence
    left et right : noeuds fils, contenant None s'il n'y en a pas. Left a la plus faible occurence
    father : noeud père
    On aura donc node = (symbol, freq, left, right, father)
    '''
    
    def __init__(self, text):
        self.text = text

    

    def freq_list(self):
        '''
        Fonction chargée de donner deux listes symbols et freqs, associées, contenant respectivement les caractères d'un texte
        et leur fréquence d'apparition
        '''
        text = self.text

        frequences = dict()
        for elt in text:
            if elt not in frequences:
                frequences[elt] = 1
            else:
                frequences[elt] += 1

        frequences = sorted(frequences.items(), key=lambda x: x[1])
        freqs = [qtt for lettre, qtt in frequences]
        symbols = [lettre for lettre, qtt in frequences]

        return freqs, symbols

    def createTree(self, symbols, freqs):
        '''
        Cette méthode permet de créer l'arbre de Huffman, ses entrées sont deux listes
        de même longueur, contenant respectivement les symboles de l'alphabet et leurs
        fréquences.

        On suppose par ailleurs que freqs est triée. 
        '''

        Nodes = []  # Liste qui va contenir l'ensemble de noeuds

        father = symbols[0] + symbols[1]
        Nodes.append([symbols[0], freqs[0], None, None, father])
        Nodes.append([symbols[1], freqs[1], None, None, father])
        Nodes.append([father, freqs[0] + freqs[1],
                      symbols[0], symbols[1], None])

        symbols.append(symbols[0] + symbols[1])
        freqs.append(freqs[0] + freqs[1])

        del symbols[0]
        del symbols[0]

        del freqs[0]
        del freqs[0]

        while len(freqs) > 1:

            '''
            On va d'abord chercher les deux minimums de freqs, avec leur position min = (valeur, position)
            '''
            # Premier minimum
            min_freq = (freqs[0], 0)

            for i in range(len(freqs)):
                if freqs[i] < min_freq[0]:
                    min_freq = (freqs[i], i)

            pos = min_freq[1]
            val = min_freq[0]

            node1 = [symbols[pos], val, None, None, None]
            # On laisse le father en None avant de le trouver

            del symbols[pos]
            del freqs[pos]

            # Second minimum
            min_freq = (freqs[0], 0)

            for i in range(len(freqs)):
                if freqs[i] < min_freq[0]:
                    min_freq = (freqs[i], i)

            pos = min_freq[1]
            val = min_freq[0]

            node2 = [symbols[pos], val, None, None, None]
            # On laisse le father en None avant de le trouver

            del symbols[pos]
            del freqs[pos]

            # On connait maintenant le père
            father = node1[0] + node2[0]
            node1[4] = father
            node2[4] = father

            # si les noeuds qu'on a trouvé sont des lettres, on les ajoute à notre liste
            # Sinon, on cherche les noeuds dans Nodes et on leur rajoute leur père
            if len(node1[0]) == 1:
                Nodes.append(node1)
            else:
                for node in Nodes:
                    if node[0] == node1[0]:
                        node[4] = father

            if len(node2[0]) == 1:
                Nodes.append(node2)
            else:
                for node in Nodes:
                    if node[0] == node2[0]:
                        node[4] = father

            # On crée le nouveau noeud
            symbol = node1[0] + node2[0]
            val = node1[1] + node2[1]

            # On complètera le père quand on le connaitra, jamais si c'est la racine
            if node1[1] <= node2[1]:
                Nodes.append([symbol, val, node1[0], node2[0], None])

            else:
                Nodes.append([symbol, val, node2[0], node1[0], None])

            symbols.append(symbol)
            freqs.append(val)

        return Nodes

    def tree(self):
        '''
        Cette fonction va rassembler toutes les fonctions précédente pour créer l'arbre de Huffman associé au 
        texte à encoder
        '''
        Occurences = self.freq_list()
        symbols = Occurences[1]
        freqs = Occurences[0]
        return self.createTree(symbols, freqs)


class Codec:
    '''
    Classe chargée, à partir d'un arbre de Huffman, encoder un texte puis le décoder
    '''

    def __init__(self, binary_tree):
        '''
        Codages sera un dictionnaire qui va contenir l'ensemble de code correspondant aux lettre
        '''
        self.tree = binary_tree
        self.Codages = None

    def list_letters(self):
        '''
        Fonction chargée de retrouver la liste des caractères présents dans l'arbre
        '''
        tree = self.tree
        symbols = []

        for node in tree:
            if len(node[0]) == 1:  # Si la longueur est de 1, alors on a à faire à une lettre
                symbols.append(node[0])

        return symbols

    def cherche(self, Nodes, letter):
        '''
        fonction qui va chercher et renvoyer le noeud associé à letter
        '''
        for node in Nodes:
            if node[0] == letter:
                return node

    def createCode(self, Nodes, symbols):
        '''
        Fonction qui prend en argument un arbe de Huffman et qui retourne
        les codages binaires des symboles de a à z.
        Pour cela, on va parcourir la liste symbols contenant les lettres du texte et associer 
        à chacune un codage en fonctionde son chemin dans l'arbre, ici appelé Nodes
        '''
        Codages = dict()

        for letter in symbols:

            # On cherche le premier père de notre lettre
            Node_letter = self.cherche(Nodes, letter)
            father = Node_letter[4]

            # On cherche le noeuds père du père
            Node_fath = self.cherche(Nodes, father)

            # On cherche si notre lettre est le fils gauche (codage 0) ou droit (codage 1) du père
            if Node_fath[2] == letter:
                codage = '0'
            else:
                codage = '1'

            # On définit un nouveau père, et fils devient l'ancien père
            fils = father
            father = Node_fath[4]

            while father != None:  # Seule la racine a un father = None, donc tant qu'on n'est pas sur la racine
                Node_fath = self.cherche(Nodes, father)

                # On cherche si notre lettre est le fils gauche (codage 0) ou droit (codage 1) du père
                if Node_fath[2] == fils:
                    codage += '0'
                else:
                    codage += '1'

                fils = father
                father = Node_fath[4]

            # Il faut renverser codage come on l'a construit en sens inverse
            Codages[letter] = codage[::-1]

        self.Codages = Codages

    def encode(self, text):
        '''
        On traduit le texte en binaire selon le code Huffman
        '''
        symbols = self.list_letters()
        self.createCode(self.tree, symbols)
        Codages = self.Codages

        encoded = ''

        for letter in text:
            encoded += Codages[letter]

        return encoded

    def decode(self, encoded):
        '''
        Fonction qui va décoder un code binaire pour donner le texte d'origine
        '''
        Nodes = self.tree

        text = ''
        compt = 0

        while compt < len(encoded):
            # On va d'abord chercher le premier fil
            if encoded[compt] == '0':
                fils = Nodes[-1][2]
                # La façon dont j'ai codé CreateTree fait que la racine se trouvera toujours en dernière position

            else:
                fils = Nodes[-1][3]

            # Une fois qu'on a trouvé le fils et son noeud, on avance le compteur
            compt += 1
            Node_fils = self.cherche(Nodes, fils)

            # Si c'est le cas, c'est que notre noeud n'a pas de fils et donc c'est
            while Node_fils[2] != None:
                                         # une lettre

                # Cette fois ci on cherche le fils du noeud actuel, qui s'appelle Node_fils

                if encoded[compt] == '0':
                    fils = Node_fils[2]

                else:
                    fils = Node_fils[3]

                # Une fois qu'on a trouvé le fils et son noeud, on avance le compteur que si le fils existe
                # vraiment
                compt += 1

                Node_fils = self.cherche(Nodes, fils)

            # Une fois qu'on a trouvé une lettre, on l'ajoute au texte
            # La lettre qu'on a trouvé est le symbole de Node_fils
            text += Node_fils[0]

        return text



#text = "a dead dad ceded a bad babe a beaded abaca bed"
#
## on analyse les fréquences d'occurrence dans text
## pour fabriquer un arbre binaire
#builder = TreeBuilder(text)
#binary_tree = builder.tree()
#
## on passe l'arbre binaire à un encodeur/décodeur
#codec = Codec(binary_tree)
## qui permet d'encoder
#encoded = codec.encode(text)
## et de décoder
#decoded = codec.decode(encoded)
## si cette assertion est fausse il y a un gros problème avec le code
#assert text == decoded
#
## on affiche le résultat
#print(f"{text}\n{encoded}")
#if decoded != text:
#    print("OOPS")