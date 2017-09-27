from __future__ import (absolute_import, division, print_function)

from owslib.etree import etree
import owslib.util as util

# Import the appropriate namespace variables.
from .namespaces import WPS_DEFAULT_VERSION, WPS_DEFAULT_SCHEMA_LOCATION
from .namespaces import namespaces


class gdpXMLGenerator():
    """
    This class is responsible for generating the upload XML tree template
    as well as the xml post request tree template.
    This class serves no other functions.
    """

    def __init__(self):
        pass

    def _init_(self):
        pass

    def _subElement(self, root, elementName):
        return etree.SubElement(root, util.nspath_eval(elementName, namespaces))

    def getUploadXMLtree(self, filename, wfs_url, filedata):
        # generate the POST XML request
        # <wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0"
        #             xmlns:ows="http://www.opengis.net/ows/1.1" 
        #             xmlns:xlink="http://www.w3.org/1999/xlink" 
        #             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        #             service="WPS" 
        #             version="1.0.0" 
        #             xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">       
        root = etree.Element(util.nspath_eval('wps:Execute', namespaces), nsmap=namespaces)
        root.set('service', 'WPS')
        root.set('version', WPS_DEFAULT_VERSION)
        root.set(util.nspath_eval('xsi:schemaLocation', namespaces),
                 '%s %s' % (namespaces['wps'], WPS_DEFAULT_SCHEMA_LOCATION))

        # <ows:Identifier>gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids</ows:Identifier>
        identifier_element = self._subElement(root, 'ows:Identifier')
        identifier_element.text = 'gov.usgs.cida.gdp.wps.algorithm.filemanagement.ReceiveFiles'

        # <wps:DataInputs>
        #    <wps:Input>
        #        <ows:Identifier>filename</ows:Identifier>
        #        <wps:Data>
        #            <wps:LiteralData>FILENAME</wps:LiteralData>
        #        </wps:Data>
        #    <wps:Input>
        #        <wps:Identifier>wfs-url</wps:Identifier>
        #            <wps:Data>
        #                <wps:LiteralData>false</wps:LiteralData>
        #            </wps:Data>
        # </wps:DataInputs>
        data_inputs_element = self._subElement(root, 'wps:DataInputs')
        input_elements = self._subElement(data_inputs_element, 'wps:Input')
        identifier_element = self._subElement(input_elements, 'ows:Identifier')
        identifier_element.text = 'filename'

        data_element = self._subElement(input_elements, 'wps:Data')
        literal_element = self._subElement(data_element, 'wps:LiteralData')
        literal_element.text = filename

        input_elements = self._subElement(data_inputs_element, 'wps:Input')
        identifier_element = self._subElement(input_elements, 'ows:Identifier')
        identifier_element.text = 'wfs-url'
        data_element = self._subElement(input_elements, 'wps:Data')
        literal_element = self._subElement(data_element, 'wps:LiteralData')
        literal_element.text = wfs_url

        # adding complex information
        input_elements = self._subElement(data_inputs_element, 'wps:Input')
        identifier_element = self._subElement(input_elements, 'ows:Identifier')
        identifier_element.text = 'file'
        data_element = self._subElement(input_elements, 'wps:Data')
        complex_data_element = etree.SubElement(data_element, util.nspath_eval('wps:ComplexData', namespaces),
                                                attrib={"mimeType": "application/x-zipped-shp",
                                                        "encoding": "Base64"})
        # sets filedata
        complex_data_element.text = filedata

        # <wps:ResponseForm>
        #    <wps:ResponseDocument>
        #        <ows:Output>
        #            <ows:Identifier>result</ows:Identifier>
        #        </ows:Output>
        #    </wps:ResponseDocument>
        # </wps:ResponseForm>
        response_form_element = self._subElement(root, 'wps:ResponseForm')
        response_doc_element = self._subElement(response_form_element, 'wps:ResponseDocument')
        output_element = self._subElement(response_doc_element, 'wps:Output')
        identifier_element = self._subElement(output_element, 'ows:Identifier')
        identifier_element.text = 'result'
        output_element = self._subElement(response_doc_element, 'wps:Output')
        identifier_element = self._subElement(output_element, 'ows:Identifier')
        identifier_element.text = 'wfs-url'
        output_element = self._subElement(response_doc_element, 'wps:Output')
        identifier_element = self._subElement(output_element, 'ows:Identifier')
        identifier_element.text = 'featuretype'

        return root

    def getXMLRequestTree(self, dataSetURI, algorithm, method, varID=None, verbose=False):
        # <wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0"
        #             xmlns:ows="http://www.opengis.net/ows/1.1" 
        #             xmlns:xlink="http://www.w3.org/1999/xlink" 
        #             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        #             service="WPS" 
        #             version="1.0.0" 
        #             xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">       
        root = etree.Element(util.nspath_eval('wps:Execute', namespaces), nsmap=namespaces)
        root.set('service', 'WPS')
        root.set('version', WPS_DEFAULT_VERSION)
        root.set(util.nspath_eval('xsi:schemaLocation', namespaces),
                 '%s %s' % (namespaces['wps'], WPS_DEFAULT_SCHEMA_LOCATION))

        # <ows:Identifier>gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids</ows:Identifier>
        identifier_element = etree.SubElement(root, util.nspath_eval('ows:Identifier', namespaces))
        identifier_element.text = algorithm

        # <wps:DataInputs>
        #    <wps:Input>
        #        <ows:Identifier>catalog-url</ows:Identifier>
        #        <wps:Data>
        #            <wps:LiteralData>'dataSetURI</wps:LiteralData>
        #        </wps:Data>
        #    <wps:Input>
        #        <wps:Identifier>allow-cached-response</wps:Identifier>
        #            <wps:Data>
        #                <wps:LiteralData>false</wps:LiteralData>
        #            </wps:Data>
        # </wps:DataInputs>
        data_inputs_element = etree.SubElement(root, util.nspath_eval('wps:DataInputs', namespaces))
        input_elements = etree.SubElement(data_inputs_element, util.nspath_eval('wps:Input', namespaces))
        identifier_element = etree.SubElement(input_elements, util.nspath_eval('ows:Identifier', namespaces))
        identifier_element.text = 'catalog-url'
        data_element = etree.SubElement(input_elements, util.nspath_eval('wps:Data', namespaces))
        literal_element = etree.SubElement(data_element, util.nspath_eval('wps:LiteralData', namespaces))
        literal_element.text = dataSetURI

        if method == 'getDataSetTime':
            input_elements = etree.SubElement(data_inputs_element, util.nspath_eval('wps:Input', namespaces))
            identifier_element = etree.SubElement(input_elements, util.nspath_eval('ows:Identifier', namespaces))
            identifier_element.text = 'grid'
            data_element = etree.SubElement(input_elements, util.nspath_eval('wps:Data', namespaces))
            literal_element = etree.SubElement(data_element, util.nspath_eval('wps:LiteralData', namespaces))
            literal_element.text = varID

        input_elements = etree.SubElement(data_inputs_element, util.nspath_eval('wps:Input', namespaces))
        identifier_element = etree.SubElement(input_elements, util.nspath_eval('ows:Identifier', namespaces))
        identifier_element.text = 'allow-cached-response'
        data_element = etree.SubElement(input_elements, util.nspath_eval('wps:Data', namespaces))
        literal_element = etree.SubElement(data_element, util.nspath_eval('wps:LiteralData', namespaces))
        literal_element.text = 'false'

        # <wps:ResponseForm storeExecuteResponse=true status=true>
        #    <wps:ResponseDocument>
        #        <ows:Output asReference=true>
        #            <ows:Identifier>result</ows:Identifier>
        #        </ows:Output>
        #    </wps:ResponseDocument>
        # </wps:ResponseForm>
        response_form_element = etree.SubElement(root, util.nspath_eval('wps:ResponseForm', namespaces),
                                                 attrib={'storeExecuteResponse': 'true', 'status': 'true'})
        response_doc_element = etree.SubElement(response_form_element, util.nspath_eval('wps:ResponseDocument',
                                                                                        namespaces))
        output_element = etree.SubElement(response_doc_element, util.nspath_eval('wps:Output', namespaces),
                                          attrib={'asReference': 'false'})
        identifier_element = etree.SubElement(output_element, util.nspath_eval('ows:Identifier', namespaces))
        identifier_element.text = 'result_as_xml'

        return root
