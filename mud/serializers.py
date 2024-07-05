from rest_framework import serializers
from .models import Pumps,MudPumpMasterData,MudPumpMasterSpeed,MudPumpMasterFlowRate
class MudPumpMasterDataSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['linear_size', 'max_discharge_pressure']
        model = MudPumpMasterData
class MudPumpMasterFlowRateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['flowrate']
        model = MudPumpMasterFlowRate


class MudPumpMasterSpeedSerializer(serializers.ModelSerializer):
    mud_pump_flowrate = MudPumpMasterFlowRateSerializer(source='mudpumpmasterflowrate_set',read_only=True, many=True)

    class Meta:
        fields = ['pump_speed',"mud_pump_flowrate"]
        model = MudPumpMasterSpeed
 

class PumpsSerializer(serializers.ModelSerializer):
    mud_pump_data = MudPumpMasterDataSerializer(source='mudpumpmasterdata_set',read_only=True, many=True)
    mud_pump_master_speed = MudPumpMasterSpeedSerializer(source='mudpumpmasterspeed_set',read_only=True, many=True)

    class Meta:
        fields = ["name","type", "stroke_length", "mud_pump_data","mud_pump_master_speed","unit"]    
        model = Pumps


