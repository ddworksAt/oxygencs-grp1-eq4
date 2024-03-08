# Ajout de linting, analyse et statique de code et de formatage
Pour ajouter la librairie permettant d'analyser le code, on a execute cette `pipenv install pylint`. À l'aide de cette commande, on a pu recupérer l'état du code par rapport à nos critères qui sont par exemple : le nombre de method ou class documentées, le nombre de module documenté, la quantité d'espace non nécessaire, le formatage des noms des variables, etc...

# Configuration et mise en marche de pylint
La configuration de pylint se fait dans le fichier `.pylintrc` et pour executer cette librairie et obtenir un rapport détails de l'état de notre code. Vous devez entrez cette commande : `pipenv run pylint --rcfile=.pylintrc src/*`

# Ajout du formatage
Le formatage s'effectue à l'aide de notre librairie `black`, on a execute cette `pipenv install black` pour pouvoir l'installer.

# Configuration et mise en marche de black
Les paramêtres de configuration de black se retrouve dans notre fichier `pyproject.toml`. Pour utiliser cette librairie, vous avez juste à executer cette commande `pipenv run black .`

# Ajout du pre-commit
Le pre-commit s'effectue à l'aide de notre librairie `pre-commit`, on a execute cette `pipenv install pre-commit` pour pouvoir l'installer.

# Configuration et mise en marche de pre-commit
Les paramêtres de configuration de pre-commit se retrouve dans notre fichier `.pre-commit-config.yaml`. Pour utiliser cette librairie, vous avez juste à executer ces commandes `pipenv run pre-commit install` et `pipenv run pre-commit run --all-files`
