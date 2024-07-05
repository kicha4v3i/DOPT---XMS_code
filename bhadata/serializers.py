from rest_framework import serializers
from .models import Drillcollerlength,Drillcollers

class DrillcollersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["normal_od", "normal_id"]
        model = Drillcollers

class DrillcollerlengthSerializer(serializers.ModelSerializer):
    drill_collers = DrillcollersSerializer(source='drillcollers_set',read_only=True, many=True)

    class Meta:
        fields = ["length","drill_collers"]
        model = Drillcollerlength