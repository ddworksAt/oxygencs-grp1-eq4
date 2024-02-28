import unittest
from unittest.mock import MagicMock
from src.main import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.connection_pool = MagicMock()
        self.app.connection_pool.getconn = MagicMock(return_value=MagicMock())
        self.app.connection_pool.putconn = MagicMock()

    def test_on_sensor_data_received(self):
        self.app.take_action = MagicMock()
        self.app.save_event_to_database = MagicMock()
        
        self.app.on_sensor_data_received([{"date": "2020-01-01", "data": "25.0"}])
        self.app.take_action.assert_called_once
        self.app.save_event_to_database.assert_called_once

    def test_take_action(self):
        self.assertEqual(self.app.take_action(18.0), "Activating Heater for 10 ticks")
        self.assertEqual(self.app.take_action(19.0), "Activating Heater for 10 ticks")
        self.assertEqual(self.app.take_action(19.1), None)
        self.assertEqual(self.app.take_action(22.0), None)
        self.assertEqual(self.app.take_action(23.9), None)
        self.assertEqual(self.app.take_action(24.0), "Activating AC for 10 ticks")
        self.assertEqual(self.app.take_action(25.0), "Activating AC for 10 ticks")

    def test_save_event_to_database(self):
        self.app.get_connection = MagicMock(return_value=MagicMock())
        self.app.put_connection = MagicMock()

        self.app.save_event_to_database("2024-01-01", 18.0, "Activating Heater for 10 ticks")
        self.app.get_connection.assert_called_once()
        self.app.put_connection.assert_called_once()
        self.app.get_connection.return_value.cursor.assert_called()
        self.app.get_connection.return_value.commit.assert_called_once()
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO events (event, "createdAt") VALUES (%s, %s)', ("Activating Heater for 10 ticks", "2024-01-01"))
        
        self.app.save_event_to_database("2024-01-01", 19.0, "Activating Heater for 10 ticks")
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO events (event, "createdAt") VALUES (%s, %s)', ("Activating Heater for 10 ticks", "2024-01-01"))

        self.app.save_event_to_database("2024-01-01", 19.1, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)', (19.1, "2024-01-01"))

        self.app.save_event_to_database("2024-01-01", 22.0, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)', (22.0, "2024-01-01"))
        
        self.app.save_event_to_database("2024-01-01", 23.9, None)
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)', (23.9, "2024-01-01"))

        self.app.save_event_to_database("2024-01-01", 24.0, "Activating AC for 10 ticks")
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO events (event, "createdAt") VALUES (%s, %s)', ("Activating AC for 10 ticks", "2024-01-01"))

        self.app.save_event_to_database("2024-01-01", 25.0, "Activating AC for 10 ticks")
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO events (event, "createdAt") VALUES (%s, %s)', ("Activating AC for 10 ticks", "2024-01-01"))