from django.db import models


class LRLX(models.Model):
    class Meta:
        db_table = "lrlx_data"
    
    name = models.CharField(
        max_length=256
    )

    classification = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    lr = models.FloatField(
        null=True,
        blank=True
    )

    lr_ler = models.FloatField(
        null=True,
        blank=True
    )

    lr_uer = models.FloatField(
        null=True,
        blank=True
    )

    lx = models.FloatField(
        null=True,
        blank=True
    )

    lx_ler = models.FloatField(
        null=True,
        blank=True
    )

    lx_uer = models.FloatField(
        null=True,
        blank=True
    )

    uplink = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    alpha = models.FloatField(
        null=True,
        blank=True
    )

    nu = models.FloatField(
        null=True,
        blank=True
    )

    e1_measured = models.FloatField(
        null=True,
        blank=True
    )

    e2_measured = models.FloatField(
        null=True,
        blank=True
    )

    gamma = models.FloatField(
        null=True,
        blank=True
    )

    time = models.FloatField(
        null=True,
        blank=True
    )

    ref = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    id = models.BigAutoField(
        primary_key=True
    )

    def __str__(self):
        return ""