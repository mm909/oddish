
import re
import sys
import time
import glob
import pickle
import logging
import pandas as pd
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class AppleHealthKit:
    """
    A class to handle the ingestion and processing of Apple HealthKit export data.

    This class loads, parses, and converts Apple HealthKit export data into usable 
    structured formats. AppleHealthKit makes no assumptions about data formatting or
    timezones, and the data is stored in raw form. The class provides internal methods
    to extract metadata, characteristics, quantities, workouts, and routes from the
    Apple HealthKit export XML. The class does not have any public facing methods.

    Exporting Apple HealthKit data is done through the Apple Health app on an iOS device.
    Follow https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios
    to export your Apple Health data. 

    Folder Structure of Apple HealthKit Export Data
    ----------------------------------------------
    apple_health_export/
    ├── export.xml
    ├── export_cda.xml
    ├── workout-routes/
    │   ├── route_2021-06-18_7.36am.gpx

    Example Usage
    -------------
    >>> config = {
    >>>     'apple_health_export_folder': 'apple_health_export'
    >>> }
    >>> ahk = AppleHealthKit(config)
    >>> print(ahk.quantities['BodyMass'])

    Attributes
    ----------
    config : dict
        Configuration dictionary containing paths and other settings.
    xml_namespaces : dict
        Dictionary of XML namespaces used in the Apple HealthKit export data.
    apple_health_export_xml_root : xml.etree.ElementTree.Element
        The root element of the Apple HealthKit export XML.
    metadata : dict
        Dictionary containing metadata from the Apple HealthKit export XML.
    characteristics : dict
        Dictionary containing characteristics from the Apple HealthKit export XML.
    quantities : dict
        Dictionary of DataFrames, where the key is the quantity type and the value is the DataFrame.
    workouts : dict
        Dictionary of DataFrames, where the key is the workout type and the value is the DataFrame.
    routes : pandas.DataFrame
        DataFrame containing route data from the Apple HealthKit export XML.

    Methods
    -------
    __init__(self, config)
        Initializes the AppleHealthKit class with the given configuration.
    _ingest_apple_health_data(self)
        Ingests the Apple HealthKit data by loading and parsing the export XML.
    _load_apple_healthkit_export_xml(self)
        Loads the Apple HealthKit export XML file into memory.
    _get_metadata(self)
        Extracts metadata from the Apple HealthKit export XML.
    _get_characteristics(self)
        Extracts characteristics from the Apple HealthKit export XML.
    _build_AHK_quantity_tables(self)
        Builds quantity tables from the Apple HealthKit export XML.
    _build_AHK_workout_tables(self)
        Builds workout tables from the Apple HealthKit export XML.
    _build_AHK_route_tables(self)
        Builds route tables from the Apple HealthKit export XML.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing paths and other settings.
    """

    def __init__(self, apple_health_export_folder):
        self.apple_health_export_folder = apple_health_export_folder
        self.memory_usage_mb = 0
        self.xml_namespaces = {'ahk-workout-route': 'http://www.topografix.com/GPX/1/1'}

        ts = time.time()
        self._ingest_apple_health_data()
        logger.info(f'Apple HealthKit data ingestion complete in {time.time() - ts:.2f} seconds ({self.memory_usage_mb:.2f} MB)')

        return


    def _ingest_apple_health_data(self):
        """
        Ingests the Apple HealthKit data by loading and parsing the export XML.
        """
        self.apple_health_export_xml_root = self._load_apple_healthkit_export_xml()

        ts = time.time()
        logger.info('Ingesting Apple HealthKit data...')

        self.metadata = self._get_metadata()
        self.characteristics = self._get_characteristics()
        self.quantities = self._build_AHK_quantity_tables()
        self.workouts = self._build_AHK_workout_tables()
        self.routes = self._build_AHK_route_tables()

        logger.debug(f'Ingested Apple HealthKit data in {time.time() - ts:.2f} seconds')
        return


    def _load_apple_healthkit_export_xml(self):
        """
        Load the Apple HealthKit export XML file into memory

        Note
        ----
            [2024-09-07] 
            The XML object may need to be deleted after processing to free up memory
            Total memory usage of the whole AppleHealthKit object is (1335.04 MB)
            Given that Apple HealthKit export XML object size: 11.81 MB
            I am not worried about deleting the XML object

        Returns
        -------
            apple_health_export_xml_root (xml.etree.ElementTree.Element): The root of the Apple HealthKit export XML
        """
        apple_health_export_xml_file = f'{self.apple_health_export_folder}/export.xml'

        logger.info(f'Loading Apple HealthKit export XML from {apple_health_export_xml_file}...')

        ts = time.time()
        with open(apple_health_export_xml_file, 'r') as f:
            xml_string = f.read()

            start_strip = re.search('<!DOCTYPE', xml_string).span()[0]
            end_strip = re.search(']>', xml_string).span()[1]
            xml_string = xml_string[:start_strip] + xml_string[end_strip:]

            xml_string = xml_string.replace("\x0b", "")


        apple_health_export_xml_root = ET.fromstring(xml_string)

        apple_health_export_xml_root_size_mb = sys.getsizeof(apple_health_export_xml_root) / 1024 / 1024
        self.memory_usage_mb += apple_health_export_xml_root_size_mb

        logger.debug(f'Loaded Apple HealthKit export XML from {apple_health_export_xml_file} in {time.time() - ts:.2f} seconds')
        logger.debug(f'Apple HealthKit export XML object size: {apple_health_export_xml_root_size_mb:.2f} MB')
        return apple_health_export_xml_root
    

    def _get_metadata(self):
        """
        Get the metadata from the Apple HealthKit export XML

        Returns
        -------
            metadata (dict): A dictionary of metadata from the Apple HealthKit export XML
                {'export_date': '2024-08-11 21:34:30 -0700'}
        """
        ts = time.time()
        logger.debug('Getting metadata from Apple HealthKit export XML...')

        metadata = {}
        
        export_date_xml = self.apple_health_export_xml_root.find('.//ExportDate')
        metadata['export_date'] = pd.to_datetime(export_date_xml.attrib['value'])
        logger.debug(f'Apple HealthKit export date: {metadata["export_date"]}')

        metadata_size_mb = sys.getsizeof(metadata) / 1024 / 1024
        self.memory_usage_mb += metadata_size_mb

        logger.debug(f'Got metadata from Apple HealthKit export XML in {time.time() - ts:.2f} seconds')
        return metadata


    def _get_characteristics(self):
        """
        Get the characteristics from the Apple HealthKit export XML

        Returns
        -------
            characteristics (dict): A dictionary of characteristics from the Apple HealthKit export XML
                Given HKCharacteristicTypeIdentifierBiologicalSex
                BiologicalSex = characteristics['BiologicalSex']
        """
        ts = time.time()
        logger.debug('Getting characteristics from Apple HealthKit export XML...')

        characteristics_xml = self.apple_health_export_xml_root.find('.//Me')
        characteristics = {}
        for ahk_characteristic_id in characteristics_xml.attrib.keys():
            characteristic_type = ahk_characteristic_id.replace('HKCharacteristicTypeIdentifier', '')
            characteristics[characteristic_type] = characteristics_xml.attrib[ahk_characteristic_id]

        characteristics['DateOfBirth'] = pd.to_datetime(characteristics['DateOfBirth'])

        characteristics_size_mb = sys.getsizeof(characteristics) / 1024 / 1024
        self.memory_usage_mb += characteristics_size_mb    

        logger.debug(f'Found {len(characteristics):,} characteristics')
        logger.debug(f'Got characteristics from Apple HealthKit export XML in {time.time() - ts:.2f} seconds')
        return characteristics


    def _build_AHK_quantity_tables(self):
        """
        Build the quantity tables from the Apple HealthKit export XML

        Returns
        -------
            quantities (dict): A dictionary of DataFrames, where the key is the quantity type and the value is the DataFrame
                Given HKQuantityTypeIdentifierBodyMass, HKDataTypeSleepDurationGoal, and HKCategoryTypeIdentifierSleepAnalysis
                body_mass_df = quantities['BodyMass']
                sleep_duration_goal_df = quantities['SleepDurationGoal']
                sleep_analysis_df = quantities['SleepAnalysis']
        """
        ts = time.time()
        logger.debug('Building quantity tables from Apple HealthKit export XML...')

        quantity_records = self.apple_health_export_xml_root.findall('.//Record')
        logger.debug(f'Found {len(quantity_records):,} records')

        quantities = {}
        for record in quantity_records:
            record_type = record.attrib['type']
            record_type = record_type.replace('HKQuantityTypeIdentifier', '')
            record_type = record_type.replace('HKCategoryTypeIdentifier', '')
            record_type = record_type.replace('HKDataType', '')

            record_dict = {}
            for key in record.attrib.keys():
                record_dict[key] = record.attrib[key]

            if record_type not in quantities:
                quantities[record_type] = []
                
            quantities[record_type].append(record_dict)

        logger.debug(f'Found {len(quantities):,} unique quantity types')

        route_total_memory_usage_mb = 0
        for record_type in quantities:
            quantities[record_type] = pd.DataFrame(quantities[record_type])

            date_columns = [col for col in quantities[record_type].columns if 'date' in col.lower()]
            for date_column in date_columns:
                quantities[record_type][date_column] = pd.to_datetime(quantities[record_type][date_column])

            try:
                quantities[record_type]['value'] = pd.to_numeric(quantities[record_type]['value'])
            except:
                pass
                                                                                
            num_rows, num_columns = quantities[record_type].shape
            memory_usage_mb = quantities[record_type].memory_usage(deep=True).sum() / 1024 / 1024
            logger.debug(f'{record_type} {num_rows:,} x {num_columns:,} ({memory_usage_mb:.2f} MB)')

            route_total_memory_usage_mb += memory_usage_mb

        self.memory_usage_mb += route_total_memory_usage_mb

        logger.debug(f'Total memory usage of all quantity tables: {route_total_memory_usage_mb:.2f} MB')
        logger.debug(f'Built {len(quantities):,} quantity tables in {time.time() - ts:.2f} seconds')
        return quantities
    

    def _build_AHK_workout_tables(self):
        """
        Build the workout tables from the Apple HealthKit export XML

        Returns
        -------
            workouts (dict): A dictionary of DataFrames, where the key is the workout type and the value is the DataFrame
                Given HKWorkoutActivityTypeWalking
                walking_df = workouts['Walking']
        """
    
        ts = time.time()
        logger.debug('Building workout tables from Apple HealthKit export XML...')

        workout_records = self.apple_health_export_xml_root.findall('.//Workout')
        logger.debug(f'Found {len(workout_records):,} workouts')

        workouts = {}
        for workout in workout_records:
            workout_type = workout.attrib['workoutActivityType']
            workout_type = workout_type.replace('HKWorkoutActivityType', '')

            workout_dict = {}
            for key in workout.attrib.keys():
                workout_dict[key] = workout.attrib[key]

            workout_metadata = workout.findall('.//MetadataEntry')
            for metadata_entry in workout_metadata:
                workout_dict[metadata_entry.attrib['key']] = metadata_entry.attrib['value']

            for child in workout.findall('.//WorkoutActivity'):
                workout.remove(child)

            workout_statistics = workout.findall('.//WorkoutStatistics')
            for workout_statistic in workout_statistics:
                ws_type = workout_statistic.attrib['type']
                ws_type = ws_type.replace('HKQuantityTypeIdentifier', '')
                for key in workout_statistic.attrib.keys():
                    if key not in ['type', 'startDate', 'endDate']:
                        workout_dict[f'{ws_type}_{key}'] = workout_statistic.attrib[key]

            workout_route = workout.find('.//WorkoutRoute')
            if workout_route is not None:
                file_reference = workout_route.find('.//FileReference').attrib['path']
                workout_dict['route_file_reference'] = file_reference

            if workout_type not in workouts:
                workouts[workout_type] = []
            workouts[workout_type].append(workout_dict)

        logger.debug(f'Found {len(workouts):,} unique workout types')

        workout_total_memory_usage_mb = 0
        for workout_type in workouts:
            workouts[workout_type] = pd.DataFrame(workouts[workout_type])

            date_columns = [col for col in workouts[workout_type].columns if 'date' in col.lower()]
            for date_column in date_columns:
                workouts[workout_type][date_column] = pd.to_datetime(workouts[workout_type][date_column])

            num_rows, num_columns = workouts[workout_type].shape
            memory_usage_mb = workouts[workout_type].memory_usage(deep=True).sum() / 1024 / 1024
            logger.debug(f'{workout_type} {num_rows:,} x {num_columns:,} ({memory_usage_mb:.2f} MB)')

            workout_total_memory_usage_mb += memory_usage_mb

        self.memory_usage_mb += workout_total_memory_usage_mb
            
        logger.debug(f'Total memory usage of all workout tables: {workout_total_memory_usage_mb:.2f} MB')
        logger.debug(f'Built {len(workouts):,} workout tables in {time.time() - ts:.2f} seconds')
        return workouts
    

    def _build_AHK_route_tables(self):
        """
        Build the route tables from the Apple HealthKit export XML

        Returns
        -------
            routes (pandas.DataFrame): DataFrame containing route data from the Apple HealthKit export XML
                Columns: route_id, lat, lon, ele, time, speed, course, hAcc, vAcc
        """

        ts = time.time()
        logger.debug('Building route table from Apple HealthKit export XML...')

        route_folder = f'{self.apple_health_export_folder}/workout-routes/'
        route_files = glob.glob(f'{route_folder}/*.gpx')
        logger.debug(f'Found {len(route_files):,} route files in {route_folder}')
        
        trkpt_list = []
        for route_file in route_files:
            route_tree = ET.parse(route_file)
            route_root = route_tree.getroot()

            route_id = route_file.split('\\')[-1].replace('.gpx', '')
            trkpts = route_root.findall('.//ahk-workout-route:trkpt', self.xml_namespaces)

            for trkpt in trkpts:
                lat = trkpt.attrib['lat']
                lon = trkpt.attrib['lon']
                
                ele = trkpt.find('.//ahk-workout-route:ele', self.xml_namespaces).text
                trkpt_time = trkpt.find('.//ahk-workout-route:time', self.xml_namespaces).text

                extensions = trkpt.find('.//ahk-workout-route:extensions', self.xml_namespaces)
                speed = extensions.find('.//ahk-workout-route:speed', self.xml_namespaces).text
                course = extensions.find('.//ahk-workout-route:course', self.xml_namespaces).text
                hAcc = extensions.find('.//ahk-workout-route:hAcc', self.xml_namespaces).text
                vAcc = extensions.find('.//ahk-workout-route:vAcc', self.xml_namespaces).text

                trkpt_list.append({
                    'route_id': route_id,
                    'lat': lat,
                    'lon': lon,
                    'ele': ele,
                    'time': trkpt_time,
                    'speed': speed,
                    'course': course,
                    'hAcc': hAcc,
                    'vAcc': vAcc
                })

            logger.debug(f'Processed {route_id} with {len(trkpts):,} track points')

        routes = pd.DataFrame(trkpt_list)

        date_columns = [col for col in routes.columns if 'time' in col.lower()]
        for date_column in date_columns:
            routes[date_column] = pd.to_datetime(routes[date_column])

        value_columns = ['lat', 'lon', 'ele', 'speed', 'course', 'hAcc', 'vAcc']
        for value_column in value_columns:
            try:
                routes[value_column] = pd.to_numeric(routes[value_column])
            except:
                pass

        num_rows, num_columns = routes.shape
        route_memory_usage_mb = routes.memory_usage(deep=True).sum() / 1024 / 1024

        self.memory_usage_mb += route_memory_usage_mb

        logger.debug(f'Processed {len(route_files):,} route files: {num_rows:,} x {num_columns:,} ({route_memory_usage_mb:.2f} MB)')
        logger.debug(f'Built route table in {time.time() - ts:.2f} seconds')
        return routes

def build_apple_health_kit(apple_health_export_folder, pickle_file=None):
    """
    Build an AppleHealthKit object from the Apple HealthKit export data.

    Parameters
    ----------
    apple_health_export_folder : str
        The folder containing the Apple HealthKit export data.

    Returns
    -------
    apple_health_kit : AppleHealthKit
        An AppleHealthKit object containing the parsed Apple HealthKit export data.

    """
    apple_health_kit = AppleHealthKit(apple_health_export_folder)
    if pickle_file:
        with open(pickle_file, 'wb') as f:
            pickle.dump(apple_health_kit, f)
    return apple_health_kit

def load_apple_health_kit(apple_health_kit_pkl_file):
    """
    Load an AppleHealthKit object from a pickle file.

    Parameters
    ----------
    apple_health_kit_pkl_file : str
        The path to the pickle file containing the AppleHealthKit object.

    Returns
    -------
    apple_health_kit : AppleHealthKit
        An AppleHealthKit object loaded from the pickle file.
    """
    ts = time.time()
    with open(apple_health_kit_pkl_file, 'rb') as f:
        apple_health_kit = pickle.load(f)
    logging.info(f'Loaded AppleHealthKit in {time.time() - ts:.2f} seconds')
    return apple_health_kit
