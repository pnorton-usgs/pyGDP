from __future__ import (absolute_import, division, print_function)

from ._execute_request import _executeRequest, dodsReplace
from ._get_geotype import _getFeatureCollectionGeoType

from owslib.util import log


def submitFeatureWeightedGridStatistics(geoType, dataSetURI, varID, startTime, endTime, attribute, value,
                                        gmlIDs, verbose, coverage, delim, stat, grpby, timeStep, summAttr,
                                        weighted, wfs_url, outputfname, sleepSecs, async=False):
    """
    Makes a featureWeightedGridStatistics algorithm call. 
    The web service interface implemented is summarized here: 
    https://my.usgs.gov/confluence/display/GeoDataPortal/Generating+Area+Weighted+Statistics+Of+A+Gridded+Dataset+For+A+Set+Of+Vector+Polygon+Features
    
    Note that varID and stat can be a list of strings.
    
    """
    # test for dods:
    dataSetURI = dodsReplace(dataSetURI)

    log.info('Generating feature collection.')

    featureCollection = _getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, wfs_url)

    if featureCollection is None:
        return

    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureWeightedGridStatisticsAlgorithm'
    if not weighted:
        processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureGridStatisticsAlgorithm'

    solo_inputs = [("FEATURE_ATTRIBUTE_NAME", attribute),
                   ("DATASET_URI", dataSetURI),
                   ("TIME_START", startTime),
                   ("TIME_END", endTime),
                   ("REQUIRE_FULL_COVERAGE", str(coverage).lower()),
                   ("DELIMITER", delim),
                   ("GROUP_BY", grpby),
                   ("SUMMARIZE_TIMESTEP", str(timeStep).lower()),
                   ("SUMMARIZE_FEATURE_ATTRIBUTE", str(summAttr).lower()),
                   ("FEATURE_COLLECTION", featureCollection)]

    if isinstance(stat, list):
        num_stats = len(stat)
        if num_stats > 7:
            raise Exception('Too many statistics were submitted.')
    else:
        num_stats = 1

    if isinstance(varID, list):
        num_varids = len(varID)
    else:
        num_varids = 1

    inputs = [('', '')] * (len(solo_inputs) + num_varids + num_stats)

    count = 0
    rm_cnt = 0

    for solo_input in solo_inputs:
        if solo_input[1] is not None:
            inputs[count] = solo_input
            count += 1
        else:
            rm_cnt += 1

    del inputs[count:count + rm_cnt]

    if num_stats > 1:
        for stat_in in stat:
            if stat_in not in ["MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"]:
                raise Exception('The statistic {} is not in the allowed list: "MEAN", "MINIMUM", "MAXIMUM", ' +
                                '"VARIANCE", "STD_DEV", "SUM", "COUNT"'.format(stat_in))
            inputs[count] = ("STATISTICS", stat_in)
            count += 1
    elif num_stats == 1:
        if stat not in ["MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"]:
            raise Exception('The statistic {} is not in the allowed list: "MEAN", "MINIMUM", "MAXIMUM", ' +
                            '"VARIANCE", "STD_DEV", "SUM", "COUNT"'.format(stat))
        inputs[count] = ("STATISTICS", stat)
        count += 1

    if num_varids > 1:
        for var in varID:
            inputs[count] = ("DATASET_ID", var)
            count += 1
    elif num_varids == 1:
        inputs[count] = ("DATASET_ID", varID)

    output = "OUTPUT"

    return _executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs, async=async)
