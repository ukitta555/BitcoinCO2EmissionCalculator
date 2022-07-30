var wms_layers = [];


        var lyr_OSMStandard_0 = new ol.layer.Tile({
            'title': 'OSM Standard',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' &middot; <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors, CC-BY-SA</a>',
                url: 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_Hospitals_1 = new ol.format.GeoJSON();
var features_Hospitals_1 = format_Hospitals_1.readFeatures(json_Hospitals_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Hospitals_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Hospitals_1.addFeatures(features_Hospitals_1);
var lyr_Hospitals_1 = new ol.layer.Heatmap({
                declutter: true,
                source:jsonSource_Hospitals_1, 
                radius: 1 * 2,
                gradient: ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'],
                blur: 15,
                shadow: 250,
                title: 'Hospitals'
            });

lyr_OSMStandard_0.setVisible(true);lyr_Hospitals_1.setVisible(true);
var layersList = [lyr_OSMStandard_0,lyr_Hospitals_1];
