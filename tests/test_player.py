import unittest
from src.player import Player

class TestPlayer(unittest.TestCase):
    def test_player(self):
        socket_mock = "socket_mock_object"
        player_default_score = Player('1.1.1.1', socket_mock, 'pancrazio')
        self.assertTrue(player_default_score.get_ip() == '1.1.1.1')
        self.assertTrue(player_default_score.get_socket() == socket_mock)
        self.assertTrue(player_default_score.get_name() == 'pancrazio')
        self.assertTrue(player_default_score.get_score() == 0)

        player_default_score.add_point()
        self.assertTrue(player_default_score.get_score() == 1)
        player_default_score.remove_point()
        player_default_score.remove_point()
        self.assertTrue(player_default_score.get_score() == -1)

        player_set_score = Player('2.2.2.2', socket_mock, 'alice', 1000)
        self.assertTrue(player_set_score.get_ip() == '2.2.2.2')
        self.assertTrue(player_set_score.get_socket() == socket_mock)
        self.assertTrue(player_set_score.get_name() == 'alice')
        self.assertTrue(player_set_score.get_score() == 1000)

        player_set_score.add_point()
        player_set_score.add_point()
        player_set_score.add_point()
        self.assertTrue(player_set_score.get_score() == 1003)
        player_set_score.remove_point()
        self.assertTrue(player_set_score.get_score() == 1002)


if __name__ == '__main__':
    unittest.main()

