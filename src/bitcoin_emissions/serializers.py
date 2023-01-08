from rest_framework import serializers

from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "longitude",
            "latitude",
            "location_name"
        ]


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolElectricityConsumptionAndCO2EEmissionHistory
        fields = [
            'date',
            'electricity_usage',
            'co2e_emissions',
            'location_of_servers'
        ]

    location_of_servers = LocationSerializer()