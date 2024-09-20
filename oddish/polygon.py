
import os
import glob
import time
import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

import oddish

logger = logging.getLogger(__name__)


def load_polygon(path):
    """
    Load a polygon from a CSV file. 
    The CSV file should have two columns (longitude, latitude)
    First and last row should be the same to close the polygon
    https://www.keene.edu/campus/maps/tool/

    Parameters
    ----------
    path : str
        The path to the CSV file.

    Returns
    -------
    Polygon
        The polygon defined by the coordinates in the CSV file.
    """
    ts = time.time()
    logger.debug(f'Loading polygon from {path}.')
    geo_polygon = pd.read_csv(path, header=None)
    coordinates = [(x[0], x[1]) for x in geo_polygon.values]

    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])

    polygon = Polygon(coordinates)
    logger.debug(f'Polygon with {len(coordinates)} vertices loaded in {time.time() - ts:.2f} seconds.')
    return polygon


def load_polygons(paths):
    """
    Load multiple polygons from a list of CSV files.

    Parameters
    ----------
    paths : list
        The list of paths to the CSV files.

    Returns
    -------
    list
        The list of polygons defined by the coordinates in the CSV files.
    """
    polygons = [load_polygon(path) for path in paths]
    return polygons


def show_polygon(polygon, out_file=None, open_browser=True):
    """
    Convert a polygon to a GeoPandas DataFrame and plot it.
    https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.explore.html

    Parameters
    ----------
    polygon : Polygon
        The polygon to plot.
    out_file : str, optional
        The path to save the plot, by default None
    open_browser : bool, optional
        Open the plot in the browser, by default True
    """

    polygon_df = pd.DataFrame([polygon], columns=['polygon'])
    gdf = gpd.GeoDataFrame(
        polygon_df, geometry='polygon', crs="EPSG:4326"
    )

    if out_file is None:
        out_file = f'../data/explore/polygon.html'
    folders = os.path.dirname(out_file)
    os.makedirs(folders, exist_ok=True)


    map_html = gdf.explore().save(out_file)

    if open_browser:
        oddish.open_browser(out_file)


def show_polygons(polygons, out_file=None, open_browser=True):
    """
    Convert a list of polygons to a GeoPandas DataFrame and plot them.
    https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.explore.html

    Parameters
    ----------
    polygons : list
        The list of polygons to plot.
    out_file : str, optional
        The path to save the plot, by default None
    open_browser : bool, optional
        Open the plot in the browser, by default True
    """

    polygon_df = pd.DataFrame(polygons)
    gdf = gpd.GeoDataFrame(
        polygon_df, geometry='polygon', crs="EPSG:4326"
    )

    if out_file is None:
        out_file = f'../data/explore/polygons.html'
    folders = os.path.dirname(out_file)
    os.makedirs(folders, exist_ok=True)

    def style_function(feature):
        return {
            'fill': feature['properties']['fill'],
            'fillColor': feature['properties']['color'],
            'fillOpacity': feature['properties']['opacity'],
        }

    map_html = gdf.explore(
        tooltip=['name'],
        style_kwds={
            "style_function": style_function
        },
    ).save(out_file)

    if open_browser:
        oddish.open_browser(out_file)


def union_polygons(polygons):
    """
    Combine multiple polygons into a single polygon.

    Parameters
    ----------
    polygons : list
        The list of polygons to combine.

    Returns
    -------
    Polygon
        The polygon defined by the union of the input polygons.
    """
    ts = time.time()
    logger.debug(f'Combining {len(polygons)} polygons.')
    combined_polygon = Polygon()
    for polygon in polygons:
        combined_polygon = combined_polygon.union(polygon)
    logger.debug(f'{len(polygons)} polygons combined in {time.time() - ts:.2f} seconds.')
    return combined_polygon


def build_polygon_hierarchy(folder):
    polygon_files = glob.glob(f'{folder}/*.csv')

    polygons = []
    for polygon_file in polygon_files:
        polygon = load_polygon(polygon_file)
        names = os.path.basename(polygon_file).split('.')[0].split('-')
        formatted_names = [name.replace('_', ' ').title() for name in names]
        polygons.append({
            'city': formatted_names[0],
            'region': formatted_names[1],
            'section': formatted_names[2],
            'name': ' '.join(formatted_names),
            'polygon': polygon,
        })
    polygon_df = pd.DataFrame(polygons)

    city_region_polygons = []
    for city in polygon_df['city'].unique():
        city_df = polygon_df[polygon_df['city'] == city]
        city_polygon = union_polygons(city_df['polygon'])
        city_region_polygons.append({
            'city': city,
            'region': 'All',
            'section': 'All',
            'name': city,
            'polygon': city_polygon,
        })
    city_region_df = pd.DataFrame(city_region_polygons)

    region_polygons = []
    for city in polygon_df['city'].unique():
        for region in polygon_df[polygon_df['city'] == city]['region'].unique():
            region_df = polygon_df[(polygon_df['city'] == city) & (polygon_df['region'] == region)]
            region_polygon = union_polygons(region_df['polygon'])
            region_polygons.append({
                'city': city,
                'region': region,
                'section': 'All',
                'name': f"{city} - {region}",
                'polygon': region_polygon,
            })
    region_df = pd.DataFrame(region_polygons)

    combined_df = pd.concat([polygon_df, city_region_df, region_df], ignore_index=True)
    combined_df.set_index(['city', 'region', 'section'], inplace=True)
    return combined_df

def print_polygon_for_keene(polygon):
    for idx, point in enumerate(polygon.exterior.coords):
        print(f'{point[0]},{point[1]}')
    return