from lettuce import *
from nose.tools import assert_equal
import os
import pyGDP

@step(r'I have a test shapefile and all its associated components')
def point_to_file(step):
    world.shapefile_name = 'CIDA_TEST_.shp'
    world.shapefile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), world.shapefile_name)
    
@step(r'I run the shapeToZip function')
def shape_to_zip(step):
    test_pyGDP = create_web_processing_object()
    world.zip_name = test_pyGDP.shapeToZip(world.shapefile_path)
        
def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'And I upload the shapefile')
def upload_shp(step):
    test_pyGDP = create_web_processing_object()
    print world.zip_name
    world.uploadName = test_pyGDP.uploadShapeFile(world.zip_name)

@step(r'I get back the shapefile name that I expect')
def check_layer_name(step):
    assert_equal(world.uploadName, 'upload:CIDA_TEST_')
    
def clean_up():
    os.remove(world.zip_name)
