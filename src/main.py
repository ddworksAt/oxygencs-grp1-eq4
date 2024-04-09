from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv


class App:
    def __init__(self):
        self._hub_connection = None
        self.TICKS = 10

        # To be configured by your team
        load_dotenv()
        self.HOST = os.getenv("HOST")
        self.TOKEN = os.getenv("TOKEN")

        self.T_MIN = os.getenv("T_MIN")
        self.T_MAX = os.getenv("T_MAX")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.MIN_CONN = os.getenv("MIN_CONN")
        self.MAX_CONN = os.getenv("MAX_CONN")

        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=self.MIN_CONN, maxconn=self.MAX_CONN, dsn=self.DATABASE_URL
        )

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            action = self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature, action)
        except Exception as err:
            print(err)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            return self.send_action_to_hvac("TurnOnAc")
        if float(temperature) <= float(self.T_MIN):
            return self.send_action_to_hvac("TurnOnHeater")
        return None

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}")
        details = json.loads(r.text)
        # print(details, flush=True)
        return details["Response"]

    def save_event_to_database(self, timestamp, temperature, action):
        """Save sensor data into database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)',
                (temperature, timestamp),
            )
            print(" # Inserted {}, {} in the table temperatures...".format(temperature, timestamp))

            if action:
                cursor.execute(
                    'INSERT INTO events (event, "createdAt") VALUES (%s, %s)',
                    (action, timestamp),
                )
                print(" # Inserted {}, {} in the table events...".format(action, timestamp))

            print()

            conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print("Error saving into db: {}".format(e))
        finally:
            self.put_connection(conn)

    def get_connection(self):
        # Get a db connection from the pool
        # test
        return self.connection_pool.getconn()

    def put_connection(self, conn):
        # Put a db connection back into the pool
        self.connection_pool.putconn(conn)


if __name__ == "__main__":
    app = App()
    app.start()
