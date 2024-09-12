import pandas as pd
import json
import geopandas as gpd
import webbrowser

class Run:
    def __init__(self, run_config):
        
        gpx = run_config['route_info']

        gdf = gpd.GeoDataFrame(
            gpx, 
            geometry=gpd.points_from_xy(gpx.lon, gpx.lat),
            crs="EPSG:4326"  # WGS84 coordinate system
        )

                # Visualize using geopandas.explore and save to HTML
        map_html = gdf.explore(
            tiles='Stadia.AlidadeSmoothDark', 
            popup=True,  # Enable popups
            tooltip=['time', 'speed', 'course', 'hAcc', 'vAcc'],  # Add tooltips
        ).save('map.html')

        # Open the HTML file in the default web browser
        # webbrowser.open('map.html')

        pass

    @staticmethod
    def from_HKMetadataKey(apple_health_kit, HKMetadataKey):

        date_of_birth = apple_health_kit.characteristics['DateOfBirth']
        sex = apple_health_kit.characteristics['BiologicalSex'].replace('HKBiologicalSex', '').lower()

        workouts = apple_health_kit.workouts['Running']
        workout = workouts[workouts['HKMetadataKeySyncIdentifier'] == HKMetadataKey].copy().iloc[0]
        workout_start_date = workout['startDate']

        weight_table = apple_health_kit.quantities['BodyMass']
        resting_heart_rate_table = apple_health_kit.quantities['RestingHeartRate']
        vo2_max_table = apple_health_kit.quantities['VO2Max']
        heart_rate_variability_sdnn_table = apple_health_kit.quantities['HeartRateVariabilitySDNN']
        
        weight = weight_table[weight_table['startDate'] < workout_start_date].iloc[-1]['value']
        resting_heart_rate = resting_heart_rate_table[resting_heart_rate_table['startDate'] < workout_start_date].iloc[-1]['value']
        v02_max = vo2_max_table[vo2_max_table['startDate'] < workout_start_date].iloc[-1]['value']
        heart_rate_variability_sdnn = heart_rate_variability_sdnn_table[heart_rate_variability_sdnn_table['startDate'] < workout_start_date].iloc[-1]['value']

        heart_rate_table = apple_health_kit.quantities['HeartRate'][['startDate', 'value']]
        heart_rate = heart_rate_table[(heart_rate_table['startDate'] > workout['startDate']) & (heart_rate_table['startDate'] < workout['endDate'])]

        routes = apple_health_kit.routes
        route_id = workout['route_file_reference'].split('/')[-1].split('.gpx')[0]
        route_info = routes[routes['route_id'] == route_id].drop(columns=['route_id'])

        run_config = {
            'date_of_birth': date_of_birth,
            'sex': sex,
            'weight': float(weight),
            'resting_heart_rate': float(resting_heart_rate),
            'v02_max': float(v02_max),
            'heart_rate_variability_sdnn': float(heart_rate_variability_sdnn),
            'duration': float(workout['duration']),
            'start_date': workout['startDate'],
            'end_date': workout['endDate'],
            'temperature': float(workout['HKWeatherTemperature'].replace(' degF', '')),
            'humidity': float(workout['HKWeatherHumidity'].replace(' %', ''))/100,
            'active_energy': float(workout['HKQuantityTypeIdentifierActiveEnergyBurned']),
            'basal_energy': float(workout['HKQuantityTypeIdentifierBasalEnergyBurned']),
            'distance': float(workout['HKQuantityTypeIdentifierDistanceWalkingRunning']),
            'elevation_ascended': float(workout['HKElevationAscended'].replace(' cm', '')),
            'route_file': workout['route_file_reference'],
            'heart_rate': heart_rate,
            'route_info': route_info,
        }

        return Run(run_config)
