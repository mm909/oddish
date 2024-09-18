
import os
import time
import logging
import webbrowser
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

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
        tooltip='label',
        style_kwds={
            "style_function": style_function
        },
    ).save(out_file)

    if open_browser:
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        full_path = os.path.abspath(out_file)
        webbrowser.get(chrome_path).open(full_path)