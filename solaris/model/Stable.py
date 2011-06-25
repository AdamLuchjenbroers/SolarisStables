# -*- coding: iso-8859-1 -*-
from django.db import models

class Stable(models.Model):
  StableName = models.CharField(max_length=200)
  login = models.CharField(max_length=20)
  Reputation = models.IntegerField()
  


