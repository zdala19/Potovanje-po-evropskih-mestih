import baza_mesta
import sqlite3

conn = sqlite3.connect("baza_potovanj.sqlite3")
baza_mesta.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

#iskanje mest glede na letni cas
def mesta_glede_na_letni_cas(letni_cas):
    '''
    Funkcija izpiše vsa mesta glede na letni čas
    '''
    poizvedba = '''
    SELECT id
    FROM glavna_mesta 
    WHERE letni_cas = ?
    ORDER BY id
    '''
    id_mest = []
    for (id_mesta,) in conn.execute(poizvedba, [letni_cas]):
        id_mest.append(id_mesta)
    return id_mest

def cas_obiska_mesta(id_mesta):
    '''
    Funkcija vrne vse primerne čase obiska lokacije, ki ima podan ID.
    '''
    poizvedba = """
        SELECT letni_cas
        FROM glavna_mesta
        WHERE id = ?
    """
    letni_cas_potovanja = []
    for (letni_cas_mesto,) in conn.execute(poizvedba, [id_mesta]):
        letni_cas_potovanja.append(letni_cas_mesto)
    return letni_cas_potovanja

#iskanje mest glede na namen
def mesta_glede_na_namen(namen):
    '''
    Funkcija izpiše id mest glede na namen
    '''
    poizvedba = '''
        SELECT DISTINCT glavna_mesta.id 
        FROM glavna_mesta
        JOIN namen ON glavna_mesta.id = namen.id_mesta
        WHERE namen = ?  
    '''
    id_mest = []
    for (id_mesta,) in conn.execute(poizvedba, [namen]):
        id_mest.append(id_mesta)
    return id_mest

def nameni_mest(id_mesta):
    '''
    Funkcija vrne vse namene obiska mesta, katerega id je podan
    '''
    poizvedba = '''
        SELECT namen.namen 
        FROM namen
        JOIN glavna_mesta ON namen.id_mesta = glavna_mesta.id
        WHERE glavna_mesta.id = ? 
    '''
    nameni_mesta = []
    for (namen_mesta,) in conn.execute(poizvedba, [id_mesta]):
        nameni_mesta.append(namen_mesta)
    return nameni_mesta



#iskanje mest glede na cenovni_rang
def mesta_glede_na_cenovni_rang(id_mesta):
    '''
     Funkcija izpiše vsa mesta glede na cenovni rang
    '''
    poizvedba = '''
    SELECT id
    FROM glavna_mesta
       JOIN
       cenovni_rang ON glavna_mesta.cenovni_rang = cenovni_rang.rang
    WHERE cenovni_rang.cena = ?
    '''
    cenovni_rangi = []
    for (cenovni_rang,) in conn.execute(poizvedba, [id_mesta]):
        cenovni_rangi.append(cenovni_rang)
    return cenovni_rangi

#iskanje mest glede na stevilo dni
def mesta_glede_na_stevilo_dni(stevilo_dni):
    '''
    Funkcija izpiše vsa mesta glede na število dni
    '''
    poizvedba = '''
    SELECT id
    FROM glavna_mesta 
    WHERE stevilo_dni = ?
    '''
    id_mest = []
    for (id_mesta,) in conn.execute(poizvedba, [stevilo_dni]):
        id_mest.append(id_mesta)
    return id_mest

def stevilo_dni_obiska_mesta(id_mesta):
    '''
    Funkcija vrne vsa stevila dni potovanja, ki ima podan ID.
    '''
    poizvedba = """
        SELECT stevilo_dni
        FROM glavna_mesta
        WHERE id = ?
    """
    stevilo_dni_potovanja = []
    for (stevilo_dni_mesto,) in conn.execute(poizvedba, [id_mesta]):
        stevilo_dni_potovanja.append(stevilo_dni_mesto)
    return stevilo_dni_potovanja

#iskanje mest glede na glavne atrakcije
def mesta_glede_na_glavne_atrakcije(glavna_atrakcija):
    '''
    Funkcija izpiše vsa mesta glede na glavne atrakcije
    '''
    poizvedba = '''
        SELECT glavna_mesta.id
        FROM glavna_mesta
        JOIN glavne_atrakcije ON glavna_mesta.id = glavne_atrakcije.id_mesta
        WHERE glavne_atrakcije.glavna_atrakcija = ?
        '''

    id_mest = []
    for (id_mesta,) in conn.execute(poizvedba, [glavna_atrakcija]):
        id_mest.append(id_mesta)
    return id_mest

