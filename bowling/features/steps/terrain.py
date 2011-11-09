import mock
from lettuce import before, after

from south.management.commands import patch_for_test_db_setup
from django.db import connection
from django.core.management import call_command

@before.all
def setup_test_database():
    patch_for_test_db_setup()
    connection.creation.create_test_db(verbosity=0, autoclobber=True)

@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False)

@before.each_scenario
def patch_stdin(scenario):
    scenario.stdin = mock.patch('__builtin__.raw_input')
    scenario.raw_input = scenario.stdin.start()

@after.each_scenario
def unpatch_stdin(scenario):
    scenario.stdin.stop()
