
import mock
from django.utils import unittest
from django.test import TestCase

from bowling.game import BowlingGame, Frame, BowlingLane, ADD_BOWLER_PROMPT, THROW_BALL_PROMPT
class FrameTests(TestCase):

    def setUp(self):
        self.frame = Frame(1)

    def test_starts_with_roll_count_of_zero(self):
        self.assertEqual(0, self.frame.roll_count)

    def test_starts_rolls_as_empty_list(self):
        self.assertEqual([], self.frame.rolls)

    def test_defaults_is_tenth_to_false(self):
        self.assertEqual(False, self.frame.is_tenth)

    def test_sets_is_tenth_to_value_passed_in(self):
        frame = Frame(10)
        self.assertEqual(True, frame.is_tenth)

    def test_roll_count_is_number_of_rolls(self):
        self.frame.rolls = [1, 2]
        self.assertEqual(2, self.frame.roll_count)

    def test_add_roll_adds_pins_to_frame_rolls(self):
        self.frame.rolls = [9]
        self.frame.add_roll(1)
        self.assertEqual([9, 1], self.frame.rolls)

    def test_is_strike_returns_true_when_first_ball_equals_ten(self):
        self.frame.add_roll(10)
        self.assertEqual(True, self.frame.is_strike)

    def test_is_strike_returns_false_when_first_ball_not_ten(self):
        self.frame.add_roll(1)
        self.assertEqual(False, self.frame.is_strike)

    def test_is_strike_returns_false_when_no_rolls(self):
        self.assertEqual(False, self.frame.is_strike)

    def test_is_spare_returns_false_when_no_rolls(self):
        self.assertEqual(False, self.frame.is_spare)

    def test_is_spare_returns_false_when_only_one_roll(self):
        self.frame.add_roll(1)
        self.assertEqual(False, self.frame.is_spare)

    def test_is_spare_returns_false_when_two_rolls_less_than_ten(self):
        self.frame.add_roll(1)
        self.frame.add_roll(8)
        self.assertEqual(False, self.frame.is_spare)

    def test_is_spare_returns_true_when_two_rolls_equal_ten(self):
        self.frame.add_roll(2)
        self.frame.add_roll(8)
        self.assertEqual(True, self.frame.is_spare)

    def test_is_not_complete_when_only_has_one_ball(self):
        self.frame.rolls =[1]
        self.assertEqual(False, self.frame.is_complete())

    def test_is_complete_when_is_strike(self):
        self.frame.add_roll(10)
        self.assertEqual(True, self.frame.is_complete())

    def test_is_complete_when_has_two_balls(self):
        self.frame.rolls =[1, 2]
        self.assertEqual(True, self.frame.is_complete())

    def test_is_complete_when_is_tenth_frame_and_has_three_balls(self):
        frame = Frame(10)
        frame.rolls = [1, 9, 10]
        self.assertEqual(True, frame.is_complete())

    def test_is_complete_when_is_tenth_and_has_two_balls_without_strike_or_spare(self):
        frame = Frame(10)
        frame.rolls = [1, 2]
        self.assertEqual(True, frame.is_complete())

    def test_is_not_complete_when_tenth_frame_and_one_ball_strike(self):
        frame = Frame(10)
        frame.rolls = [10]
        self.assertEqual(False, frame.is_complete())

    def test_is_not_complete_when_tenth_frame_and_two_ball_strike(self):
        frame = Frame(10)
        frame.rolls = [10, 2]
        self.assertEqual(False, frame.is_complete())

    def test_is_not_complete_when_tenth_frame_and_two_balls_spare(self):
        frame = Frame(10)
        frame.rolls = [1, 9]
        self.assertEqual(False, frame.is_complete())

    def test_is_not_complete_when_tenth_frame_and_only_one_ball(self):
        frame = Frame(10)
        frame.rolls = [1]
        self.assertEqual(False, frame.is_complete())

    def test_total_pins_return_sum_of_rolls(self):
        self.frame.rolls =[1, 2]
        self.assertEqual(3, self.frame.total_pins)


from bowling.models import BowlingModel

