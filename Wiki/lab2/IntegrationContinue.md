# Intégration Continue

## Configuration du pre-commit git hook
Le *pre-commit git hook* permet d'automatiquement vérifier la qualité du code en effectuant une analyse de code et de formattage lorsqu'un développeur effectue un commit. Cela permet de garder une qualité régulière à travers les développeurs de l'équipe. Ceux-ci devront corriger tout *bad smell* provenant de l'analyse de code, puis le formattage automatique est effectué à travers les fichiers au besoin. Une fois le code de qualité adéquate, le *commit* passe, puis un *push* est effectué dans le répositoire du projet.

Pour installer les paquets nécessaires au pre-commit, il faut rouler la commande `pipenv install --dev` qui installe autant les dépendances nécessaires au fonctionnement de l'application que celles pour le développement. Entre autres, les paquets pylint, black et pre-commit sont utilisés pour implémenter l'analyse de code, le formattage et le pre-commit. Ces paquets sont les `[dev-packages]` se retrouvant dans le fichier `Pipfile`.

### Linting et analyse statique de code
Le paquet `pylint` effectue une analyse de code et permet d'identifier où des améliorations peuvent être apportés pour bien suivre les nomenclatures de développement. La configuration se retrouve dans le fichier `.pylintrc`. Pour exécuter manuellement, utilisez la commande `pipenv run pylint --rcfile=.pylintrc src/*`

### Formattage
Le paquet `black` sert au formattage des fichiers lorsque nécessaire et peut être exécuté manuellement avec la commande `pipenv run black.`

### Pre-commit
Pour le paquet `pre-commit` permet rouler des scripts lorsqu'un *commit* est effectué par un développeur. Tel que mentionné précédemment, nous utilisons `pre-commit` pour analyser le code et le formatter automatiquement pour assurer une bonne qualité de code avant de *push*. Si le script échoue, des corrections devront être effectuées avant de faire un nouveau *commit*. Pour rouler manuellement (sans effectuer de commit), utilisez la commande `pipenv run pre-commit run --all-files`.

## Construction et déploiement de l'image Docker
Cette partie de l'intégration continue est implémentée grâce à *Github Actions* dans le fichier `/.github/workflows/main.yml`. Ce fichier permet de dicter un *workflow* à rouler lorsqu'un évènement particulier est détecté. Dans ce cas-ci, le *workflow* roule lorsque l'évènement *push* est détecté dans n'importe quelle branche. Les *workflows* sont visibles dans l'onglet Actions du répositoire `oxygencs-grp1-eq4` et sont marqués par leur succès avec une coche verte et par leur échec par un x rouge. Sélectionner un *workflow* spécifique permet de voir les détails de chaque action, ce qui est particulièrement utile pour comprendre pourquoi il y a eu un échec à cause d'une action spécifique.

### Action test
La première action consiste à rouler les tests. Pour stopper le reste du *workflow* quand les tests échouent, la deuxième étape est marquée `needs test` pour rouler. Si les tests passent, alors la deuxième action roule, sinon, elle est ignorée. Les variables d'environnement, soit HOST, TOKEN, T_MIN, T_MAX, DATABASE_URL, MIN_CONN et MAX_CONN, sont obtenues grâces aux secrets d'action de Github.

Pour rouler les tests, les dépendances sont installées avec `pipenv install --dev`, puis `pipenv run test` est roulé.

### Action format
La deuxième action consiste à rouler l'analyse de code et le formattage. Tel que mentionné précédemment, cette action dépend de `test`, sinon elle est ignorée.

Pour rouler cette étape, les dépendances sont installées avec `pipenv install --dev`, puis `pipenv run pylint --rcfile=.pylintrc src/*` et `pipenv run black .` sont roulés pour vérifier les fichiers et les formatter au besoin. Dans le cas que pylint échoue, le développeur responsable devra effectuer les corrections nécessaires et effectuer un nouveau *push*.

### Action build-and-deploy
Cette dernière étape dépend de l'action `format`, donc si `test` échoue dès le début, celle-ci est ignorée puisque la deuxième l'est initialement. À cette étape, l'image Docker est construite et déployée sur le répositoire *Dockerhub* de notre choix. Les informations de connexion à *Dockerhub* sont stockés dans les secrets d'action de Github.

Deux images sont construites: une avec le tag *latest* et l'autre avec le numéro du build, afin de garder un historique d'images au cas où il y aurait un besoin d'utiliser une version antérieure de l'application. Pour construire ces images, la commande `docker build -t ddworksat/oxygencs-grp1-eq4:latest -t ddworksat/oxygencs-grp1-eq4:${GITHUB_RUN_NUMBER} .` est utilisée.

Spécifiquement à cette étape, nous construisons et déployons les images uniquement si l'évènement *push* se déroule dans la branche *main*. Si ce n'est pas le cas, cette étape est ignorée.

Pour déployer les deux images, des commandes séparées sont utilisées:
- `docker push ddworksat/oxygencs-grp1-eq4:latest`
- `docker push ddworksat/oxygencs-grp1-eq4:${GITHUB_RUN_NUMBER}`

Lorsque les trois actions sont roulés avec succès, le *workflow* entier passe avec le statut *Success*, sinon c'est le statut *Failure*.