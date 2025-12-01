from django.contrib.auth.models import 
from rest_framework             import serializers


class XRBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = XRB
        fields = ["name", "distance", "dist_err", "rl", "incl", "incl_err", "hard_slope", "hard_slope_err", "spec_type", "porb", "mass"]