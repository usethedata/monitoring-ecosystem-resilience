
data_collections = {
    'Sentinel2' : {
        'collection_name': 'COPERNICUS/S2',
        'data_type': 'vegetation',
        'RGB_bands': ['B4','B3','B2'],
        'NIR_band': 'B8',
        'mask_cloud': True,
        'cloudy_pix_frac': 50,
        'cloudy_pix_flag': 'CLOUDY_PIXEL_PERCENTAGE',
        'time_per_point': "1m"
    },
    'Landsat8' : {
        'collection_name': 'LANDSAT/LC08/C01/T1_SR',
        'data_type': 'vegetation',
        'RGB_bands': ['B4','B3','B2'],
        'NIR_band': 'B5',
        'cloudy_pix_flag': 'CLOUD_COVER',
        'time_per_point': "3m"
    },
    'Landsat5' : {
        'collection_name': 'LANDSAT/LT05/C01/T1_SR',
        'data_type': 'vegetation',
        'RGB_bands': ['B3','B2','B1'],
        'NIR_band': 'B4',
        'cloudy_pix_flag': 'None',
        'time_per_point': "3m"
    },
    'Landsat4' : {
        'collection_name': 'LANDSAT/LT04/C01/T1_SR',
        'data_type': 'vegetation',
        'RGB_bands': ['B3','B2','B1'],
        'NIR_band': 'B4',
        'cloudy_pix_flag': 'None',
        'time_per_point': "3m"
    },
    'ERA5' : {
        'collection_name': 'ECMWF/ERA5/MONTHLY',
        'data_type': 'weather',
        'precipitation_band': ['total_precipitation'],
        'temperature_band': ['mean_2m_air_temperature'],
        'time_per_point': "1m"
    }
}