import pyGDP

pyGDP = pyGDP.pyGDPwebProcessing()

shapefile = 'sample:CONUS_states'
attribute = 'STATE'
value = 'Alabama'

dataSetURI = 'https://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer'

dataType = '1'
file_handle = pyGDP.submitFeatureCategoricalGridCoverage(shapefile, dataSetURI, dataType, attribute, value, verbose=True)
