from django.db import models

# Create your models here.
class Scores(models.Model):
    score = models.CharField(max_length=100)