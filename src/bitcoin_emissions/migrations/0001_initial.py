# Generated by Django 4.1.4 on 2022-12-21 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UUIDModel",
            fields=[
                ("uuid", models.UUIDField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="BitcoinDifficulty",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("date", models.DateField()),
                ("difficulty", models.DecimalField(decimal_places=6, max_digits=50)),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("location_name", models.CharField(max_length=200)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="MiningGear",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("release_date", models.DateField()),
                ("efficiency", models.DecimalField(decimal_places=11, max_digits=12)),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="Pool",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("pool_name", models.CharField(max_length=100)),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="PoolElectricityConsumptionAndCO2EEmissionHistory",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "electricity_usage",
                    models.DecimalField(decimal_places=6, max_digits=24),
                ),
                (
                    "co2e_emissions",
                    models.DecimalField(decimal_places=6, max_digits=24),
                ),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="PoolLocation",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("valid_for_date", models.DateField()),
                (
                    "blockchain_pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bitcoin_emissions.pool",
                    ),
                ),
                (
                    "blockchain_pool_location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bitcoin_emissions.location",
                    ),
                ),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="CO2EmissionFactor",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "co2_emission_factor",
                    models.DecimalField(decimal_places=6, max_digits=15),
                ),
                ("information_source", models.CharField(max_length=100)),
                (
                    "pool_location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bitcoin_emissions.poollocation",
                    ),
                ),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
        migrations.CreateModel(
            name="BlocksFoundByPoolPerWindow",
            fields=[
                (
                    "uuidmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="bitcoin_emissions.uuidmodel",
                    ),
                ),
                ("blocks_found", models.IntegerField()),
                ("window_start_date", models.DateField()),
                ("window_end_date", models.DateField()),
                (
                    "blockchain_pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bitcoin_emissions.pool",
                    ),
                ),
            ],
            bases=("bitcoin_emissions.uuidmodel",),
        ),
    ]
