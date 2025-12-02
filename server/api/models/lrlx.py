from django.db import models


class LRLX(models.Model):
    class Meta:
        db_table = "lrlx_data"
    
    name = models.CharField(

    )

    # `db_column="class"` prevents naming conflict with serializer.
    # db_column shall be renamed to `classification` in future database patch.
    classification = models.CharField(
        db_column="class"
    )

    lr = models.FloatField(
        
    )

    lr_ler = models.FloatField(
        
    )

    lr_uer = models.FloatField(
        
    )

    lx = models.FloatField(
        
    )

    lx_ler = models.FloatField(
        
    )

    lx_uer = models.FloatField(
        
    )

    # `db_column="uplim"` prevents naming conflict with serializer.
    # db_column shall be renamed to `uplink` in future database patch.
    uplink = models.CharField(
        db_column="uplim"
    )

    alpha = models.FloatField(
        
    )

    nu = models.FloatField(
        
    )

    e1_measured = models.FloatField(
        
    )

    e2_measured = models.FloatField(
        
    )

    gamma = models.FloatField(
        
    )

    time = models.FloatField(
        
    )

    ref = models.CharField(
        
    )

    id = models.BigAutoField(
        primary_key=True
    )

    def __str__(self):
        return ""