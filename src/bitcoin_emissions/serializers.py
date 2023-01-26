from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, DateTimeField, DateField, CharField

from src.bitcoin_emissions.consts import CLOUDFLARE_LOCATION_DATA
from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, Location, \
    HashRatePerPoolServer, AverageEfficiency, BitcoinDifficulty, NetworkHashRate


class ServerHashRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashRatePerPoolServer
        fields = [
            "blockchain_pool_name",
            "hash_rate",
        ]

    blockchain_pool_name = CharField(source="blockchain_pool.pool_name")
    hash_rate = serializers.FloatField()


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
            'location_of_servers',
            'servers_at_location',
            'is_cloudflare',
            'averaged_difficulty',
            'network_hash_rate_720_block_window',
            'averaged_gear_efficiency',
        ]

    location_of_servers = LocationSerializer()
    co2e_emissions = serializers.FloatField()
    electricity_usage = serializers.FloatField()
    servers_at_location = SerializerMethodField()
    is_cloudflare = SerializerMethodField()
    averaged_gear_efficiency = SerializerMethodField()
    averaged_difficulty = SerializerMethodField()
    network_hash_rate_720_block_window = SerializerMethodField()

    def get_servers_at_location(self, obj):
        queryset = HashRatePerPoolServer.objects.filter(
            date=obj.date,
            blockchain_pool_location=obj.location_of_servers.uuid
        )
        return ServerHashRateSerializer(queryset, many=True).data

    def get_is_cloudflare(self, obj):
        location_obj = Location.objects.get(uuid=obj.location_of_servers.uuid)
        if location_obj.location_name == CLOUDFLARE_LOCATION_DATA[0]:
            return True
        return False

    def get_averaged_gear_efficiency(self, obj):
        return AverageEfficiency.objects.get(
            date=obj.date
        ).average_efficiency_j_gh

    def get_averaged_difficulty(self, obj):
        return BitcoinDifficulty.objects.get(
            date=obj.date
        ).difficulty

    def get_network_hash_rate_720_block_window(self, obj):
        return NetworkHashRate.objects.get(
            date=obj.date
        ).network_hash_rate_eh_s
