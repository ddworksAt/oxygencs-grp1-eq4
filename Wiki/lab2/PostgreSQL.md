# Connexion à PostgreSQL et données
La connexion à la base de données se fait directement dans le fichier `src/main.py`. En utilisant le paquet `psycopg2`, la connexion à la base de données est établie grâce à une URL de connexion. L'application utilise également un pool de connexions, spécifiant un nombre minimal et maximal de connexions simultanées à maintenir, puisque les insertions dans la base de données sont fréquentes. Ces valeurs sont obtenues à partir du fichier `.env` grâce au paquet `dotenv`.

## Insertion dans la base de données
Pour effectuer une insertion dans la base de données, une connexion est obtenue du pool de connexions grâce à la fonction `get_connection()`. Un *cursor* est créé avec `cursor()`, puis `cursor.execute('')` est appelé pour effectuer l'insertion. `cursor.commit()` est utilisé pour confirmer l'insertion, puis la connection est remis au pool avec `cursor.close()`.

## Temperatures
La table *temperature* possède les colonnes *temperature* et *createdAt*. Chaque rangée dans cette table représente la température détectée à un temps précis par le simulateur HVAC suite à la réception de données de celui-ci par l'application, grâce à la fonction `on_sensor_data_received()` qui est appelé à chaque évènement `ReceiveSensorData` provenant de la connexion établie par `signalrcore`.

## Events
La table *temperature* possède les colonnes *event* et *createdAt*. Chaque rangée dans cette table représente une action que l'application a envoyée à un temps précis lorsque la température détectée est inférieure à la température minimale ou supérieure à la température maximale, soit les deux valeurs configurées dans le fichier `.env`.