class BowlingTests(TestCase):

    def setUp(self):
        self.game = BowlingGame()

    def roll_many(self, pins, times):
        for _ in range(times):
            self.game.throw(pins)

    def test_starts_all_rolls_with_empty_list(self):
        self.assertEqual([], self.game.all_rolls)

    def test_starts_game_with_first_frame(self):
        self.assertEqual([self.game.active_frame], self.game.frames)

    def test_throw_adds_to_rolls(self):
        self.game.all_rolls = [10]
        self.game.throw(1)
        self.assertEqual([10, 1], self.game.all_rolls)

    def test_scores_zero_score_game(self):
        self.roll_many(0, 20)
        self.assertEqual(0, self.game.score_for_frame())

    def test_scores_all_ones(self):
        self.roll_many(1, 20)
        self.assertEqual(20, self.game.score_for_frame())

    def test_scores_spare_properly(self):
        self.roll_many(5, 3)
        self.roll_many(0, 17)
        self.assertEqual(20, self.game.score_for_frame())

    def test_scores_perfect_game(self):
        self.roll_many(10, 12)
        self.assertEqual(300, self.game.score_for_frame())

    def test_scores_strike_and_other(self):
        self.game.throw(10)
        self.roll_many(3, 2)
        self.roll_many(0, 16)
        
        self.assertEqual(22, self.game.score_for_frame())

    def test_scores_all_strikes_and_spare_in_tenth(self):
        self.roll_many(10, 9)
        self.game.throw(8)
        self.game.throw(2)
        self.game.throw(10)
        self.assertEqual(278, self.game.score_for_frame())

    def test_add_new_frame_adds_frame_to_frames_list(self):
        # note, instantiating the game starts the first frame
        self.game.add_new_frame()
        self.assertEqual(2, len(self.game.frames))
        self.assertTrue(isinstance(self.game.frames[1], Frame))

    def test_add_new_frame_sets_active_frame_to_new_frame(self):
        existing_frame = Frame(1)
        self.game.frames = [existing_frame]

        self.game.add_new_frame()
        new_frame = self.game.frames[-1]
        self.assertEqual(new_frame, self.game.active_frame)
        self.assertEqual(False, new_frame.is_tenth)
        self.assertNotEqual(existing_frame, self.game.active_frame)

    def test_add_new_frame_sends_frame_number_to_frame(self):

        self.assertEqual(1, self.game.active_frame.number)
        self.game.add_new_frame()
        self.assertEqual(2, self.game.active_frame.number)
        self.game.add_new_frame()
        self.assertEqual(3, self.game.active_frame.number)

    def test_adds_new_frame_on_throw_when_active_frame_is_complete(self):
        active_frame = Frame(1)
        active_frame.rolls = [1,2]
        self.game.frames = [active_frame]
        self.game.active_frame = active_frame

        self.game.throw(5)
        new_frame = self.game.frames[-1]

        self.assertEqual(2, len(self.game.frames))
        self.assertEqual([5], new_frame.rolls)
        self.assertEqual(new_frame, self.game.active_frame)

    def test_throw_adds_pins_to_active_frame(self):
        active_frame = Frame(1)
        self.game.active_frame = active_frame

        self.game.throw(1)
        self.game.throw(5)
        self.assertEqual([1, 5], active_frame.rolls)

    def test_game_has_more_throws_when_active_frame_is_not_tenth(self):
        active_frame = Frame(1)
        self.game.active_frame = active_frame
        self.assertEqual(True, self.game.more_throws)

    def test_game_has_more_throws_when_tenth_frame_but_not_complete(self):
        active_frame = Frame(10)
        self.game.active_frame = active_frame
        self.assertEqual(True, self.game.more_throws)

    def test_game_does_not_have_more_throws_when_active_frame_is_tenth_and_is_complete(self):
        active_frame = Frame(10)
        active_frame.rolls = [10, 10, 10]
        self.game.active_frame = active_frame
        self.assertEqual(False, self.game.more_throws)

    def test_current_frame_returns_active_frame_number_when_not_complete(self):
        active_frame = Frame(1)
        active_frame.rolls = [5]
        self.game.active_frame = active_frame

        self.assertEqual(1, self.game.current_frame)

    def test_current_frame_returns_active_frame_plus_one_when_already_complete(self):
        active_frame = Frame(1)
        active_frame.rolls = [10]
        self.game.active_frame = active_frame

        self.assertEqual(2, self.game.current_frame)

    def test_pins_for_frame_returns_frame_rolls_for_corresponding_frame(self):
        frame_rolls = [1, 9]
        self.game.active_frame.rolls = frame_rolls

        self.assertEqual(frame_rolls, self.game.pins_for_frame(1))

    def test_pins_for_frame_returns_frame_rolls_on_arbitrary_frame(self):
        self.game.frames = [Frame(x) for x in range(1,11)]

        frame_rolls = [3, 5]
        self.game.frames[5].rolls = frame_rolls
        self.assertEqual(frame_rolls, self.game.pins_for_frame(6))

