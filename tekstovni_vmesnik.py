from pomozne_funkcije import Meni, JaNe, prekinitev
import model

def izberi_moznost(moznosti):
    '''
    Funkcija izpiše seznam možnosti in vrne indeks izbrane možnosti.
    
    Če na voljo ni nobene možnosti, uporabnika o tem opozori ter izpiše None.
    Če je na voljo samo ena možnost, vrne '.
    '''
    
    if len(moznosti) == 0:
        return
    elif len(moznosti) == 1:
        return 0
    else:
        for i, moznost in enumerate(moznosti, 1):
            print(f'{i}) {moznost}')
        
        stevilo_moznosti = len(moznosti)
        while True:
            print()
            izbira = input('Vnesite izbiro > ')
            if not izbira.isdigit():
                print('NAPAKA: vnesti morate število.')
            else:
                n = int(izbira)
                if 1 <= n <= stevilo_moznosti:
                    return n - 1
                else:
                    print(f'NAPAKA: vnesti morate število med 1 in {stevilo_moznosti}!')

#IZBIRA 0
def izberi_mesto():
    print()
    niz = input("Vnesite del naziva mesta > ")
    idji_mest = model.poisci_mesto(niz)
    print()
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    return None if izbira is None else idji_mest[izbira]

def prikazi_podatke_mest():
    id_mest = izberi_mesto()
    if id_mest is None:
        print("Nobeno mesto ne ustreza iskanemu nizu.")
        print()
    else:
        izpis_podatkov_mesta(id_mest)

# IZBIRA 1 - glede na letni čas
        
def poisci_mesta_letni_čas():
    letni_časi_obiska = ['Poletje', 'Zima', 'Jesen', 'Pomlad']
    izbira = izberi_moznost(letni_časi_obiska)
    letni_čas_obiska = letni_časi_obiska[izbira]
    
    idji_mest = model.mesta_glede_na_letni_cas(letni_čas_obiska)
    print()
    print(f"Mesta s primernim časom obiska ({letni_čas_obiska}): ")
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    id_mesta = idji_mest[izbira]
    izpis_podatkov_mesta(id_mesta)    

# IZBIRA 2 - glede na število dni
def poisci_mesta_št_dni():
    st_dni_obiska = ['1','2','3','4','5','6']
    izbira = izberi_moznost(st_dni_obiska)
    st_dni_obiska_mes = st_dni_obiska[izbira]
    
    idji_mest = model.mesta_glede_na_stevilo_dni(st_dni_obiska_mes)
    print()
    print(f"Mesta s primernim časom obiska ({st_dni_obiska_mes}): ")
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    id_mesta = idji_mest[izbira]
    izpis_podatkov_mesta(id_mesta)    

# IZBIRA 3 - glede na cenovni rang
def poisci_mesta_cenovni_rang():
    cenovni_rang_potovanja = ['100€ ali manj', '100€ - 250€', '250€+']
    izbira = izberi_moznost(cenovni_rang_potovanja)
    cenovni_r_obiska = cenovni_rang_potovanja[izbira]
    
    idji_mest = model.mesta_glede_na_cenovni_rang(cenovni_r_obiska)
    print()
    print(f"Mesta s primernim cenovnim rangom obiska ({cenovni_r_obiska}): ")
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    id_mesta = idji_mest[izbira]
    izpis_podatkov_mesta(id_mesta)

# IZBIRA 4 - glede na namen obiska
def poisci_mesta_namen_obiska():
    nameni = ['zgodovina','narava','šport','kulinarika','arhitektura','umetnost','nakupovanje','zabava','plaža','glasba']
    izbira = izberi_moznost(nameni)
    nameni_potovanja = nameni[izbira]
    
    idji_mest = model.mesta_glede_na_namen(nameni_potovanja)
    print()
    print(f"Mesta s primernim namenom obiska ({nameni_potovanja}): ")
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    id_mesta = idji_mest[izbira]
    izpis_podatkov_mesta(id_mesta) 

#IZBIRA 5 - glede na glavne atrakcije
def poisci_mesta_glavne_atrakcije():
    glavne_atrakcije = ['znamenitosti','bližina morja','parki','muzeji','živalski vrt','gradovi','kopališča','jezera']
    izbira = izberi_moznost(glavne_atrakcije)
    glavne_atrakcije_mest = glavne_atrakcije[izbira]
    
    idji_mest = model.mesta_glede_na_glavne_atrakcije(glavne_atrakcije_mest)
    print()
    print(f"Mesta s primernimi glavnimi atrakcijami ({glavne_atrakcije_mest}): ")
    moznosti = [
        "{} ({})".format(ime, drzava) for _, ime, drzava in model.podatki_mest(idji_mest)
        ]
    izbira = izberi_moznost(moznosti)
    id_mesta = idji_mest[izbira]
    izpis_podatkov_mesta(id_mesta) 



def izpis_podatkov_mesta(id_mest):
    '''
    Funkcija prejme ID mesta in izpiše vse njene podatke.
    '''
    print()
    mesto, drzava, letni_cas, stevilo_dni, opis, url = model.podatki_mesta(id_mest)
    letni_cas_obiska = model.cas_obiska_mesta(id_mest)
    cenovni_rang = model.cenovni_rang_mesta(id_mest)
    stevilo_dni_obiska = model.stevilo_dni_obiska_mesta(id_mest)
    opis = model.opis_mesta(id_mest)


    dolžina_naziva = len(mesto) + len(drzava) + 2
    print(dolžina_naziva * '*')
    print(f"{mesto}, {drzava}")
    print(dolžina_naziva * '*')
    
    print(f"   > Letni čas: {letni_cas_obiska}")
    print(f"   > Število dni: {stevilo_dni_obiska}")
    print(f"   > Cenovni rang: {cenovni_rang}")
    print(f"   > Opis mesta: {opis}")
    print()

#MENI (izbire):
def prikazi_moznosti():
    print(50 * '-')
    print('Kaj vas zanima?')
    izbira = izberi_moznost([
        'prikaži podatke mesta',
        'prikaži mesta glede na letni čas obiska',
        'prikaži mesta glede na število dni obiska',
        'prikaži mesta glede na cenovni rang',
        'prikaži mesta glede na namen obiska',
        'prikaži mesta glede na glavne atrakcije',
        'izhod',
        ])
    if izbira == 0:
        prikazi_podatke_mest()
    elif izbira == 1:
        poisci_mesta_letni_čas()
    elif izbira == 2:
        poisci_mesta_št_dni()
    elif izbira == 3:
        poisci_mesta_cenovni_rang()
    elif izbira == 4:
        poisci_mesta_namen_obiska()
    elif izbira == 5:
        poisci_mesta_glavne_atrakcije()
    elif izbira == 6:
        print('Nasvidenje')
        exit()

def main():
    print('Pozdravljeni v bazi mest!')
    while True:
        prikazi_moznosti()

main()