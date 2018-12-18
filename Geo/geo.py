import fiona
from osgeo import ogr
import geopandas as gpd
import os

os.chdir('G:/Python/Geo')
shape = fiona.open("polys.shp")
print(shape.schema['geometry'])
print(shape.schema['properties'])

shape_geopanda = gpd.read_file("polys.shp")

file = ogr.Open("polys.shp")
shape_ogr = file.GetLayer(0)
#shape_ogr.SetSpatialFilterRect(-102, 26, -94, 36)

print('a')