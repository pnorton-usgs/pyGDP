from __future__ import (absolute_import, division, print_function)

from owslib.wps import WebProcessingService
from owslib.etree import etree

from . import _execute_request
from .GDP_XML_Generator import gdpXMLGenerator
from .namespaces import WPS_Service

# import sys
# from io import BytesIO


def _generateRequest(dataSetURI, algorithm, method, varID, verbose):
    """
    Takes a dataset uri, algorithm, method, and datatype. This function will generate a simple XML document
    to make the request specified. (Only works for ListOpendapGrids and GetGridTimeRange).

    Will return a list containing the info requested for (either data types or time range).
    """

    post = WebProcessingService(WPS_Service, verbose=verbose)

    xml_gen = gdpXMLGenerator()
    root = xml_gen.getXMLRequestTree(dataSetURI, algorithm, method, varID, verbose)

    request = etree.tostring(root)

    execution = post.execute(None, [], request=request)

    _execute_request._check_for_execution_errors(execution)

    if method == 'getDataSetTime':
        seekterm = '{xsd/gdptime-1.0.xsd}time'
    elif method == 'getDataType':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}name'
    elif method == 'getDataLongName':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}description'
    elif method == 'getDataUnits':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}unitsstring'

    return _parseXMLNodesForTagText(execution.response, seekterm)


def _parseXMLNodesForTagText(xml, tag):
    """
    Parses through a XML tree for text associated with specified tag.
    Returns a list of the text.
    """

    tag_text = []
    for node in xml.iter():
        if node.tag == tag:
            tag_text.append(node.text)
    return tag_text
