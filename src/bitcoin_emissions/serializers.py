from typing import OrderedDict
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField
from django.db.models import Sum

from src.bitcoin_emissions.consts import CLOUDFLARE_LOCATION_DATA, UNKNOWN_POOL, UNKNOWN_POOL_USER_VIEW
from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, Location, \
    HashRatePerPoolServer, AverageEfficiency, BitcoinDifficulty, NetworkHashRate
from src.bitcoin_emissions.models.co2_electricity_history_per_server_db_model import CO2ElectricityHistoryPerServer


class ServerHashrateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashRatePerPoolServer
        fields = [
            "blockchain_pool_name",
            "hash_rate"
        ]

    blockchain_pool_name = SerializerMethodField()
    hash_rate = serializers.FloatField()

    def get_blockchain_pool_name(self, obj: HashRatePerPoolServer):
        if obj.blockchain_pool.pool_name == UNKNOWN_POOL:
            return UNKNOWN_POOL_USER_VIEW
        return obj.blockchain_pool.pool_name


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

    def get_servers_at_location(self, obj: PoolElectricityConsumptionAndCO2EEmissionHistory):
        hashrate_queryset = HashRatePerPoolServer.objects.filter(
            date=obj.date,
            blockchain_pool_location=obj.location_of_servers.uuid
        )
        hashrate_data: OrderedDict = ServerHashrateSerializer(hashrate_queryset, many=True).data

        granural_data_queryset = CO2ElectricityHistoryPerServer.objects.filter(
            date=obj.date,
            server_info__blockchain_pool_location=obj.location_of_servers.uuid
        )
        total_electricity = 0
        total_co2e = 0
        for server_hashrate in hashrate_data:
            # even if there are two servers at the same location for the same pool at the same date
            # electricity consumption/co2 emissions are the same for them, therefore we can just fetch any of them to return to the end user
            # unknown/unrecognized pools are always shoved in one mega-pool, meaning that the logic is correct for these cases as well.
            try:
                blockchain_pool_name = server_hashrate['blockchain_pool_name'] 
                if blockchain_pool_name == UNKNOWN_POOL_USER_VIEW:
                    blockchain_pool_name = UNKNOWN_POOL
                server_emissions = granural_data_queryset.filter(
                    server_info__blockchain_pool__pool_name=blockchain_pool_name
                )[0]
            except Exception as e:
                # print(obj.date)
                # print(server_hashrate['blockchain_pool_name'])
                # print(obj.location_of_servers.location_name)
                raise(e)
            server_hashrate['electricity_usage'] = server_emissions.electricity_usage
            server_hashrate['co2e_emissions'] = server_emissions.co2e_emissions
            total_electricity += server_emissions.electricity_usage
            total_co2e += server_emissions.co2e_emissions
        
        # print(obj.electricity_usage, total_electricity)
        # print(obj.co2e_emissions, total_co2e)
        assert(abs(total_electricity - obj.electricity_usage) <= 10 ** (-5))
        assert(abs(total_co2e - obj.co2e_emissions) <= 10 ** (-5))
        
        return hashrate_data

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


class ServerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CO2ElectricityHistoryPerServer
        fields = [
            "longitude",
            "latitude",
            "location_name",
            "electricity_usage",
            "co2e_emissions",
            "is_cloudflare"
        ]

    is_cloudflare = SerializerMethodField()
    location_name = SerializerMethodField()
    longitude = SerializerMethodField()
    latitude = SerializerMethodField()

    def get_is_cloudflare(self, obj: CO2ElectricityHistoryPerServer):
        location_obj = Location.objects.get(uuid=obj.server_info.blockchain_pool_location.uuid)
        if location_obj.location_name == CLOUDFLARE_LOCATION_DATA[0]:
            return True
        return False
    
    def get_location_name(self, obj: CO2ElectricityHistoryPerServer):
        return obj.server_info.blockchain_pool_location.location_name
    
    def get_longitude(self, obj: CO2ElectricityHistoryPerServer):
        return obj.server_info.blockchain_pool_location.longitude

    def get_latitude(self, obj: CO2ElectricityHistoryPerServer):
        return obj.server_info.blockchain_pool_location.latitude
    


    


class EmissionSerializerPerPool(serializers.ModelSerializer):
    class Meta:
        model = CO2ElectricityHistoryPerServer
        fields = [
            'date',
            'blockchain_pool_name',
            'servers_at_locations',
            'electricity_usage',
            'co2e_emissions',
        ]

    blockchain_pool_name = SerializerMethodField()
    servers_at_locations = SerializerMethodField()
    electricity_usage = SerializerMethodField()
    co2e_emissions = SerializerMethodField()


    def get_blockchain_pool_name(self, obj: CO2ElectricityHistoryPerServer):
        if obj.server_info.blockchain_pool.pool_name == UNKNOWN_POOL:
            return UNKNOWN_POOL_USER_VIEW
        return obj.server_info.blockchain_pool.pool_name
    
    def get_servers_at_locations(self, obj: CO2ElectricityHistoryPerServer):
        history_queryset = CO2ElectricityHistoryPerServer.objects.filter(
            server_info__blockchain_pool__pool_name = obj.server_info.blockchain_pool.pool_name,
            date = obj.date
        )
        pool_servers_locations: OrderedDict = ServerHistorySerializer(history_queryset, many=True).data
        return pool_servers_locations

    def get_electricity_usage(self, obj: CO2ElectricityHistoryPerServer):
        history_queryset = CO2ElectricityHistoryPerServer.objects.filter(
            server_info__blockchain_pool__pool_name = obj.server_info.blockchain_pool.pool_name,
            date = obj.date
        )
        result =  history_queryset.aggregate(total_electricity = Sum('electricity_usage'))["total_electricity"]
        return result

    def get_co2e_emissions(self, obj: CO2ElectricityHistoryPerServer):
        history_queryset = CO2ElectricityHistoryPerServer.objects.filter(
            server_info__blockchain_pool__pool_name = obj.server_info.blockchain_pool.pool_name,
            date = obj.date
        )
        result = history_queryset.aggregate(total_emissions = Sum('co2e_emissions'))["total_emissions"]
        return result

