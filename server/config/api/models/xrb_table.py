from django.db import models


class XRB(models.Model):

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="name",       
    )

    dist = models.FloatField(
        null=True,
        blank=True,
        db_column="distance",
    )

    distErr = models.FloatField(
        null=True,
        blank=True,
        db_column="dist_err",
    )

    rl = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="rl",
    )

    incl = models.FloatField(
        null=True,
        blank=True,
        db_column="incl",
    )

    incl_err = models.FloatField(
        null=True,
        blank=True,
        db_column="incl_err",
    )

    hardline_slope = models.FloatField(
        null=True,
        blank=True,
        db_column="hard_slope"

    hardline_slope_err = models.FloatField(
        null=True,
        blank=True,
        db_column="hard_slope_err",
    )

    spec_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="spec_type",
    )

    porb = models.FloatField(
        null=True,
        blank=True,
        db_column="porb",
    )

    mass = models.FloatField(
        null=True,
        blank=True,
        db_column="mass",
    )

    class Meta:
        db_table = "xrb"

    def __str__(self):
        return self.name or f"XRB #{self.pk}"
