from cStringIO import StringIO
import mock

from django.core.management import call_command

__all__ = ('run_django_command', )

def run_django_command(step, command, *args, **kwargs):
    step.scenario.output = StringIO()
    with mock.patch('sys.stdout', step.scenario.output):
        call_command(command, *args, **kwargs)
