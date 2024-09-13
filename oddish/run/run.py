import os
import pytz
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import webbrowser


class Run:
    def __init__(self, run_config):
        self.date_of_birth = run_config['date_of_birth']
        self.sex = run_config['sex']

        self.weight = run_config['weight']
        self.resting_heart_rate = run_config['resting_heart_rate']
        self.v02_max = run_config['v02_max']
        self.heart_rate_variability_sdnn = run_config['heart_rate_variability_sdnn']
        
        self.temperature = run_config['temperature']
        self.humidity = run_config['humidity']
        self.time_zone = run_config['time_zone']
        
        self.id = run_config['id']
        self.route_id = run_config['route_id']
        self.route_file = run_config['route_file']
        
        self.duration = run_config['duration']
        self.start_date = run_config['start_date']
        self.end_date = run_config['end_date']
        
        self.active_energy = run_config['active_energy']
        self.basal_energy = run_config['basal_energy']
        
        self.distance = run_config['distance']
        self.elevation_ascended = run_config['elevation_ascended']
        
        self.heart_rate = run_config['heart_rate']
        self.route_gpx = run_config['route_gpx']

        self.route_gpx_gdf = gpd.GeoDataFrame(
            self.route_gpx, 
            geometry=gpd.points_from_xy(self.route_gpx.lon, self.route_gpx.lat),
            crs="EPSG:4326"
        )

        self.interpolate_heart_rate()
        self.pace_per_heart_beat = self.calc_pace_per_heart_rate()

        # self.simple_graph([
        #     # {'value': 'pace_per_beat', 'windows': [1]},
        #     {'value': 'heart_rate', 'windows': [1]},
        #     # {'value': 'pace', 'windows': [50]},
        #     # {'value': 'elevation', 'windows': [1, 5, 10]},
        # ])

    def interpolate_heart_rate(self):
        self.heart_rate['status'] = 'real'
        self.heart_rate = self.heart_rate.set_index('startDate')
        resampled_heart_rate = self.heart_rate.resample('1S').asfreq()
        resampled_heart_rate['value'] = resampled_heart_rate['value'].interpolate(method='time')
        resampled_heart_rate['status'] = resampled_heart_rate['status'].fillna('sampled')
        self.heart_rate = resampled_heart_rate
        self.heart_rate = self.heart_rate.reset_index()
        return


    def calc_pace_per_heart_rate(self):
        print(self.route_gpx)
        print(self.heart_rate)
        pace_per_heart_rate = self.route_gpx.speed / self.heart_rate['value']
        return pace_per_heart_rate


    def leaflet_display_run(self, config={}, out_file=None, open_browser=True):
        
        if out_file is None:
            out_file = f'runs/{self.id}.html'
        os.makedirs('runs', exist_ok=True)

        map_html = self.route_gpx_gdf.explore(
            **config
        ).save(out_file)

        if open_browser:
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            full_path = os.path.abspath(out_file)
            webbrowser.get(chrome_path).open(full_path)


    def get_data_from_type(self, data_types):
        if not isinstance(data_types, list):
            data_types = [data_types]

        graph_data_list = []
        for data_type in data_types:
            graph_data = None
            if data_type == 'heart_rate':
                graph_data = {
                    'x': self.heart_rate['startDate'],
                    'y': self.heart_rate['value'],
                    'xlabel': 'Time',
                    'ylabel': 'Heart Rate',
                }
            elif data_type == 'pace':
                # Convert meters per second to miles per hour
                graph_data = {
                    'x': self.route_gpx.time,
                    'y': self.route_gpx.speed * 2.23694,
                    'xlabel': 'Time',
                    'ylabel': 'Pace (mph)',
                }
            elif data_type == 'elevation':
                graph_data = {
                    'x': self.route_gpx.time,
                    'y': self.route_gpx.ele,
                    'xlabel': 'Time',
                    'ylabel': 'Elevation',
                }
            elif data_type == 'pace_per_beat':
                graph_data = {
                    'x': self.route_gpx.time,
                    'y': self.pace_per_heart_beat,
                    'xlabel': 'Time',
                    'ylabel': 'Pace per Heart Beat',
                }
            if graph_data:
                graph_data_list.append(graph_data)
        return graph_data_list


    def simple_graph(self, data_configs):
        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx() if len(data_configs) > 1 else None

        color_cycle = plt.cm.tab10.colors
        color_index = 0

        for i, data_config in enumerate(data_configs):
            data_type = data_config['value']
            smoothing_windows = data_config.get('windows', [1])
            graph_data_list = self.get_data_from_type([data_type])
            graph_data = graph_data_list[0]
            ax = ax1 if i == 0 else ax2

            for smoothing_window in smoothing_windows:
                smoothed_values = graph_data['y'].rolling(window=smoothing_window, min_periods=1).mean()
                smooth_label = f'[{smoothing_window}]' if smoothing_window > 1 else ''
                ax.plot(graph_data['x'], smoothed_values, label=f'{data_type} {smooth_label}', color=color_cycle[color_index % len(color_cycle)])
                color_index += 1

            ax.set_xlabel(graph_data['xlabel'])
            ax.set_ylabel(graph_data['ylabel'])

        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M', tz=self.time_zone))

        default_title = f'{self.distance:.2f} miles in {self.duration:.2f} minutes at {self.start_date:%H:%M} on {self.start_date:%Y-%m-%d}'
        ax1.set_title(default_title)

        if len(data_configs) > 1:
            fig.legend(loc='upper right')

        plt.show()
        return


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
        route_gpx = routes[routes['route_id'] == route_id].drop(columns=['route_id'])

        time_zone = pytz.timezone(workout['HKTimeZone'])

        run_config = {
            'id': workout['HKMetadataKeySyncIdentifier'],
            'route_id': route_id,
            'time_zone': time_zone,
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
            'route_gpx': route_gpx,
        }

        return Run(run_config)
