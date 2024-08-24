import bottle
import model
from datetime import date 


@bottle.get('/')
def zacetna_stran():
    return bottle.template('views/zacetek.html')


@bottle.get('/vsa_mesta')
def seznam_mest():
    podatki = model.isci_vsa_mesta()
    idji_mest = []
    imena_mest = []
    for i in podatki:
        idji_mest.append(i[0])
        imena_mest.append(i[3])
    return bottle.template('views/vsa_mesta.html', idji = idji_mest, mesta = imena_mest)


@bottle.get('/vsa_mesta_vmesna/<id>')
def podatki_vseh_mest(id):
    '''Izpiše vse podatke o mestu.'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki,kom = komentarji)

@bottle.post('/vsa_mesta_vmesna/<id>')
def shrani_komentar(id):
    mesto = bottle.request.forms.getunicode('mesto')
    ime = bottle.request.forms.ime
    komentar = bottle.request.forms.komentar
    trenuten_datum = date.today()
    #Shrani v bazo
    model.shrani_komentar(mesto, trenuten_datum, ime, komentar)
    bottle.redirect('/komentarji')
   


#odpre se prva stran
@bottle.get('/zacetek')
def zacetek():
    return bottle.template('views/zacetek.html')

#KOMENTARJI
@bottle.get('/komentarji')
def komentarji():
    '''Odpre okno za možnost komentiranja'''
    return bottle.template('views/komentarji.html')
    
#NAMEN POTOVANJA
@bottle.get('/namen_potovanja')
def namen_potovanja():
    '''Iskanje glede na namen potovanja.'''
    return bottle.template('views/namen_potovanja.html')

@bottle.post('/namen_potovanja')
def iskanje_namen_post():
    '''Prebere izbiro namena potovanja in potem poišče vsa mesta,ki imajo dani namen obiska'''
    namen = bottle.request.forms.getunicode('namen')
    id_mesta_po_namenu = model.mesta_glede_na_namen(namen)
    mes_po_namenu = []
    for i in id_mesta_po_namenu:
        podatki_po_namenu = model.podatki_mesta(i)
        mes_po_namenu.append(podatki_po_namenu[0])
    return bottle.template('views/izpisi_mesta_po_namenu.html', mesta_po_namenu = mes_po_namenu, idji_po_namenu = id_mesta_po_namenu)

@bottle.get('/izpisi_podatke_mesta_vmesna/<id>')
def podatki_mesta_po_namenu(id):
    '''Izpiše podatke ustrezne lokacije poiskane glede na namen obiska.'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom=komentarji)


#ČAS POTOVANJA
@bottle.get('/letni_cas')
def namen_potovanja():
    '''Iskanje glede na letni čas potovanja.'''
    return bottle.template('views/letni_cas.html')

@bottle.post('/letni_cas')
def iskanje_letnega_casa_post():
    '''Prebere izbiro letnega casa potovanja in potem poišče vsa mesta,ki imajo dani letni cas obiska'''
    letni_cas = bottle.request.forms.getunicode('letni_cas')
    id_mesta_po_letnem_casu = model.mesta_glede_na_letni_cas(letni_cas)
    mes_po_letnem_casu = []
    for i in id_mesta_po_letnem_casu:
        podatki_po_letnem_casu = model.podatki_mesta(i)
        mes_po_letnem_casu.append(podatki_po_letnem_casu[0])
    return bottle.template('views/izpisi_mesta_po_letnem_casu.html', mesta_po_letnem_casu = mes_po_letnem_casu, idji_po_letnem_casu = id_mesta_po_letnem_casu)

@bottle.get('/izpisi_podatke_mesta_po_casu_vmesna/<id>')
def podatki_mesta_po_namenu(id):
    '''Izpiše podatke ustrezna mesta glede na letni čas potovanja'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom=komentarji)   

#CENOVNI RANG
@bottle.get('/cenovni_rang')
def cenovni_rang_potovanja():
    '''Iskanje glede na cenovni rang potovanja.'''
    
    return bottle.template('views/cenovni_rang.html')

@bottle.post('/cenovni_rang')
def iskanje_cenovnega_ranga_post():
    '''Prebere izbiro cenovnega ranga potovanja in potem poišče vsa mesta,ki imajo dani cenovni rang'''
    cenovni_rang = bottle.request.forms.getunicode('cenovni_rang')
    id_mesta_po_cenovnem_rangu = model.mesta_glede_na_cenovni_rang(cenovni_rang)
    mes_po_cenovnem_rangu = []
    for i in id_mesta_po_cenovnem_rangu:
        podatki_po_cenovnem_rangu = model.podatki_mesta(i)
        mes_po_cenovnem_rangu.append(podatki_po_cenovnem_rangu[0])
    return bottle.template('views/izpisi_mesta_po_cenovnem_rangu.html', mesta_po_cenovnem_rangu = mes_po_cenovnem_rangu, idji_po_cenovnem_rangu = id_mesta_po_cenovnem_rangu)

@bottle.get('/izpisi_podatke_mesta_cenovni_rang_vmesna/<id>')
def podatki_mesta_po_cenovnem_rangu(id):
    '''Izpiše podatke ustrezna mesta glede na cenovni rang potovanja'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom=komentarji)  

