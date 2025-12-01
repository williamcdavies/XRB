from server.config.api.models import xrb
from rest_framework           import serializers


class XRBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = xrb
        fields = ["name", "distance", "distance_err", "rl", "incl", "incl_err", "hard_line_slope", "hard_line_slope_err", "spec_type", "p_orb", "mass"]