from __future__ import (absolute_import, division, print_function)

import os
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE

# Global URLs for GDP and services


# URLs are read out from the dictionary.
# Here they are prepared to be sent to pyGDP.
def get_URLs(environ_name):
    urls = {'production': {'WFS_URL': 'https://cida.usgs.gov/gdp/geoserver/wfs',
                           'upload_URL': 'https://cida.usgs.gov/gdp/geoserver',
                           'WPS_URL': 'https://cida.usgs.gov/gdp/process/WebProcessingService',
                           'WPS_Service': 'https://cida.usgs.gov/gdp/utility/WebProcessingService',
                           'CSW_URL': 'https://www.sciencebase.gov/catalog/item/54dd2326e4b08de9379b2fb1/csw'
                           },
            'development': {'WFS_URL': 'https://cidasddvasgdp.cr.usgs.gov:8082/gdp/geoserver/wfs',
                            'upload_URL': 'https://cidasddvasgdp.cr.usgs.gov:8082/gdp/geoserver',
                            'WPS_URL': 'https://cidasddvasgdp.cr.usgs.gov:8080/gdp-process-wps/WebProcessingService',
                            'WPS_Service': 'https://cidasddvasgdp.cr.usgs.gov:8080/gdp-utility-wps/WebProcessingService?Service=WPS&Request=GetCapabilities',
                            'CSW_URL': 'https://www.sciencebase.gov/catalog/item/54dd2326e4b08de9379b2fb1/csw'
                            },
            'testing': {'WFS_URL': 'https://cida-test.er.usgs.gov/gdp/geoserver/wfs',
                        'upload_URL': 'https://cida-test.er.usgs.gov/gdp/geoserver',
                        'WPS_URL': 'https://cida-test.er.usgs.gov/gdp/process/WebProcessingService',
                        'WPS_Service': 'https://cida-test.er.usgs.gov/gdp/utility/WebProcessingService',
                        'CSW_URL': 'https://www.sciencebase.gov/catalog/item/54dd2326e4b08de9379b2fb1/csw'
                        },
            'custom': {'WFS_URL': 'your input here',
                       'upload_URL': 'your input here',
                       'WPS_URL': 'your input here',
                       'WPS_Service': 'your input here',
                       'CSW_URL': 'your input here'
                       }
            }

    return urls[environ_name]


urls = get_URLs(environ_name=os.environ.get('PYGDP_TIER', 'production'))

WFS_URL = urls['WFS_URL']
upload_URL = urls['upload_URL']
WPS_URL = urls['WPS_URL']
WPS_Service = urls['WPS_Service']
CSW_URL = urls['CSW_URL']

# These are the schema locations for pyGDP XML validation.
WPS_DEFAULT_VERSION = '1.0.0'
WPS_DEFAULT_SCHEMA_LOCATION = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd'
GML_SCHEMA_LOCATION = "http://schemas.opengis.net/gml/3.1.1/base/feature.xsd"

# These namespaces are subject to change in version number. They will change
# with pyGDP versions here if necessary.
WPS_DEFAULT_NAMESPACE = "http://www.opengis.net/wps/1.0.0"
CSW_NAMESPACE = 'http://www.opengis.net/cat/csw/2.0.2'

WFS_NAMESPACE = 'http://www.opengis.net/wfs'
OGC_NAMESPACE = 'http://www.opengis.net/ogc'
GML_NAMESPACE = 'http://www.opengis.net/gml'

# These are geoserver specific namespaces for different work environments.
# These will probably never change.
DRAW_NAMESPACE = 'gov.usgs.cida.gdp.draw'
SMPL_NAMESPACE = 'gov.usgs.cida.gdp.sample'
UPLD_NAMESPACE = 'gov.usgs.cida.gdp.upload'

# Variables used for internal pyGDP purposes
URL_timeout = 60  # seconds
WPS_attempts = 10  # tries with null response before failing

# Here is a dictionary of all the namespaces used in pyGDP. Expect to see
# both calls to this dictionary and references to the full namespace variable
# depending on the the nature of the function in pyGDP.
namespaces = {None: WPS_DEFAULT_NAMESPACE,
              'wps': WPS_DEFAULT_NAMESPACE,
              'ows': DEFAULT_OWS_NAMESPACE,
              'xlink': XLINK_NAMESPACE,
              'xsi': XSI_NAMESPACE,
              'wfs': WFS_NAMESPACE,
              'ogc': OGC_NAMESPACE,
              'gml': GML_NAMESPACE,
              'sample': SMPL_NAMESPACE,
              'upload': UPLD_NAMESPACE,
              'csw': CSW_NAMESPACE}
