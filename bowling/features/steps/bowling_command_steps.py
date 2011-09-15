# -*- coding: utf-8 -*-
import re
from bowling.features.steps.step_utilities import run_django_command
from lettuce import step

@step(u'Given I am the bowler "([^"]*)"')
def set_bowler_name_for_scenario(step, name):
    step.scenario.bowler_name = name

@step(u'(?:Given|And) the games?:')
def seutp_bowling_games(step):
    step.scenario.games = {}

    for game in step.hashes:
        frames = {}
        for column, value in game.items():
            if re.match('^\d{1,2}$', column):
                frames[column] = value

        rolls = []
        for frame in sorted(frames.keys(), cmp=lambda a, b: cmp(int(a), int(b))):
            rolls.append(frames[frame].split(','))

        step.scenario.games[game['name']] = rolls

@step(u'(?:When|And) I run django\'s "(.*)" command$')
def when_i_run_the_bowling_command(step, command):
    users = step.scenario.games.keys()
    user_entry = users + ['']

    for frame_number in range(10):
        for user in users:
            user_entry += step.scenario.games[user][frame_number]

    def side_effect(*args):
        return user_entry.pop(0) if user_entry else ''

    step.scenario.raw_input.side_effect = side_effect
    run_django_command(step, command)

@step(u'When I run django\'s "([^"]*)" command with "([^"]*)"')
def assert_bowling_scores(step, command, argument):
    run_django_command(step, command, *[argument])

@step(u'(?:Then|And) I should see "([^"]*)"')
def assert_perfect_game(step, message):
    output = step.scenario.output.getvalue()
    assert message in output, "%s is not in '%s'" % (message, output)