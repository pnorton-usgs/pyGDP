from __future__ import (absolute_import, division, print_function)

from . import _execute_request
from . import _get_geotype


def submitFeatureCategoricalGridCoverage(geoType, dataSetURI, varID, attribute='the_geom',
                                         value=None, gmlIDs=None, verbose=False, coverage=True,
                                         delim='COMMA', wfs_url=None, outputfname=None, sleepSecs=10, async=False):
    """
    Makes a featureCategoricalGridCoverage algorithm call.
    """

    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, wfs_url)
    if featureCollection is None:
        return

    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCategoricalGridCoverageAlgorithm'
    inputs = [("FEATURE_ATTRIBUTE_NAME", attribute),
              ("DATASET_URI", dataSetURI),
              ("DATASET_ID", varID),
              ("DELIMITER", delim),
              ("REQUIRE_FULL_COVERAGE", str(coverage).lower()),
              ("FEATURE_COLLECTION", featureCollection)]
    output = "OUTPUT"
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs, async=async)


def submitFeatureCoverageWCSIntersection(geoType, dataSetURI, varID, attribute='the_geom',
                                         value=None, gmlIDs=None, verbose=False, coverage=True,
                                         wfs_url=None, outputfname=None, sleepSecs=10, async=False):
    """
    Makes a featureCoverageWCSIntersection algorithm call.
    """

    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, wfs_url)
    if featureCollection is None:
        return

    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageIntersectionAlgorithm'
    inputs = [("DATASET_URI", dataSetURI),
              ("DATASET_ID", varID),
              ("REQUIRE_FULL_COVERAGE", str(coverage).lower()),
              ("FEATURE_COLLECTION", featureCollection)]
    output = "OUTPUT"
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs, async=async)


def submitFeatureCoverageOPenDAP(geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None,
                                 gmlIDs=None, verbose=False, coverage=True, wfs_url=None, outputfname=None,
                                 sleepSecs=10, async=False):
    """
    Makes a featureCoverageOPenDAP algorithm call.
    """

    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, wfs_url)
    if featureCollection is None:
        return

    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageOPeNDAPIntersectionAlgorithm'
    inputs = [("DATASET_URI", dataSetURI),
              ("DATASET_ID", varID),
              ("TIME_START", startTime),
              ("TIME_END", endTime),
              ("REQUIRE_FULL_COVERAGE", str(coverage).lower()),

              ("FEATURE_COLLECTION", featureCollection)]
    output = "OUTPUT"
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs, async=async)
