from django.contrib.auth.models import 
from rest_framework             import serializers


class XRBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = XRB
        fields = ["name", "distance", "dist_err", "rl", "incl", "incl_err", "hard_slope", "hard_slope_err", "spec_type", "porb", "mass"]


class LRLXSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LRLX
        fields = ["name", "lrlx_class", "lr", "lr_ler", "lr_uer", "lx", "lx_ler", "lx_uer", "uplink", "alpha", "nu", "e1_measured", "e2_measured", "gamma", "time", "ref"]