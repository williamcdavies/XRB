from django.contrib.auth.models import 
from rest_framework             import serializers


class LRLXSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LRLX
        fields = ["name", "class", "lr", "lr_ler", "lr_uer", "lx", "lx_ler", "lx_uer", "uplim", "alpha", "nu", "e1_measured", "e2_measured", "gamma", "time", "ref", "id"]