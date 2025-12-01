from django.db import models


class LRLX(models.Model):
    

    class Meta:
        db_table = "lrlx_data"

    def __str__(self):
        return ""