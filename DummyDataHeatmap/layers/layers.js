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
var format_DummyDataforheatmap_1 = new ol.format.GeoJSON();
var features_DummyDataforheatmap_1 = format_DummyDataforheatmap_1.readFeatures(json_DummyDataforheatmap_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_DummyDataforheatmap_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_DummyDataforheatmap_1.addFeatures(features_DummyDataforheatmap_1);
var lyr_DummyDataforheatmap_1 = new ol.layer.Heatmap({
                declutter: true,
                source:jsonSource_DummyDataforheatmap_1, 
                radius: 10 * 2,
                gradient: ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'],
                blur: 15,
                shadow: 250,
                title: 'Dummy Data for heat map'
            });

lyr_OSMStandard_0.setVisible(true);lyr_DummyDataforheatmap_1.setVisible(true);
var layersList = [lyr_OSMStandard_0,lyr_DummyDataforheatmap_1];
