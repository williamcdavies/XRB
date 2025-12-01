from django.db import models

class XRBTable(models.Model):
    name = models.CharField(max_length=255, null=True)
    dist = models.FloatField(null=True)
    distErr = models.FloatField(null=True)
    rl = models.CharField(max_length=50, null=True)
    incl = models.FloatField(null=True)
    incl_err = models.FloatField(null=True)
    hardline_slope = models.FloatField(null=True)
    hardline_slope_err = models.FloatField(null=True)
    spec_type = models.CharField(max_length=100, null=True)
    porb = models.FloatField(null=True)
    mass = models.FloatField(null=True)