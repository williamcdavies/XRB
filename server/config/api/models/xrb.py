from django.db import models


class XRB(models.Model):
    class Meta:
        db_table = "xrb_properties"

    name = models.CharField(
        max_length=256,
        primary_key=True
    )

    distance = models.FloatField(
        null=True,
        blank=True
    )

    distance_err = models.FloatField(
        null=True,
        blank=True
    )

    rl = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    incl = models.FloatField(
        null=True,
        blank=True
    )

    incl_err = models.FloatField(
        null=True,
        blank=True
    )

    hard_line_slope = models.FloatField(
        null=True,
        blank=True
    )

    hard_line_slope_err = models.FloatField(
        null=True,
        blank=True
    )

    spec_type = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    p_orb = models.FloatField(
        null=True,
        blank=True
    )

    mass = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name