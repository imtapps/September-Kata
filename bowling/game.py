from bowling.models import BowlingModel

class Frame(object):

    def __init__(self, number):
        self.number = number
        self.rolls = []

    @property
    def roll_count(self):
        return len(self.rolls)

    @property
    def is_strike(self):
        return bool(self.rolls and self.rolls[0] == 10)

    @property
    def is_spare(self):
        return bool(self.roll_count == 2 and sum(self.rolls[:2]) == 10)

    @property
    def is_tenth(self):
        return self.number == 10

    def add_roll(self, pins):
        self.rolls.append(pins)

    def is_complete(self):
        if self.is_tenth:
            return self.is_tenth_complete()
        return bool(self.is_strike or self.roll_count == 2)

    def is_tenth_complete(self):
        if self.roll_count == 3:
            return True
        return bool(self.roll_count == 2 and not (self.is_strike or self.is_spare))

    @property
    def total_pins(self):
        return sum(self.rolls)

class BowlingGame(object):
    active_frame = None

    def __init__(self):
        self.all_rolls = []
        self.frames = []
        self.add_new_frame()

    @property
    def current_frame(self):
        """
        Represents which frame number the next throw will be
        added to.
        """
        if self.active_frame.is_complete():
            return self.active_frame.number + 1
        return self.active_frame.number

    @property
    def more_throws(self):
        return not (self.active_frame.is_tenth and self.active_frame.is_complete())

    def throw(self, pins):
        if self.active_frame.is_complete():
           self.add_new_frame()

        self.active_frame.add_roll(pins)
        self.all_rolls.append(pins)

    def add_new_frame(self):
        frame_number = len(self.frames) + 1
        self.active_frame = Frame(frame_number)
        self.frames.append(self.active_frame)

    def add_bonus_pins(self, roll_index):
        """
        roll_index is as of the start of the frame.

        If we have a strike, we add the strike plus the next two rolls.

        If we have a spare, we still add three balls...
        first ball, second ball, and the first roll after spare.

        So... we can treat a strike and a spare the same!
        """
        return sum(self.all_rolls[roll_index:roll_index + 3])

    def get_frame_score(self, frame, roll_index):
        if frame.is_strike or frame.is_spare:
            return self.add_bonus_pins(roll_index)
        else:
            return frame.total_pins

    def score_for_frame(self, frame_number=None):
        """
        If there is not a frame number, this will just give you the
        total score, otherwise it gives a running total of the
        score as of the frame number requested.
        """
        total_score = 0
        roll_index = 0
        for frame in self.frames:
            total_score += self.get_frame_score(frame, roll_index)
            roll_index += frame.roll_count

            if frame.number == frame_number:
                break
        return total_score

    def pins_for_frame(self, frame_number):
        """
        self.frames is just a list, so it has a zero-based index.
        the Game example looks like frame will be the actual
        number of the frame, 1-10.
        """
        return self.frames[frame_number - 1].rolls

ADD_BOWLER_PROMPT = 'Enter Bowler Name:'
THROW_BALL_PROMPT = "How many pins did you knock over?:"

class BowlingLane(object):
    max_player_count = 4

    def __init__(self):
        self._bowlers = []

    def add_bowler(self, name):
        self._bowlers.append([name, BowlingGame()])

    def prompt_for_bowlers(self):
        counter = 0
        while counter < self.max_player_count:
            bowler_name = raw_input(ADD_BOWLER_PROMPT)
            if not bowler_name:
                break

            self.add_bowler(bowler_name)
            counter += 1

    def play_game(self):
        for frame in range(1, 11):
            self._get_all_bowler_throws(frame)

    def _get_throw(self, game):
        game.throw(int(raw_input(THROW_BALL_PROMPT)))

    def _get_user_throws(self, game):
        self._get_throw(game)
        while not game.active_frame.is_complete():
            self._get_throw(game)

    def _get_all_bowler_throws(self, frame):
        for name, game in self._bowlers:
            print("\nHey %s, it's your turn for frame %s" % (name, frame))
            self._get_user_throws(game)

    def display_results(self):
        print "\n\nFinal Score\n-----------"
        for name, game in self._bowlers:
            score = ["[%s]" % game.score_for_frame(f) for f in range(1, 11)]
            score_string = ''.join(score)
            print "%s: %s" % (name, score_string)
            BowlingModel.objects.create(name=name, score=score_string)
        print "\n\n"

def main():
    lane = BowlingLane()
    lane.prompt_for_bowlers()
    lane.play_game()
    lane.display_results()

if __name__ == '__main__':
    main()