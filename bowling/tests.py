from mock import Mock, patch
from unittest import TestCase

from models import *
from bowling.game import *
from management.commands import bowl as bowl_command

class BowlingTests(TestCase):

    def test_store_bowling_scores(self):
        scores = Scores(score='test')
        self.assertEqual('test', scores.score)

class BowlCommandTests(TestCase):

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_handle_creates_bowling_lane(self, bowlinglane):
        command = bowl_command.Command()
        command.handle()
        bowlinglane.assert_called_once_with()

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_prompts_for_bowlers(self, bowlinglane):
        command = bowl_command.Command()
        command.handle()
        bowlinglane.return_value.prompt_for_bowlers.assert_called_once_with()

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_plays_game(self, bowlinglane):
        command = bowl_command.Command()
        command.handle()
        bowlinglane.return_value.play_game.assert_called_once_with()