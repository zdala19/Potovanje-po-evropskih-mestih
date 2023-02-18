import baza_mesta
import sqlite3

conn = sqlite3.connect("baza_potovanj.sqlite3")

#pripravimo vse tabele v primeru, da še ne obstajajo