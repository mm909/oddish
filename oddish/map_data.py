
import os
import osmnx as ox

import oddish

walkable_streets_filter = (
    '["highway"]["area"!~"yes"]["access"!~"private"]'
    '["highway"!~"abandoned|bridleway|bus_guideway|'
    'motor|unclassified|construction|corridor|cycleway|'
    'elevator|escalator|footway|no|path|pedestrian|'
    'planned|platform|proposed|raceway|razed|service|'
    'steps|track"]'
    '["name"]["motor_vehicle"!~"no"]["motorcar"!~"no"]'
    '["foot"!~"no"]["service"!~"private"]'
)


def view_section(section, out_file=None, open_browser=True):
    if out_file is None:
        out_folder = '../data/explore/'
        os.makedirs(f'{out_folder}/', exist_ok=True)
        out_file = f'{out_folder}/{section}.html'
        
    polygon_file = f'../data/polygons/{section}.csv'
    polygon = oddish.load_polygon(polygon_file)
    G = ox.graph_from_polygon(polygon, custom_filter=oddish.walkable_streets_filter)
    view_osmnx_data(G, out_file, open_browser)


def view_osmnx_data(g, out_file=None, open_browser=True):

    if out_file is None:
        out_folder = '../data/explore/'
        os.makedirs(out_folder, exist_ok=True)
        out_file = f'{out_folder}/temp.html'

    nodes, edges = ox.graph_to_gdfs(g)
    m = edges.explore()
    nodes.explore(m=m, color='black').save(out_file)

    if open_browser:
        oddish.open_browser(out_file)

def get_gates_from_polygon(polygon):
    tags = {"barrier": ["gate"]}
    features = ox.features_from_polygon(polygon, tags)
    features.reset_index(inplace=True)
    return features

def explore_wrapper(gdf, out_file=None, open_browser=False, kwargs={}):
    if out_file is None:
        out_folder = '../data/explore/'
        os.makedirs(out_folder, exist_ok=True)
        out_file = f'{out_folder}/temp.html'
    m = gdf.explore(**kwargs)
    m.save(out_file)
    if open_browser:
        oddish.open_browser(out_file)
    return m

# Get gates
# Graph gates/other things on the map