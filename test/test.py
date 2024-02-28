import unittest
from unittest.mock import MagicMock
from src.main import App
import os
from dotenv import load_dotenv

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        load_dotenv()

        self.app.HOST = os.getenv('HOST')
        self.app.TOKEN = os.getenv('TOKEN')
        self.app.T_MAX = os.getenv('T_MAX')
        self.app.T_MIN = os.getenv('T_MIN')
        self.app.DATABASE_URL = os.getenv('DATABASE_URL')
        self.app.MIN_CONN = os.getenv('MIN_CONN')
        self.app.MAX_CONN = os.getenv('MAX_CONN')
        self.app.connection_pool = MagicMock()
        self.app.connection_pool.getconn = MagicMock(return_value=MagicMock())
        self.app.connection_pool.putconn = MagicMock()

# make more interesting tests for on_sensor_data_received...
    # def test_on_sensor_data_received(self):
    #     self.app.take_action = MagicMock()
    #     def side_effect(temperature):
    #         if float(temperature) >= float(self.app.T_MAX):
    #             return "Activating Heater for 10 ticks"
    #         elif float(temperature) <= float(self.app.T_MIN):
    #             return "Activating AC for 10 ticks"
    #         else:
    #             return None
    #     self.app.take_action.side_effect = side_effect
        
    #     self.app.save_event_to_database = MagicMock()
    #     self.app.on_sensor_data_received([{"date": "2020-01-01", "data": "25.0"}])
    #     self.app.take_action.assert_called_once_with(25.0)
    #     self.app.save_event_to_database.assert_called_once_with("2020-01-01", 25.0, self.app.take_action.return_value)

    def test_take_action(self):
        self.assertEqual(self.app.take_action(18), "Activating Heater for 10 ticks")
        self.assertEqual(self.app.take_action(22), None)
        self.assertEqual(self.app.take_action(24), "Activating AC for 10 ticks")

    def test_save_event_to_database(self):
        self.app.get_connection = MagicMock(return_value=MagicMock())
        self.app.put_connection = MagicMock()
        self.app.save_event_to_database("2024-01-01", 25.0, "Activating AC for 10 ticks")
        self.app.get_connection.assert_called_once()
        self.app.put_connection.assert_called_once()
        self.app.get_connection.return_value.cursor.assert_called()
        # since 25.0 exceeds T_MAX = 24, the last cursor call is with the events insert. add asserts for various temperature values
        # self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO temperatures (temperature, "createdAt") VALUES (%s, %s)', (25.0, "2024-01-01"))
        self.app.get_connection.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO events (event, "createdAt") VALUES (%s, %s)', ("Activating AC for 10 ticks", "2024-01-01"))
        self.app.get_connection.return_value.commit.assert_called_once()