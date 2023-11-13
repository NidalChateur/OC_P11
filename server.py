import json

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

# 1 # : commentaire
### 3 ### : bogue où incohérence

# Liste des bogues généraux à fixer

### 0. Mettre à jour les dependences du projet pour améliorer la sécurité ###
### 1. Mettre en place une BDD SQLITE, pour la persistance des données ####
### 2. Utiliser if __name__ == "main": app.run() pour lancer l'appli ! ###
### 3. Créer un fichier config.py ###
### 4. Utiliser {% extends "base.html" %} {% include %} {% block content %} pour faire du DRY sur le html###
###    Respecter la syntaxe html et sa structure body head nav main section footer ###
### 5. Structurer le projet en créant une app authentication, une app competition ###
### 6. Urls.py, views.py, models.py... ###
### 7. Ajouter login_required pour les vue de réservation
### 8. Gérer les exception pour ne pas que l'app plante ###
### 9. Ajouter des tests unitaire et fonctionnel ###
### 10. Bootstrap ###


# charge le json club
def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


# charge le json compétition
def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


### charger les variables d'environnement pour permettre la CLI 'flask run' ###
load_dotenv()

# création de l'app
app = Flask(__name__)

### secret key à mettre dans un fichier config ###
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


### plante si l'email n'est pas correcte ! à corriger ####
### pas de mot de passe pour s'authentifier ####
### utilisateur déconnecté une fois au retour à l'accueil ###
### vérifier l'authentification et gérer les exceptions ###
# vue accueil (entrer le mail...)
# renvoi vers la vue showSummary qui permet de réserver des places
@app.route("/")
def index():
    return render_template("index.html")


# méthode POST only
### n'affiche pas le nom du club ####
### affiche des compétition du passé !! ###
### Il ne doit pas être possible de réserver des places dans une compétition passé ###
# vue showSummary qui lit competitions.json
# Lis les info du club dans clubs.json where club["email"] == request.form["email"]
# Lis competition.json
# renvoi vers la vue book qui permet d'entrer le nombre de place à réserver
@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


# vue permettant de réserver des place dans une compétition
# book/competition.name/club.name
# renvoi vers la vue purchasePlaces qui affiche le tableau de bord après réservation
### maximum 12 place par club ###
### et maximum le nombre de point du club ###
@app.route("/book/<competition>/<club>")
def book(competition, club):
    # récupère le club dans clubs.json à partir de club.name passé en paramètre de l'url
    ### si la liste est vide, impossible d'accéder à l'indice 0 ! IndexError ###
    foundClub = [c for c in clubs if c["name"] == club][0]

    # récupère la compétition dans competitions.json à partir de competition.name passé en paramètre de l'url
    ### si la liste est vide, impossible d'accéder à l'indice 0 ! IndexError ###
    foundCompetition = [c for c in competitions if c["name"] == competition][0]

    # gestion de l'exception club et competition existante
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        ### ce else n'aboutit pas dans le cas où club n'exite pas ###
        ### ce else n'aboutit pas dans le cas où competition n'existe pas ###
        ### "welcome.html" ne s'affiche pas en de competition ou club inexistant ###
        #### mauvaise syntaxe balise <br> réglé sur "welcome.html" ###
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


# méthode POST only, GET impossible
# vue de "tableau de bord" affichant les point du club
# lis competitions.json
@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    ### pas de persistance des données !! ###
    ### possibilité de reserver plus de place que de disponibles....###
    ### possibilité de reserver un nombre négatif de places.... ###
    ### le nombre de point de club ne se met pas à jour ###

    # récupération de la compétition ciblé par une réservation
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    ### request.form["places"].isdigit() doit être contrôlé avant de convertir en int ! ###
    ### placesRequired doit être cleaned (sans signe), seule la valeur absolue doit être retenu ###

    placesRequired = int(request.form["places"])

    ### competition doit être vérifié avant d'effectuer des opérations ###
    ### si competition["numberOfPlaces"] < 0, afficher complet ! ###
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

    ### ce message flash est incohérent car affiche sans condition ###
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display
# ajouter une vue non connectée affichant les points des clubs


# vue déconnexion qui renvoi simplement à l'accueil
@app.route("/logout")
def logout():
    return redirect(url_for("index"))
