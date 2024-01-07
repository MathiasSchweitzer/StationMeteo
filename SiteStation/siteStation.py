import uvicorn
from fastapi import FastAPI, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import datetime
import json
import os
import sqlite3
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import init_db
import Raspberry.init as capteurs
import signal

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOIS = [
    ["Nom", "Jours"],
    ["Janvier", 31],
    ["Février", 28],
    ["Mars", 31],
    ["Avril", 30],
    ["Mai", 31],
    ["Juin", 30],
    ["Juillet", 31],
    ["Août", 31],
    ["Septembre", 30],
    ["Octobre", 31],
    ["Novembre", 30],
    ["Décembre", 31]
]
TYPES = {
    "humidite": ["Humidité", "%"],
    "lumiere": ["Lumière", "%"],
    "pression": ["Pression", "hPa"],
    "temp1": ["Température (DHT 22)", "°C"],
    "temp2": ["Température (DPS310)", "°C"]
}

@asynccontextmanager
async def lancement(app: FastAPI):
    print("Début")
    init_db.init()
    asyncio.create_task(capteurs.run())
    yield
    print("Terminé")

app = FastAPI(lifespan=lancement)

path = os.path.dirname(__file__)

templates = Jinja2Templates(directory = path + "/templates/")
app.mount("/static", StaticFiles(directory = path + "/static"), name="static")
app.mount("/assets", StaticFiles(directory = path + "/assets"), name="assets")

@app.get("/", response_class=HTMLResponse, name="Accueil") # Traitement de la requête get http
def hello(request: Request): # Valeur de retour pour la réponse http
    """
        Redirection vers aujourd'hui si on essaie d'accéder à la racine du site web (défaut).
    """
    date = datetime.date.today()
    url = "/" + str(date.year) + "/" + str(date.month) + "/" + str(date.day)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/{an}", response_class=HTMLResponse)
def annee(request: Request, an: int):
    """
        Page pour présenter les mois de l'année renseignée.
        an : Année de la barre d'adresse
    """
    db = sqlite3.connect("data.db")
    dateReq = str(an)
    data = db.execute('SELECT DISTINCT(dateDonnee) FROM data WHERE dateDonnee LIKE "' + dateReq + '%"').fetchall()
    db.close()
    donnees = [e[0][0:6] for e in data]
    donneesPresentes = [True if (str(an) + str(i + 1).zfill(2)) in donnees else False for i in range(12)]
    return templates.TemplateResponse("annee.html", {"request": request, "annee": an, "MOIS": MOIS, "donnees": donneesPresentes})

@app.get("/{an}/{mo}", response_class=HTMLResponse)
def mois(request: Request, an: int, mo: int):
    """
        Page pour présenter les jours du mois donné, et qui renvoie une page différente si la date est invalide.
        an : Année de la barre d'adresse
        mo : Mois de la barre d'adresse
    """
    if (not(1 <= mo <= 12)):
        return templates.TemplateResponse("mauvaiseDate.html", {"request": request, "mois": mo, "annee": an, "title": "Mauvaise date"})
    nbJour = MOIS[mo][1]
    if ((mo == 2) and ((an % 4 == 0) and ((an % 100 != 0) or (an % 400 == 0)))):
        nbJour += 1
    anPrec = an
    moisPrec = mo - 1
    if moisPrec <= 0:
        anPrec -= 1
        moisPrec += 12
    jourPrec = MOIS[moisPrec][1]
    if ((moisPrec == 2) and ((anPrec % 4 == 0) and ((anPrec % 100 != 0) or (anPrec % 400 == 0)))):
        jourPrec += 1
    skip = datetime.date(an, mo, 1).isoweekday() - 1
    db = sqlite3.connect("data.db")
    dateReq = str(an) + str(mo).zfill(2)
    data = db.execute('SELECT DISTINCT(dateDonnee) FROM data WHERE dateDonnee LIKE "' + dateReq + '%"').fetchall()
    db.close()
    donnees = [e[0] for e in data]
    donneesPresentes = [True if (str(an) + str(mo).zfill(2) + str(i + 1).zfill(2)) in donnees else False for i in range(nbJour)]
    return templates.TemplateResponse("mois.html", {"request": request, "mois": mo, "annee": an, "skip": skip, "MOIS": MOIS, "JOURS": JOURS, "donnees": donneesPresentes, "nbJour": nbJour, "jourPrec": jourPrec, "moisZfill": str(mo).zfill(2)})



@app.get("/{an}/{mo}/{jo}", response_class=HTMLResponse)
def jour(request: Request, an: int, mo: int, jo: int):
    """
        Page pour présenter les données du jour indiqué, et qui renvoie une page différente si la date est invalide.
        an : Année de la barre d'adresse
        mo : Mois de la barre d'adresse
        jo : Jour de la barre d'adresse
    """
    if (not(1 <= mo <= 12) or not(1 <= jo <= MOIS[mo][1])) and not((jo == 29) and (mo == 2) and ((an % 4 == 0) and ((an % 100 != 0) or (an % 400 == 0)))):
        return templates.TemplateResponse("mauvaiseDate.html", {"request": request, "jour": jo, "mois": mo, "annee": an, "title": "Mauvaise date"})
    date = datetime.date(an, mo, jo).isoweekday() - 1
    db = sqlite3.connect("data.db")
    dateReq = str(an) + str(mo).zfill(2) + str(jo).zfill(2)
    distincts = db.execute('SELECT DISTINCT(typeDonnee) FROM data WHERE dateDonnee == "' + dateReq + '"').fetchall()
    data = db.execute('SELECT * FROM data WHERE dateDonnee == "' + dateReq + '"').fetchall()
    db.close()
    return templates.TemplateResponse("jour.html", {"request": request, "jour": jo, "mois": mo, "annee": an, "date": date, "MOIS": MOIS, "JOURS": JOURS, "data": json.dumps(data), "TYPES": TYPES, "distincts": distincts, "distinctsJSON": json.dumps(distincts)})

@app.get("/stop", response_class=HTMLResponse)
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Extinction du serveur...')

def run():
    uvicorn.run(app)


if __name__ == "__main__":
    run()