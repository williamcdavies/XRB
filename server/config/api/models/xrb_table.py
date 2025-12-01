from django.db import models


class XRBTable(models.Model):
    # id: AutoField primary key is created automatically

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="Name",         # matches existing Postgres column
    )

    dist = models.FloatField(
        null=True,
        blank=True,
        db_column="Distance",
    )

    distErr = models.FloatField(
        null=True,
        blank=True,
        db_column="Distance Error",
    )

    rl = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column="RL/RQ Flag",
    )

    incl = models.FloatField(
        null=True,
        blank=True,
        db_column="Inclination",
    )

    incl_err = models.FloatField(
        null=True,
        blank=True,
        db_column="Inclination Error",
    )

    hardline_slope = models.FloatField(
        null=True,
        blank=True,
        db_column="Emission Variance (EV)",
    )

    hardline_slope_err = models.FloatField(
        null=True,
        blank=True,
        db_column="EV Error",
    )

    spec_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="Star Type",
    )

    porb = models.FloatField(
        null=True,
        blank=True,
        db_column="Orbital Period",
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
