import bottle
import model

glavni_model = model.Model()

@bottle.get("/") #ko na strani pridem do / nse požene ta funkcija
def glavna_stran():
    podatki = glavni_model.dobi_vse_drzave()

    return bottle.template("glavna.html", uporabniki = podatki)



bottle.run(debug=True, reloader=True)