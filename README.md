[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) 
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# Projet GUDLFT

<p align="center">
  <img src="./static/img/icon.jpg" alt="Icone GUDLFT">
</p>

 L'objectif de l'application est de rationaliser la gestion des compétitions entre les clubs (hébergement, inscriptions, frais et administration). L'application permettra aux clubs d'inscrire des athlètes aux compétitions organisées au sein
de la division. Seules les admins et les secrétaires de club auront accès à l'application.



Actuellement, les clubs gagnent des points via la mise en place et le déroulement des
compétitions. Chaque club peut voir son solde actuel et échanger des points pour inscrire
des athlètes à de futures compétitions, à raison d'un point par inscription. Chaque
compétition aura un nombre limité d'inscriptions, et chaque club ne peut inscrire qu'un
maximum de 12 athlètes.


 ## Réalisations
 - <a href="https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues"> Phase 1 du projet : régler les bogues du POC. </a>
 - <a href="https://github.com/NidalChateur/OC_P11_GUDLFT/blob/main/mission/Spe%CC%81cifications_fonctionnelles.pdf">Phase 2 du projet : améliorer les fonctionnalités de l'application par des tests.</a> 
 - <a href="https://github.com/NidalChateur/OC_P11_GUDLFT/blob/main/mission/schema_base_de_donnee_P11.xlsx">Schéma de base de donnée GUDLFT.</a> 

## Cas d'usages

 #### Cas d'usages d'un utilisateur "visiteur" (non connecté)
  1. Par souci de transparence, les visiteurs peuvent consulter le nombre de points disponibles pour chaque club. 

  2. Les visiteurs peuvent s'inscrire sur la plateforme GUDLFT en créant un compte "secrétaire".

 #### Cas d'usages d'un utilisateur "secrétaire"
  1. Les secrétaires de club pourront utiliser leur adresse électronique pour se connecter.

  2. Les secrétaires pourront réinitialiser leur mot de passe sur la rubrique "mot passe oublié".

  3. Les secrétaires pourront créer leur club qui sera associé à leur compte utilisateur secrétaire. 
  Contrainte : un compte secrétaire ne peut gérer plusieurs clubs à la fois.

  4. Les secrétaires peuvent consulter la liste des compétitions à venir, en ayant un aperçu des places restantes et de la date de chaque compétition. Contraintes : les secrétaires ne pourront pas avoir accès aux compétitions "complètes" ou dont la date est déjà passée. 

  5. Les secrétaires pourront ensuite sélectionner une compétition et utiliser les points de leur club pour réserver des places dans cette compétition. Les points utilisés seront déduits du total précédent. Contraintes : chaque secrétaire ne peut effectuer qu'une seule réservation dans chaque compétition, et les secrétaires ne pourront pas réserver plus de 12 places dans une compétition dans la limite des points que possède leur club (afin de garantir l'équité envers les autres clubs).

  6. Les secrétaires auront la possibilité de consulter leurs réservations et les annuler pour récupérer leurs points. Contrainte : les secrétaires ne peuvent pas annuler une réservation sur une compétition dont la date est déjà passée.

  6. Les secrétaires des clubs pourront se déconnecter.

 #### Cas d'usages d'un utilisateur "admin"
 * CRUD : Create, Read, Update, Delete.

 1. Les admins pourront utiliser leur adresse électronique pour se connecter.

 2. Les admins pourront réaliser du CRUD sur la liste des utilisateurs inscrits sur l'application.

 3. Les admins pourront réaliser du CRUD sur la liste des clubs inscrits sur l'application.

 5. Les admins pourront réaliser du CRUD sur la liste des compétitions inscrites sur l'application.

 6. Les admins pourront réaliser du CRUD sur la liste des réservations inscrites sur l'application.    

## Pré-requis

* Installer Python 3 : [Téléchargement Python 3](https://www.python.org/downloads/)
* Installer git : [Téléchargement Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

## Installation

### 1. Télécharger le projet sur votre répertoire local : 
```
git clone https://github.com/NidalChateur/OC_P11_GUDLFT.git 
cd OC_P11_GUDLFT
```
### 2. Mettre en place un environnement virtuel :
* Créer l'environnement virtuel: `python -m venv env`

### 3. Activer l'environnement virtuel
* Activer l'environnement virtuel :
    * Windows : `env\Scripts\activate.bat`
    * Unix/MacOS : `source env/bin/activate`
   
### 4. Installer les dépendances du projet sans poetry
```
pip install -r requirements.txt
```

### 4. Ou Installer les dépendances du projet avec poetry
```
pip install poetry

poetry install
```

### 5. Démarrage sans poetry
* Lancer le script à l'aide de la commande suivante : `flask run`

### 5. Démarrage avec poetry
* Lancer le script à l'aide de la commande suivante : `poetry run flask run`

Lorsque le serveur fonctionne, l'application peut être consultée à partir de l'url [http://127.0.0.1:5000].

Les étapes 1, 2 et 4 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs du serveur de l'application, il suffit d'exécuter les étapes 3 et 5 à partir du répertoire racine du projet.

## Générer un rapport d'erreur grâce à flake8

Flake8 est souvent utilisé pour vérifier le respect des conventions de style PEP 8 dans le code Python. Pour réaliser ceci, se positionner à la racine du projet puis exécuter dans le terminal : 

`flake8`

Un rapport d'erreur au format html, sera alors disponible dans le dossier "flake8_report".

## Générer un rapport complet et détaillé de couverture de test 

La couverture de test vérifie le taux de lignes couvertes par des tests. 

Pour réaliser ceci, se positionner à la racine du projet puis exécuter dans le terminal : 

`pytest --cov=. --cov-report html`

Quand le script est terminé, vous découvrez qu'un nouveau dossier "htmlcov" a été créé à l'endroit où vous avez lancé la commande. Ce dossier contient différents documents dont des fichiers HTML.

Ouvrez le fichier "index.html" qui contient un résumé du rapport de couverture.

À partir de cette page, vous pourrez naviguer à travers les différents fichiers afin d’avoir le détail sur la couverture. Effectivement, vous aurez un rapport détaillé pour chaque fichier source sous le format HTML.

