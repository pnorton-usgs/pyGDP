# The functions in this file exist to WFS requests to get the various values that exist for
# shapefiles on the GDP. These include the shapefiles themselves, the attributes of those
# shapefiles, and the values of those attributes.
from __future__ import (absolute_import, division, print_function)

from io import BytesIO
from owslib.wfs import WebFeatureService
from owslib.etree import etree
from .namespaces import GML_NAMESPACE

# 2017-09-19 PAN: currently not used
# from .namespaces import upload_URL, WPS_URL, WPS_Service, CSW_URL  # WFS_URL,
# from .namespaces import WPS_DEFAULT_VERSION, WPS_DEFAULT_SCHEMA_LOCATION, GML_SCHEMA_LOCATION
# from .namespaces import WPS_DEFAULT_NAMESPACE, CSW_NAMESPACE, WPS_DEFAULT_NAMESPACE
# from .namespaces import WFS_NAMESPACE, OGC_NAMESPACE
# from .namespaces import namespaces


def getShapefiles(wfs_url):
    """
    Returns a list of available files currently on geoserver.
    """
    wfs = WebFeatureService(wfs_url)
    shapefiles = wfs.contents.keys()
    return shapefiles


def getAttributes(shapefile, wfs_url):
    """
    Given a valid shapefile(WFS Featuretype as returned by getShapefiles), this function will
    make a request for one feature from the featureType and parse out the attributes that come from
    a namespace not associated with the normal GML schema. There may be a better way to determine
    which are shapefile dbf attributes, but this should work pretty well.
    """
    wfs = WebFeatureService(wfs_url, version='1.1.0')
    feature = wfs.getfeature(typename=shapefile, maxfeatures=1, propertyname=None)
    content = BytesIO(feature.read().encode())
    gml = etree.parse(content)
    gml_root = gml.getroot()
    name_spaces = gml_root.nsmap

    attributes = []

    for namespace in name_spaces.values():
        if namespace not in ['http://www.opengis.net/wfs',
                             'http://www.w3.org/2001/XMLSchema-instance',
                             'http://www.w3.org/1999/xlink',
                             'http://www.opengis.net/gml',
                             'http://www.opengis.net/ogc',
                             'http://www.opengis.net/ows']:
            custom_namespace = namespace

            for element in gml.iter('{' + custom_namespace + '}*'):
                if etree.QName(element).localname not in ['the_geom', 'Shape', shapefile.split(':')[1]]:
                    attributes.append(etree.QName(element).localname)
    return attributes


def getValues(shapefile, attribute, getTuples, limitFeatures, wfs_url):
    """
    Similar to get attributes, given a shapefile and a valid attribute this function
    will make a call to the Web Feature Services returning a list of values associated
    with the shapefile and attribute.

    If getTuples = True, will also return the tuples of [feature:id]  along with values [feature]
    """

    wfs = WebFeatureService(wfs_url, version='1.1.0')

    feature = wfs.getfeature(typename=shapefile, maxfeatures=limitFeatures, propertyname=[attribute])
    content = BytesIO(feature.read().encode())
    gml = etree.parse(content)

    values = []

    for el in gml.iter():
        if attribute in el.tag:
            if el.text not in values:
                values.append(el.text)

    if getTuples == 'true' or getTuples == 'only':
        tuples = []
        att = False

        # If features are encoded as a list of featureMember elements.
        gmlid_found = False
        for featureMember in gml.iter('{' + GML_NAMESPACE + '}featureMember'):
            for el in featureMember.iter():
                if el.get('{' + GML_NAMESPACE + '}id'):
                    gmlid = el.get('{' + GML_NAMESPACE + '}id')
                    att = True
                    gmlid_found = True
                if attribute in el.tag and att is True:
                    value = el.text
                    tuples.append((value, gmlid))
                    att = False
            if not gmlid_found:
                raise Exception('No gml:id found in source feature service. This form of GML is not supported.')

        # If features are encoded as a featureMembers element.
        for featureMember in gml.iter('{' + GML_NAMESPACE + '}featureMembers'):
            for el in featureMember.iter():
                gmlid = el.get('{' + GML_NAMESPACE + '}id')
                for feat in el.getchildren():
                    if attribute in feat.tag:
                        value = feat.text
                        tuples.append((value, gmlid))

    if getTuples == 'true':
        return sorted(values), sorted(tuples)
    elif getTuples == 'only':
        return sorted(tuples)
    else:
        return sorted(values)
