## To implement
FROM python:3.8.0

WORKDIR /app

# Copiez les fichiers nécessaires
COPY src/ /app/src/
COPY test/ /app/test/
COPY Pipfile Pipfile.lock /app/


# Installez les dépendances
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Définissez les variables d'environnement
ENV HOST="http://159.203.50.162"
ENV TOKEN="f016a1c457cf9096b514"
ENV T_MAX="24"
ENV T_MIN="19"
ENV DATABASE_URL="postgresql://user01eq4:lyimRoKqSg7hHgc1@157.230.69.113:5432/db01eq4"
ENV MIN_CONN="1"
ENV MAX_CONN="10"

# Commande pour exécuter le script
CMD ["pipenv", "run", "start"]