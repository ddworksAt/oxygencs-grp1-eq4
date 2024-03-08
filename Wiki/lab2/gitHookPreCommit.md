# Ajout de linting, analyse et statique de code et de formatage
Pour ajouter la librairie permettant d'analyser le code, on a execute cette `pipenv install pylint`. À l'aide de cette commande, on a pu recupérer l'état du code par rapport à nos critères qui sont par exemple : le nombre de method ou class documentées, le nombre de module documenté, la quantité d'espace non nécessaire, le formatage des noms des variables, etc...

# Configuration et mise en marche de pylint
La configuration de pylint se fait dans le fichier `pylintrc` et pour executer cette librairie et obtenir un rapport détails de l'état de notre code. Vous devez entrez cette commande : `pipenv run pylint --rcfile=.pylintrc src/*`