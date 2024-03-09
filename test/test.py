import unittest
from unittest.mock import MagicMock
from src.main import App
import psycopg2
import os
from dotenv import load_dotenv


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

        load_dotenv()
        self.app.HOST = os.getenv("HOST")
        self.app.TOKEN = os.getenv("TOKEN")
        self.app.T_MIN = os.getenv("T_MIN")
        self.app.T_MAX = os.getenv("T_MAX")

        self.app.connection_pool = MagicMock()
        self.app.connection_pool.getconn = MagicMock(return_value=MagicMock())
        self.app.connection_pool.putconn = MagicMock()

    # Test connection to the database
    def test_db_connection(self):
        try:
            conn = psycopg2.connect(self.app.DATABASE_URL)
            self.assertIsNotNone(conn)
            conn.close()
        except:
            self.fail("Database connection failed")

    # Test that on_sensor_data_received calls the appropriate functions
    def test_on_sensor_data_received(self):
        self.app.take_action = MagicMock()
        self.app.save_event_to_database = MagicMock()

        self.app.on_sensor_data_received([{"date": "2020-01-01", "data": "25.0"}])
        self.app.take_action.assert_called_once
        self.app.save_event_to_database.assert_called_once

    # Test that take_action returns the string value or None
    def test_take_action(self):
        self.assertEqual(
            self.app.take_action(float(self.app.T_MIN) - 1),
            "Activating Heater for 10 ticks",
        )
        self.assertEqual(
            self.app.take_action(float(self.app.T_MIN)),
            "Activating Heater for 10 ticks",
        )
        self.assertEqual(self.app.take_action(float(self.app.T_MIN) + 0.1), None)
        self.assertEqual(self.app.take_action(float(self.app.T_MIN) + 1), None)
        self.assertEqual(self.app.take_action(float(self.app.T_MAX) - 0.1), None)
        self.assertEqual(self.app.take_action(float(self.app.T_MAX)), "Activating AC for 10 ticks")
        self.assertEqual(
            self.app.take_action(float(self.app.T_MAX) + 1),
            "Activating AC for 10 ticks",
        )

    # Test scenarios for saving hvac temperatures or events to the database
    def test_save_hvac_to_database(self):
        self.app.get_connection = MagicMock(return_value=MagicMock())
        self.app.put_connection = MagicMock()

        self.app.save_event_to_database("2024-01-01", 18.0, "Activating Heater for 10 ticks")
        self.app.get_connection.assert_called_once()
        self.app.put_connection.assert_called_once()
        self.app.get_connection.return_value.cursor.assert_called()
        self.app.get_connection.return_value.commit.assert_called_once()
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO events (event, "createdAt") VALUES (%s, %s)',
            ("Activating Heater for 10 ticks", "2024-01-01"),
        )

        self.app.save_event_to_database(
            "2024-01-01", float(self.app.T_MIN), "Activating Heater for 10 ticks"
        )
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO events (event, "createdAt") VALUES (%s, %s)',
            ("Activating Heater for 10 ticks", "2024-01-01"),
        )

        self.app.save_event_to_database("2024-01-01", float(self.app.T_MIN) + 0.1, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)',
            (19.1, "2024-01-01"),
        )

        self.app.save_event_to_database("2024-01-01", float(self.app.T_MIN) + 1, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)',
            (20.0, "2024-01-01"),
        )

        self.app.save_event_to_database("2024-01-01", float(self.app.T_MAX) - 0.1, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)',
            (23.9, "2024-01-01"),
        )

        self.app.save_event_to_database(
            "2024-01-01", float(self.app.T_MAX), "Activating AC for 10 ticks"
        )
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO events (event, "createdAt") VALUES (%s, %s)',
            ("Activating AC for 10 ticks", "2024-01-01"),
        )

        self.app.save_event_to_database(
            "2024-01-01", float(self.app.T_MAX) + 1, "Activating AC for 10 ticks"
        )
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with(
            'INSERT INTO events (event, "createdAt") VALUES (%s, %s)',
            ("Activating AC for 10 ticks", "2024-01-01"),
        )
