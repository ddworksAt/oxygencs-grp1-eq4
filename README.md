# LOG-680 : OxygenCS-GTP1-EQ4
Cette application Python surveille en permanence un hub de capteurs et gère les actions du système CVC (chauffage, ventilation et climatisation) en fonction des données de capteur reçues.

Il exploite « signalrcore » pour maintenir une connexion en temps réel au hub de capteurs et utilise des « requêtes » pour envoyer des requêtes GET à un point final de contrôle CVC distant. Les données recueillies sont enregistrées dans une base de données PostgreSQL dont l'URL de connexion doit être spécifié.

Cette application utilise `pipenv`, un outil qui vise à apporter le meilleur de tous les mondes du packaging au monde Python.

## Requis
- Python 3.8+
- pipenv

## Rouler l'application
Créer un fichier .env et configurer les variables suivantes:
```
HOST = http://{hôte de votre simulateur HVAC}
TOKEN = {token de votre simulateur HVAC}
T_MIN = {valeur de votre choix}
T_MAX = {valeur de votre choix}
DATABASE_URL = postgresql://{username}:{password}@{hôte de la BD}:{port}/{nom de la BD}
MIN_CONN = {nombre minimum de connexions}
MAX_CONN = {nombre maximum de connexions}
```

Activer l'environnement virtuel:
```bash
pipenv shell
```

Installer les dépendances essentielles au fonctionnement de l'application et mettre à jour Pipfile.lock:
```bash
pipenv install
```

Après les configurations, vous pouvez rouler l'application (si celui-ci échoue avec une erreur SignalRCoreClient, entrez ctrl+c puis la commande de nouveau):
```bash
pipenv run start
```

Installer les dépendances essentielles au fonctionnement de l'application ET pour le développement (tests, analyse de code, formattage et *pre-commit*):
```bash
pipenv install --dev
```

Rouler les tests (nécessite les dépendances de développement en plus des dépendances essentielles à l'application):
```bash
pipenv run test
```

## Licence
MIT

## Documentation
[Connexion à PostgreSQL et données](Wiki/lab2/PostgreSQL.md)

[Intégration continue](Wiki/lab2/IntegrationContinue.md)

[Kubernetes](Wiki/lab3/Kubernetes.md)