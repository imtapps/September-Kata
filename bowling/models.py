from django.db import models



class BowlingModel(models.Model):
    name = models.CharField(max_length=20)