def glavne_atrakcije_mest(id_mesta):
    '''
    FUnkcija vrne vse glavne atrakcije mesta, katerga id je podan.
    '''
    poizvedba = '''
    SELECT glavne_atrakcije.glavna_atrakcija 
    FROM glavne_atrakcije
    JOIN glavna_mesta ON glavne_atrakcije.id_mesta = glavna_mesta.id
    WHERE glavna_mesta.id = ? 
    '''
    glavne_atrakcije_mesta = []
    for (atrakcija,) in conn.execute(poizvedba, [id_mesta]):
        glavne_atrakcije_mesta.append(atrakcija)
    return glavne_atrakcije_mesta

def mesta_glede_na_zelje(stevilo_dni, letni_cas, cena):
    '''Funkcija vrne id mest glede na posameznikove zelje'''
    poizvedba = '''SELECT distinct id 
                   FROM glavna_mesta 
                   JOIN cenovni_rang ON glavna_mesta.cenovni_rang = cenovni_rang.rang
                   JOIN glavne_atrakcije ON glavna_mesta.id = glavne_atrakcije.id_mesta
                   JOIN namen ON glavna_mesta.id = namen.id_mesta
                   WHERE stevilo_dni = ? AND letni_cas = ? AND cena = ? '''
    id_mest = []
    for (id_mesta,) in conn.execute(poizvedba, [stevilo_dni, letni_cas, cena]):
        id_mest.append(id_mesta)
    return id_mest

#izpis opisa mesta
def opis_mesta(id_mesta):
    '''
    Funkcija vrne opis mesta glede na željeno izbiro mesto.
    '''
    poizvedba = '''SELECT opis
                   FROM glavna_mesta
                   WHERE id = ?'''
    opis_mesta = []
    for (opis_m,) in conn.execute(poizvedba, [id_mesta]):
        opis_mesta.append(opis_m)
    return opis_mesta

#komentarji

   
def dobi_vse_komentarje(id_mesta):
    with conn:
        cursor = conn.execute("""                
            SELECT komentar.mesto, komentar.cas, komentar.ime, komentar.komentar 
            FROM komentar 
            JOIN glavna_mesta
            ON glavna_mesta.ime = komentar.mesto
            WHERE glavna_mesta.id=?""", [id_mesta])
        podatki = list(cursor.fetchall())
    return [(pod[0], pod[1], pod[2], pod[3]) for pod in podatki]
    

# Shrani komentar v bazo za doloceno mesto
def shrani_komentar(mesto,cas,ime,komentar):
    '''Shrani komentar v bazo'''
    poizvedba = """
        INSERT INTO komentar (mesto, cas, ime, komentar) VALUES (?,?,?,?)
        """
    conn.execute(poizvedba,[mesto,cas,ime,komentar])


def poisci_mesto(niz):
    '''
    Funkcija vrne id-je vseh mest, katerih naziv vsebuje dani niz.
    '''
    
    poizvedba = """
        SELECT id
        FROM glavna_mesta
        WHERE ime LIKE ?
        ORDER BY id
    """
    idji_mest = []
    for(id_mesta,) in conn.execute(poizvedba, ['%' + niz + '%']):
        idji_mest.append(id_mesta)
    return idji_mest


def isci_vsa_mesta():
    '''Funkcija poisce vsa mesta v bazi in vrne njihove idje in imena.'''
    isci = conn.cursor()
    poizvedba = "SELECT * FROM glavna_mesta"
    isci.execute(poizvedba)
    mesto = isci.fetchall()
    isci.close()
    return mesto #vrne id in ime mesta  


def isci_po_bazi():
    '''Funkcija poisce po bazi ustrezno drzavo/mesto'''
    isci = conn.cursor()
    poizvedba = 'SELECT ime, drzava FROM glavna_mesta WHERE ime LIKE %?% or drzava LIKE %?%'
    isci.execute(poizvedba)
    mesto = isci.fetchall()
    isci.close()
    return mesto

# IZPISOVANJE PODATKOV MEST       
def podatki_mest(idji_mest):
    """
    Funkcija vrne osnovne podatke vseh mest z danimi IDji.
    """
    poizvedba = """
        SELECT id, ime, drzava
        FROM glavna_mesta
        WHERE id IN ({})
    """.format(', '.join('?' for _ in range(len(idji_mest))))
    return conn.execute(poizvedba, idji_mest).fetchall()

def podatki_mesta(id_mesta):
    """
    Funkcije vrne podatke o mestu z podanim idjem
    """
    poizvedba = """
        SELECT ime, drzava, letni_cas, stevilo_dni, opis, url
        FROM glavna_mesta
        WHERE id = ?
        """
    
    osnovni_podatki = conn.execute(poizvedba,[id_mesta]).fetchone()
    if osnovni_podatki is None:
        return None
    else:
        mesto, drzava, letni_cas, stevilo_dni, opis, url = osnovni_podatki
    return mesto, drzava, letni_cas, stevilo_dni, opis, url 