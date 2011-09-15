import mock
from lettuce import before, after

@before.each_scenario
def patch_stdin(scenario):
    scenario.stdin = mock.patch('__builtin__.raw_input')
    scenario.raw_input = scenario.stdin.start()

@after.each_scenario
def unpatch_stdin(scenario):
    scenario.stdin.stop()
