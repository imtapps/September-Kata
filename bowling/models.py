from django.db import models

class BowlingScore(models.Model):
    name = models.CharField(max_length=30)
    score = models.TextField()

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.filter(name=name)