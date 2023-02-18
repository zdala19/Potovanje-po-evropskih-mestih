import csv

import sqlite3

db = sqlite3.connect("baza_potovanj.db")

def naredi_tabele(datoteka):
    '''funkcija naredi tabelo iz podatkov v datoteki'''
    tab = []
    with open(datoteka,'r',encoding='utf-8') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for vrstica in csvreader:
            tab.append((vrstica[i] for i in vrstica))
    return tab


############################################################

evropske_drzave = []
with open('evropske_drzave.csv','r',encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
        evropske_drzave.append((vrstica[0],vrstica[1]))

with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                drzave(
                ime TEXT UNIQUE,
                kratica TEXT NOT NULL PRIMARY KEY UNIQUE
                )
                """)

def napolni_drzave():

    with db as cursor:
        for (ime, kratica) in evropske_drzave:
            cursor.execute("""
            INSERT INTO drzave (ime, kratica)
                VALUES(:dr_ime, :dr_kratica)""",{"dr_ime":ime, "dr_kratica":kratica})
##############################################################################################################            
glavna_mesta = []

with open("glavna_mesta.csv", "r",encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
                glavna_mesta.append((vrstica[0],vrstica[3],vrstica[4],vrstica[5],vrstica[6], vrstica[7]))


with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                glavna_mesta(
                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                mesto TEXT,
                letni_cas TEXT,
                stevilo_dni INTEGER,
                cenovni_rang INTEGER,
                opis TEXT)
                """)
    

def napolni_gl_mesta():
   with db as cursor:
       for (id, mesto, letni_cas, stevilo_dni, cenovni_rang,opis) in glavna_mesta:
            cursor.execute("""
            INSERT INTO glavna_mesta (id, mesto, letni_cas, stevilo_dni, cenovni_rang,opis)
               VALUES(:mesto_id, :mesto_ime, :mesto_letnicas, :mesto_stevilodni, :mesto_cenovnirang, :mesto_opis)""",
               {"mesto_id":id, "mesto_ime":mesto, "mesto_letnicas":letni_cas, "mesto_stevilodni": stevilo_dni,
               "mesto_cenovnirang":cenovni_rang, "mesto_opis": opis})

##########################################################################################################           
cenovni_rang = []

with open('cenovni_rang.csv','r',encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
        cenovni_rang.append((vrstica[0],vrstica[1]))

db = sqlite3.connect("baza_potovanj.db")

with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                cenovni_rang(
                cena TEXT,
                rang INTEGER
                )
                """)

def napolni_rang():
    with db as cursor:
        for (cena, rang) in cenovni_rang:
            cursor.execute("""
            INSERT INTO cenovni_rang (cena, rang)
                VALUES(:_cena, :_rang)""",{"_cena":cena, "_rang":rang})

########################################################################################
gl_mesta_in_drzave = []

with open('gl_mesta_in_drzave.csv','r',encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
        gl_mesta_in_drzave.append((vrstica[0],vrstica[1]))

db = sqlite3.connect("baza_potovanj.db")

with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                gl_mesta_in_drzave (
                id_mesta INTEGER NOT NULL PRIMARY KEY,
                kratica_drzave TEXT
                )
                """)

def napolni_gl_mesta_in_drzave():
    with db as cursor:
        for (id_mesta, kratica_drzave) in gl_mesta_in_drzave:
            cursor.execute("""
            INSERT INTO gl_mesta_in_drzave (id_mesta, kratica_drzave)
                VALUES(:_idmesta, :dr_kratica)""",{"_idmesta":id_mesta, "dr_kratica":kratica_drzave})

##########################################################################################################
nameni = []


with open('namen.csv','r',encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
        nameni.append((vrstica[0],vrstica[1]))

with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                namen (
                id_mesta INTEGER UNIQUE,
                namen TEXT
                )
                """)

def napolni_namen():
    with db as cursor:
        for (id_mesta, namen) in nameni:
            cursor.execute("""
            INSERT INTO namen (id_mesta, namen)
                VALUES(:_idmesta, :_namen)""",{"_idmesta":id_mesta, "_namen":namen})

################################################################################################3
glavne_atrakcije = []

with open('glavne_atrakcije.csv','r',encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for vrstica in csvreader:
        glavne_atrakcije.append((vrstica[0],vrstica[1]))


with db as cursor:
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                glavne_atrakcije (
                id_mesta INTEGER,
                glavna_atrakcija TEXT
                )
                """)

def napolni_glavne_atrakcije():
    with db as cursor:
        for (id_mesta, glavna_atrakcija) in glavne_atrakcije:
            cursor.execute("""
            INSERT INTO glavne_atrakcije (id_mesta, glavna_atrakcija)
                VALUES(:_idmesta, :gl_atrakcija)""",{"_idmesta":id_mesta, "gl_atrakcija":glavna_atrakcija})

napolni_drzave()
napolni_gl_mesta()
napolni_rang()
napolni_gl_mesta_in_drzave()
napolni_namen()
napolni_glavne_atrakcije()