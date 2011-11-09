
from django.views.generic import TemplateView

from bowling.models import BowlingScore

class BowlerScores(TemplateView):
    template_name = 'bowling/scores.html'

    def get_context_data(self, **kwargs):
        bowler = self.kwargs['bowler']
        return {
            'bowler': bowler,
            'games': BowlingScore.get_by_name(bowler)
        }