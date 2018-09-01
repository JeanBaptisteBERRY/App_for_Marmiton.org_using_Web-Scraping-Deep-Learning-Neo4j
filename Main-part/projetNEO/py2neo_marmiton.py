#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:25:54 2018

@author: camille
"""

from py2neo import Graph



graphURL='http://localhost:7474/db/data/'
graphUser = "neo4j"
graphPassphrase = "DirtyIdols78"

sgraph=Graph(graphURL, user=graphUser, password=graphPassphrase)

ListeIngredient = [u'ketchup',u'persil',u'oeuf']

ingr = ListeIngredient


def recette(ingr):
    for i in range(len(ingr)):
        ingr[i] = ingr[i]
    commande1 = 'MATCH (r:Recette)--(e:Element) WITH r, COLLECT(e.ingredient) AS nomingre WHERE all(x in '
    commande2 = str(ingr)
    commande3 = ' WHERE x in nomingre) RETURN r.name'
    liste_temp=sgraph.data(commande1 + commande2 + commande3)
    ingrf=[]
    for i in range(len(liste_temp)):
        ingrf.append(liste_temp[i]['r.name'])
    return ingrf

def ingredients_manquants(ingr):
    commande1 = "MATCH (r:Recette)--(e:Element) WITH r, COLLECT(e.ingredient) AS nomingre WHERE all(x in "
    commande2 = str(ingr)+ "WHERE x in nomingre) RETURN FILTER(x IN nomingre WHERE x <>"
    commande3 = str(" AND x <>".join(["'"+x + "'" for x in ingr] ))+");"
    liste_temp= sgraph.data(commande1+commande2+commande3)
    for i in range(len(liste_temp)):
        liste_temp[i]=liste_temp[i].values()
        liste_temp[i]=str(liste_temp[i]).encode("utf-8")
        liste_temp[i]=liste_temp[i].replace("[u'","")
        liste_temp[i]=liste_temp[i].replace("']","")
        liste_temp[i]=liste_temp[i].replace('[u"','')
        liste_temp[i]=liste_temp[i].replace('"]','')
    return liste_temp

def affichage(listef):
    #return tuple(listef)
    return ', '.join(listef)


def instructions(x):
    y = '"' + str(x) + '"'
    commande1 = 'MATCH (r:Recette) WHERE r.name = '
    commande2 = str(y)
    commande3 = 'RETURN r.Instructions'
    instru=sgraph.data(commande1 + commande2 + commande3)
    return instru[0]['r.Instructions']
        

def etapes(x):
    #C=[]
    B=[]
    A = instructions(x)
    for i in range(len(A.split(". "))):
        B.append(str(i+1) + ") "+ A.split(". ")[i] + "\n")
    #for j in range(len(B)):
        #C[i] = B[i].encode('utf-8')
    return B
