# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:02:14 2020

@author: Perrotin
"""
import numpy as np
from colorama import Fore, Style


class Ruler:

    '''
    On construit ici une classe qui va permettre de déterminer la distance 
    entre deux brins d'ADN. On peut avoir la distance et aussi la comparaison 
    de deux brins (remplacements, alignements, effacements, insertions).
    '''

    def __init__(self, ch1, ch2):
        '''
        On prend les coûts suivants :
            al=0  pas de bonification d'alignement
            rem=1 malus de remplacement
            gap=1 malus d'insertion ou d'effacement
        '''
        self.ch1 = ch1
        self.ch2 = ch2
        self.distance = 0
        self.al = 0
        self.rem = 1
        self.gap = 1
        self.A = 0  # Matrice qui sert dans compute et report

    def compute(self):
        '''
        Fonction qui va permettre d'obtenir la distance minimale entre deux
        chaines de caractères, et la matrice A qui va permettre de construire 
        l'alignement.
        '''

        al = self.al
        rem = self.rem
        gap = self.gap
        ch1 = self.ch1
        ch2 = self.ch2

        m = len(ch1)
        n = len(ch2)
        # Matrice qui va nous permettre de comparer les chaines
        A = np.zeros((m+1, n+1))

        '''
        La première ligne et la première colonne de la matrice sont complétées 
        par des valeurs qui correspondent à une insertion/effacement en plus
        effectué à chaque passage de caractère.
        '''

        for i in range(m+1):
            A[i, 0] = i*gap

        for j in range(n+1):
            A[0, j] = j*gap

        '''
        On complète ensuite le reste de la matrice selon 
        '''

        for i in range(1, m+1):
            for j in range(1, n+1):

                # On regarde d'abord si on a un alignement
                if ch1[i-1] == ch2[j-1]:
                    S = al

                else:
                    S = rem

                allignement = A[i-1, j-1]+S
                effacement = A[i-1, j]+gap
                insertion = A[i, j-1]+gap
                A[i, j] = min(allignement, effacement, insertion)

        # Ce coefficient représente le chemin ayant le coût minimal pour 
        # parcourir les deux chaines, c'est donc la distance.
        self.distance = A[m, n]
        self.A = A

    def report(self):
        '''
        Report se charge de remonter la matrice pour comparer les deux chaines\
        et renvoie en sortie top et bottom qui sont les chaines de caractères\
        modifiées
        '''

        def red_text(text):
            return f"{Fore.RED}{text}{Style.RESET_ALL}"

        ch1 = self.ch1
        ch2 = self.ch2
        A = self.A

        top = []
        bottom = []  # On crée des listes et non des str pour que la couleur
                     # s'affiche 

        i, j = np.shape(A)
        i -= 1 
        j -= 1

        al = 0
        rem = 1
        gap = 1

        # On va parcourir la matrice mais aussi les str grâce à i et j 

        while i > 0 and j > 0:  # lorsqu'on touche un bord de la matrice

            distance_actuelle = A[i, j]
            alignement_diag = A[i-1, j-1]
            insertion = A[i, j-1]
            effacement = A[i-1, j]

            # Il faut maintenant trouver la case qui a permis d'aboutir à
            # notre case A[i,j]
            # Puis on passera à cette case en question.

            if ch1[i-1] == ch2[j-1]:
                S = al

            else:
                S = rem

            if distance_actuelle == alignement_diag + S:

                if S == rem:
                    top += [red_text(ch1[i-1])]
                    bottom += [red_text(ch2[j-1])]

                else:
                    top += [ch1[i-1]]
                    bottom += [ch2[j-1]]
                i -= 1
                j -= 1

            elif distance_actuelle == insertion + gap:
                bottom += [ch2[j-1]]
                top += [red_text('=')]
                j -= 1

            elif distance_actuelle == effacement + gap:
                bottom += [red_text('=')]
                top += [ch1[i-1]]
                i -= 1

        # On gère enfin le cas où on arrive sur un bord de la matrice
        # Il faut alors mettre des '-'

        while i > 0:

            top += [ch1[i-1]]
            bottom += [red_text('=')]
            i -= 1

        while j > 0:

            top += [red_text('=')]
            bottom += [ch2[i-1]]
            j -= 1

        # Le problème, c'est qu'on a parcouru de la fin au début les chaines
        # de caractère, donc il va falloir les renverser.

        top.reverse()
        bottom.reverse()

        # On crée une f string pour afficher la couleur avec un print

        top = f"".join(top)
        bottom = f"".join(bottom)

        return(top, bottom)


#ch1 = 'ACGT'*250 + 'C'
#ch2 = 'ACGT'*250 + 'G'
#
#ruler = Ruler(ch1,ch2)
#ruler.compute()
#top,bottom = ruler.report()
#print(ruler.distance)
#print(top)
#print(bottom)
