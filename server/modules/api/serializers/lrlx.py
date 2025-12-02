from modules.api.models import LRLX
from rest_framework     import serializers


class LRLXSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LRLX
        fields = ["name", "classification", "lr", "lr_ler", "lr_uer", "lx", "lx_ler", "lx_uer", "uplink", "alpha", "nu", "e1_measured", "e2_measured", "gamma", "time", "ref", "id"]