import csv


PARAM_FMT = ":{}" # za SQLite


class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.
    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    """
    ime = None
    podatki = None

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")

    def uvozi(self):
        """
        Metoda za uvoz podatkov.
        Argumenti:
        - encoding: kodiranje znakov
        """
        if self.podatki is None:
            return
        with open(self.podatki, encoding = 'utf-8') as datoteka:
            podatki = csv.reader(datoteka, delimiter=",")
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
                self.dodaj_vrstico(**vrstica)

    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.
        Argumenti:
        - stolpci: seznam stolpcev
        """
        return f"""
            INSERT INTO {self.ime} ({", ".join(stolpci)})
            VALUES ({", ".join(PARAM_FMT.format(s) for s in stolpci)});
        """

    def dodaj_vrstico(self, **podatki):
        """
        Metoda za dodajanje vrstice.
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items()
                   if vrednost is not None}
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid

class Drzava(Tabela):
    '''
    Tabela vseh držav
    '''
    ime = "drzave"
    podatki = "podatki/evropske_drzave.csv"

    def ustvari(self):
        '''Ustvari tabelo drzave'''
        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS
                drzave(
                ime TEXT,
                kratica TEXT PRIMARY KEY NOT NULL
                )
                """)

class GlavnaMesta(Tabela):
    '''
    Tabela glavnih mest
    '''
    ime = "glavna_mesta"
    podatki = "podatki/glavna_mesta.csv"

    def ustvari(self):
        '''Ustvari tabelo glavna_mesta'''
        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS
                glavna_mesta(
                id INTEGER NOT NULL PRIMARY KEY,
                drzava TEXT,
                kratica TEXT,
                ime TEXT,
                letni_cas TEXT,
                stevilo_dni INTEGER,
                cenovni_rang INTEGER,
                opis TEXT,
                url TEXT)
                """)

class Rang(Tabela):
    '''Tabela rang'''
    ime = "cenovni_rang"
    podatki = "podatki/cenovni_rang.csv"

    def ustvari(self):
        '''Ustvari tabelo cenovnih rangov'''
        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS
                cenovni_rang(
                cena TEXT,
                rang INTEGER
                )
                """)

class GlavnaMestaInDrzave(Tabela):
    """Tabela vseh mest."""
    ime = "gl_mesta_in_drzave"
    podatki = "podatki/gl_mesta_in_drzave.csv"

    def ustvari(self):
        '''Ustvari tabelo glavnih mest in drzav'''
        self.conn.execute("""
                CREATE TABLE IF NOT EXISTS
                gl_mesta_in_drzave(
                id_mesta INTEGER,
                kratica_drzave TEXT
                )
                 """)

class Namen(Tabela):
    "Tabela z vsemi nameni potovanja."
    ime = "namen"
    podatki = "podatki/namen.csv"

    def ustvari(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS
                namen (
                id_mesta INTEGER,
                namen TEXT
                )
            """
        )

class GlavneAtrakcije(Tabela):
    "Tabela z vsemi glavnimi atrakcijami"
    ime = "glavne_atrakcije"
    podatki = "podatki/glavne_atrakcije.csv"

    def ustvari(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS
                glavne_atrakcije (
                id_mesta INTEGER,
                glavna_atrakcija TEXT
                )
            """
        )

class Komentarji(Tabela):
    "Tabela z vsemi podanimi komentarji"
    ime ='komentarji'

    def ustvari(self):
        # KOMENTAR
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS komentar (
                mesto TEXT,
                cas TIMESTAMP,
                ime TEXT NOT NULL,
                komentar TEXT NOT NULL)
            """)

def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    drzave = Drzava(conn)
    glavna_mesta = GlavnaMesta(conn)
    cenovni_rang = Rang(conn)
    gl_mesta_in_drzave = GlavnaMestaInDrzave(conn)
    namen = Namen(conn)
    glavne_atrakcije = GlavneAtrakcije(conn)
    komentarji = Komentarji(conn)

    return [drzave, glavna_mesta, cenovni_rang, gl_mesta_in_drzave, namen, glavne_atrakcije, komentarji]

def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)

def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, ce ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)