from mock import Mock, patch
from unittest import TestCase

from models import *
from bowling.game import *
from management.commands import bowl as bowl_command
from management.commands import bowling_scores as scores_command

class GameTests(TestCase):

    def test_format_results(self):
        sut = Mock(spec=BowlingLane())
        self.assertEqual("name: [1][2][3]",
                         BowlingLane.format_results(sut, "name", [1, 2, 3]))

    @patch('bowling.game.BowlingGame.scores_for_game')
    def test_get_player_and_scores_in_formatted_scores_property(self, scores_for_game):
        scores_for_game.return_value = [1, 1, 1]
        sut = BowlingLane()
        sut._bowlers = [['name1', BowlingGame()],
                        ['name2', BowlingGame()]]
        self.assertEqual(
            ['name1: [1][1][1]', 'name2: [1][1][1]',],
            sut.formatted_scores
        )



class BowlingTests(TestCase):

    def test_store_bowling_scores(self):
        scores = Scores(score='test')
        self.assertEqual('test', scores.score)

    @patch('bowling.game.BowlingGame.score_for_frame')
    def test_return_list_of_scores_for_all_frames_in_scores_for_game(self, score_for_frame):
        score_for_frame.return_value = 1
        game = BowlingGame()
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
                         game.scores_for_game())


class BowlCommandTests(TestCase):

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_handle_creates_bowling_lane(self, bowlinglane):
        bowlinglane.return_value.formatted_scores = ['game1',]
        command = bowl_command.Command()
        command.handle()
        bowlinglane.assert_called_once_with()

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_prompts_for_bowlers(self, bowlinglane):
        bowlinglane.return_value.formatted_scores = ['game1',]
        command = bowl_command.Command()
        command.handle()
        bowlinglane.return_value.prompt_for_bowlers.assert_called_once_with()

    @patch('bowling.game.BowlingLane')
    def test_bowl_command_plays_game(self, bowlinglane):
        bowlinglane.return_value.formatted_scores = ['game1',]
        command = bowl_command.Command()
        command.handle()
        bowlinglane.return_value.play_game.assert_called_once_with()

    @patch('bowling.game.BowlingLane')
    @patch('bowling.models.Scores.objects')
    def test_save_scores_for_each_game(self, scores_objects, bowlinglane):
        bowlinglane.return_value.formatted_scores = ['game1',]
        command = bowl_command.Command()
        command.handle()
        scores_objects.create.assert_called_once_with(score='game1')


class BowlingScoresCommandTests(TestCase):

    @patch('bowling.models.Scores.objects')
    def test_dump_all_scores_in_handle(self, scores_objects):
        scores_objects.all.return_value = []
        command = scores_command.Command()
        command.handle()
        scores_objects.all.assert_called_once_with()
        