#STEVILO DNI
@bottle.get('/stevilo_dni')
def namen_potovanja():
    '''Iskanje glede na število dni potovanja.'''
    return bottle.template('views/stevilo_dni.html')

@bottle.post('/stevilo_dni')
def iskanje_stevila_dni_post():
    '''Prebere izbiro števila dni potovanja in potem poišče vsa mesta,ki imajo dani letni cas obiska'''
    stevilo_dni = bottle.request.forms.getunicode('st_dni')
    id_mesta_po_stevilu_dni = model.mesta_glede_na_stevilo_dni(stevilo_dni)
    mes_po_stevilu_dni = []
    for i in id_mesta_po_stevilu_dni:
        podatki_po_stevilu_dni = model.podatki_mesta(i)
        mes_po_stevilu_dni.append(podatki_po_stevilu_dni[0])
    return bottle.template('views/izpisi_mesta_po_stevilu_dni.html', mesta_po_stevilu_dni = mes_po_stevilu_dni, idji_po_stevilu_dni = id_mesta_po_stevilu_dni)

@bottle.get('/izpisi_podatke_stevila_dni_vmesna/<id>')
def podatki_mesta_po_stevilu_dni(id):
    '''Izpiše podatke ustrezna mesta glede na število dni potovanja'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom=komentarji)  

#GLAVNE ATRAKCIJE
@bottle.get('/glavne_atrakcije')
def glavne_atrakcije_potovanja():
    '''Iskanje glede na glavne atrakcije potovanja.'''
    return bottle.template('views/glavne_atrakcije.html')

@bottle.post('/glavne_atrakcije')
def iskanje_glavnih_atrakcij_post():
    '''Prebere izbiro cenovnega ranga potovanja in potem poišče vsa mesta,ki imajo dani cenovni rang obiska'''
    atrakcije = bottle.request.forms.getunicode('glavne_atrakcije')
    id_mesta_po_atrakciji = model.mesta_glede_na_glavne_atrakcije(atrakcije)
    mes_po_glavnih_atrakcijah = []
    for i in id_mesta_po_atrakciji:
        podatki_po_glavnih_atrakcijah = model.podatki_mesta(i)
        mes_po_glavnih_atrakcijah.append(podatki_po_glavnih_atrakcijah[0])
    return bottle.template('views/izpisi_mesta_po_glavnih_atrakcijah.html', mesta_po_glavnih_atrakcijah = mes_po_glavnih_atrakcijah, idji_po_glavnih_atrakcijah = id_mesta_po_atrakciji)

@bottle.get('/izpisi_podatke_glavne_atrakcije_vmesna/<id>')
def podatki_mesta_po_atrakcijah(id):
    '''Izpiše podatke ustrezna mesta glede na letni čas potovanja'''
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom=komentarji)    

#MESTA GLEDE NA ZELJE
@bottle.get('/izbira_glede_na_zelje')
def zelje():
    '''Iskanje glede na zelje potovanja.'''
    return bottle.template('views/zelje.html')

@bottle.post('/izbira_glede_na_zelje')
def iskanje_zeljenih_mest_post():
    '''Prebere ibiro zelja potovanja in potem poišče vsa mesta'''
    stevilo_dni = bottle.request.forms.getunicode('st_dni')
    letni_cas = bottle.request.forms.getunicode('letni_cas')
    cena = bottle.request.forms.getunicode('cenovni_rang')
    id_mesta_po_zeljah = model.mesta_glede_na_zelje(stevilo_dni, letni_cas,cena)
    mes_po_zeljah = []
    for i in id_mesta_po_zeljah:
        podatki_po_zeljah = model.podatki_mesta(i)
        mes_po_zeljah.append(podatki_po_zeljah[0])
    return bottle.template('views/izpisi_mesta_po_zeljah.html', mesta_po_zeljah = mes_po_zeljah, idji_po_zeljah = id_mesta_po_zeljah)

@bottle.get('/izpisi_podatke_po_zeljah_vmesna/<id>')
def podatki_mesta_vse(id):
    podatki = model.podatki_mesta(id)
    komentarji = model.dobi_vse_komentarje(id)
    return bottle.template('views/izpisi_podatke_mesta.html', pod = podatki, kom= komentarji) 




bottle.run(debug=True, reloader=True)