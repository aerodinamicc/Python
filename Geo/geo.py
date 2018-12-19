import fiona
from osgeo import ogr
import geopandas as gpd
import os
import pprint

os.chdir('G:/Python/Geo')
shapefile = fiona.open("polys.shp")
pprint.pprint(shapefile.schema['geometry'])
pprint.pprint(shapefile.schema['properties'])
pprint.pprint(shapefile.keys()) #dictionary keys aka column names from attribute table
shape = 1
for feat in shapefile:
    if feat['properties']['plot_id'] == 1:
        shape = feat

geom = shapefile(feat)


shape_geopanda = gpd.read_file("polys.shp")

file = ogr.Open("polys.shp")
shape_ogr = file.GetLayer(0)
#shape_ogr.SetSpatialFilterRect(-102, 26, -94, 36)

#That is how to intersect individual shapes while reading in vectors with fiona and processing with shapely
#Shapely by itself does not read or write files
#nevertheless it could take in json files
# from shapely import shape, mapping
# import fiona
# # schema of the new shapefile
# schema =  {'geometry': 'Polygon','properties': {'area': 'float:13.3','id_populat': 'int','id_crime': 'int'}}
# # creation of the new shapefile with the intersection
# with fiona.open('intersection.shp', 'w',driver='ESRI Shapefile', schema=schema) as output:
#     for crim in fiona.open('crime_stat.shp'):
#         for popu in fiona.open('population.shp'):
#            if shape(crim['geometry']).intersects(shape(popu['geometry'])):     
#               area = shape(crim['geometry']).intersection(shape(popu['geometry'])).area
#               prop = {'area': area, 'id_populat' : popu['id'],'id_crime': crim['id']} 
#               output.write({'geometry':mapping(shape(crim['geometry']).intersection(shape(popu['geometry']))),'properties': prop})
print('a')