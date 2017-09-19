from __future__ import (absolute_import, division, print_function)

import base64
import os
from owslib.etree import etree
from owslib.wps import WebProcessingService, monitorExecution
from .GDP_XML_Generator import gdpXMLGenerator
from .namespaces import upload_URL, WPS_Service


# This file contains a function to encode a zipped shapefile (probably from
# the shapeToZip function) then include that function
def uploadShapeFile(filePath):
    """
    Given a file, this function encodes the file and uploads it onto geoserver.
    """

    # encodes the file, opens it, reads it, and closes it
    # returns a filename in form of: filename_copy.zip
    filePath = _encodeZipFolder(filePath)
    if filePath is None:
        return

    filehandle = open(filePath, 'r')
    filedata = filehandle.read()
    filehandle.close()
    os.remove(filePath)  # deletes the encoded file

    # this if for naming the file on geoServer
    filename = filePath.split("/")
    # gets rid of filepath, keeps only filename eg: file.zip
    filename = filename[len(filename) - 1]
    filename = filename.replace("_copy.zip", "")

    xml_gen = gdpXMLGenerator()
    root = xml_gen.getUploadXMLtree(filename, upload_URL, filedata)

    # now we have a complete XML upload request
    upload_request = etree.tostring(root)
    post = WebProcessingService(WPS_Service)
    execution = post.execute(None, [], request=upload_request)
    monitorExecution(execution)
    return "upload:" + filename


def _encodeZipFolder(filename):
    """
    This function will encode a zipfile and return the filename.
    """
    # check extension
    if not filename.endswith('.zip'):
        raise Exception('Wrong filetype.')

    # encode the file
    with open(filename, 'rb') as fin:
        bytes_read = fin.read()
        encode = base64.b64encode(bytes_read)

    # renames the file and saves it onto local drive
    filename = filename.replace('.zip', '_copy.zip')

    fout = open(filename, 'wb')
    fout.write(encode)
    fout.close()
    return filename
