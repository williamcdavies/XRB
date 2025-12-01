from django.db import models


class LRLX(models.Model):
    class Meta:
        db_table = "lrlx_data"
    
    name = models.CharField(

    )

    # replaced `class` with `lrlx_class` since `class` is a reserved keyword.
    lrlx_class = models.CharField(
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

    uplim = models.CharField(
        
    )

    alpha = models.ChaFloatFieldrField(
        
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