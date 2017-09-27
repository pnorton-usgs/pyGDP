from __future__ import (absolute_import, division, print_function)

from . import shapefile_id_handle
from owslib.wps import WFSFeatureCollection, WFSQuery, GMLMultiPolygonFeatureCollection

# from . import shapefile_value_handle
# from owslib.wps import monitorExecution, WebProcessingService


def _getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, wfs_url):
    """
    This function returns a featurecollection. It takes a geotype and determines if
    the geotype is a shapfile or polygon.

    If value is set to None, a FeatureCollection with all features will be returned.

    """

    # This is a polygon
    if isinstance(geoType, list):
        return GMLMultiPolygonFeatureCollection([geoType])
    elif isinstance(geoType, str):
        if value is None:
            if gmlIDs is None:
                # Using an empty gmlIDs element results in all features being returned to the constructed WFS query.
                gmlIDs = []
                print('All shapefile attributes will be used.')

        tmp_id = []

        if gmlIDs is None:
            if type(value) == type(tmp_id):
                gmlIDs = []

                for v in value:
                    tuples = shapefile_id_handle.getTuples(geoType, attribute, wfs_url=wfs_url)
                    tmp_id = shapefile_id_handle._getFilterID(tuples, v)
                    gmlIDs = gmlIDs + tmp_id
                print(tmp_id)

                if not tmp_id:
                    raise Exception("Didn't find any features matching given attribute values.")
            else:
                tuples = shapefile_id_handle.getTuples(geoType, attribute, wfs_url=wfs_url)
                gmlIDs = shapefile_id_handle._getFilterID(tuples, value)
                if not gmlIDs:
                    raise Exception("Didn't find any features matching given attribute value.")

        geometry_attribute = 'the_geom'
        if 'arcgis' in wfs_url.lower():
            geometry_attribute = 'Shape'

        query = WFSQuery(geoType, propertyNames=[geometry_attribute, attribute], filters=gmlIDs)

        return WFSFeatureCollection(wfs_url, query)
    else:
        raise Exception('Geotype is not a shapefile or a recognizable polygon.')
