from django.db import models


class XRBTable(models.Model):

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="Name",       
    )

    dist = models.FloatField(
        null=True,
        blank=True,
        db_column="Dist",
    )

    distErr = models.FloatField(
        null=True,
        blank=True,
        db_column="DistErr",
    )

    rl = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="RL",
    )

    incl = models.FloatField(
        null=True,
        blank=True,
        db_column="Incl",
    )

    incl_err = models.FloatField(
        null=True,
        blank=True,
        db_column="InclErr",
    )

    hardline_slope = models.FloatField(
        null=True,
        blank=True,
        db_column="HardlineSlope"

    hardline_slope_err = models.FloatField(
        null=True,
        blank=True,
        db_column="HardlineSlopeErr",
    )

    spec_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="SpecType",
    )

    porb = models.FloatField(
        null=True,
        blank=True,
        db_column="Porb",
    )

    mass = models.FloatField(
        null=True,
        blank=True,
        db_column="Mass",
    )

    class Meta:
        db_table = "xrb_table"

    def __str__(self):
        return self.name or f"XRB #{self.pk}"