class BowlingLaneTests(TestCase):

    def setUp(self):
        self.lane = BowlingLane()

    @mock.patch('__builtin__.raw_input')
    def test_prompts_for_name_when_prompt_for_bowlers_called(self, input_mock):
        lane = BowlingLane()
        lane.prompt_for_bowlers()
        input_mock.assert_called_with(ADD_BOWLER_PROMPT)

    @mock.patch('__builtin__.raw_input')
    @mock.patch('bowling.game.BowlingLane.add_bowler')
    def test_calls_add_bowler_4_times_with_valid_raw_input_value(self, add_bowler, input_mock):
        lane = BowlingLane()
        lane.prompt_for_bowlers()
        add_bowler.assert_called_with(input_mock.return_value)
        self.assertEqual(4, add_bowler.call_count)

    @mock.patch('__builtin__.raw_input')
    @mock.patch('bowling.game.BowlingLane.add_bowler')
    def test_does_not_call_add_bowler_when_no_input_value(self, add_bowler, input_mock):
        input_mock.return_value = ''

        lane = BowlingLane()
        lane.prompt_for_bowlers()
        self.assertFalse(add_bowler.called)

    @mock.patch('__builtin__.raw_input')
    @mock.patch('bowling.game.BowlingLane.add_bowler')
    def test_breaks_from_add_bowler_loop_when_no_name_entered(self, add_bowler, input_mock):

        name_list = ['aaron', 'dave', '']
        def side_effect(*args):
            return name_list.pop(0) if name_list else ''


        input_mock.side_effect=side_effect

        lane = BowlingLane()
        lane.prompt_for_bowlers()

        self.assertEqual(3, input_mock.call_count)
        self.assertEqual([
            (('aaron',), {}),
            (('dave',), {}),
        ], add_bowler.call_args_list)

    @mock.patch('bowling.game.BowlingGame')
    def test_player_is_added_to_bowlers(self, game_class):
        self.lane.add_bowler('dave')
        self.assertEqual([['dave', game_class.return_value]], self.lane._bowlers)
        game_class.assert_called_once_with()

    @mock.patch('bowling.game.BowlingGame')
    def test_multiple_players_are_added_to_bowlers(self, game_class):

        dave_game = mock.Mock(spec_set=BowlingGame)
        aaron_game = mock.Mock(spec_set=BowlingGame)
        game_list = [dave_game, aaron_game]
        def side_effect(*args):
            return game_list.pop(0)
        game_class.side_effect = side_effect

        self.lane.add_bowler('dave')
        self.lane.add_bowler('aaron')
        self.assertEqual([
            ['dave', dave_game],
            ['aaron', aaron_game]
        ], self.lane._bowlers)

    @mock.patch('bowling.game.BowlingLane._get_all_bowler_throws')
    def test_play_game_calls_get_all_bowler_throws_for_1_thru_10(self, get_all_throws):
        self.lane.play_game()
        self.assertEqual([
            ((1, ),{}),
            ((2, ),{}),
            ((3, ),{}),
            ((4, ),{}),
            ((5, ),{}),
            ((6, ),{}),
            ((7, ),{}),
            ((8, ),{}),
            ((9, ),{}),
            ((10, ),{}),
        ], get_all_throws.call_args_list)

    @mock.patch('bowling.game.BowlingLane._get_user_throws')
    def test_get_user_throws_for_each_bowler(self, get_user_throws):
        game_1 = mock.Mock(spec_set=BowlingGame)
        game_2 = mock.Mock(spec_set=BowlingGame)
        self.lane._bowlers = [
            ['bowler_one', game_1],
            ['bowler_two', game_2],
        ]

        self.lane._get_all_bowler_throws(1)
        self.assertEqual([
            ((game_1, ),{}),
            ((game_2, ),{}),

        ], get_user_throws.call_args_list)

    @mock.patch('__builtin__.raw_input')
    def test_prompts_for_user_throw(self, input_mock):
        input_mock.return_value = "0"
        lane = BowlingLane()
        lane._get_throw(mock.Mock(spec_set=BowlingGame))
        input_mock.assert_called_with(THROW_BALL_PROMPT)

    @mock.patch('__builtin__.raw_input')
    def test_calls_throw_on_game_with_integer_of_number_of_pins_entered(self, input_mock):
        input_mock.return_value = "10"
        game = mock.Mock(spec_set=BowlingGame)

        lane = BowlingLane()
        lane._get_throw(game)
        game.throw.assert_called_once_with(10)

    @mock.patch('bowling.game.BowlingLane._get_throw')
    def test_gets_user_throw_only_once_when_game_is_complete(self, get_throw):
        game = mock.Mock(spec_set=BowlingGame)
        game.active_frame.is_complete.return_value = True

        self.lane._get_user_throws(game)
        get_throw.assert_called_once_with(game)

    @mock.patch('bowling.game.BowlingLane._get_throw')
    def test_get_throw_called_utill_frame_is_complete(self, get_throw):

        is_complete_values = [False, True]
        def side_effect(*args):
            return is_complete_values.pop(0)

        game = mock.Mock(spec_set=BowlingGame)
        game.active_frame.is_complete.side_effect = side_effect

        self.lane._get_user_throws(game)
        self.assertEqual([
            ((game,), {}),
            ((game,), {}),
        ], get_throw.call_args_list)


    @mock.patch('bowling.game.BowlingGame.score_for_frame')
    def test_saves_the_name_and_score_of_all_games(self, score_for_frame):
        self.lane._bowlers = [['carl', BowlingGame()]]

        score_for_frame.return_value = 1

        with mock.patch('bowling.models.BowlingModel.objects.create') as create:
            self.lane.display_results()

        create.assert_called_once_with(name="carl", score="[1]" * 10)

class BowlingModelTests(TestCase):
    def test_saves_bowler_name(self):
        model = BowlingModel(name='carl')
        model.save()

        carl_model = BowlingModel.objects.get(name='carl')

        self.assertEqual(model, carl_model)