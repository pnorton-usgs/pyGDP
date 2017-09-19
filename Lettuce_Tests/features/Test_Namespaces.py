from __future__ import print_function

import pyGDP

from urlparse import urlparse
import httplib
from lettuce import *


# All the global variables in pyGDP:

@step(r'Given I have all my namespaces defined in pyGDP')
def define_those_namespaces(step):
    world.name_spaces = ['upload_URL', 'WPS_URL', 'WPS_Service', 'CSW_URL',
                         'WPS_DEFAULT_NAMESPACE', 'WPS_DEFAULT_SCHEMA_LOCATION',
                         'WPS_DEFAULT_VERSION', 'WFS_NAMESPACE', 'OGC_NAMESPACE',
                         'GML_NAMESPACE', 'GML_SCHEMA_LOCATION',
                         'DRAW_NAMESPACE', 'SMPL_NAMESPACE', 'UPLD_NAMESPACE', 'CSW_NAMESPACE'
    ]


@step(r'And that each namespace points to a working URL or part of an XML')
def check_populated_namespaces(step):
    for space in world.name_spaces:
        assert (space is not None)


@step(r'When I check the http response from each url')
def check_those_responses(step):
    world.responses = []
    for x in range(len(world.name_spaces)):
        to_evaluate = 'pyGDP.' + world.name_spaces[x]
        world.responses += [[to_evaluate, server_status_is_good(eval(to_evaluate))[1]]]


@step(r'Then I get a working response for each one')
def check_responses(step):
    for response in world.responses:
        print(response[0] + ': ' + str(response[1]))
        assert response[1] is True


def server_status_is_good(url):
    host, path = urlparse(url)[1:3]
    try:
        print(host, path)
        connection = httplib.HTTPConnection(host)
        connection.request('HEAD', path)
        response = connection.getresponse().status
        print(response)
        if response > 400:
            return False
        return 'Good', True
    except StandardError:
        return url, True


def print_status():
    for x in range(len(world.name_spaces)):
        to_evaluate = 'pyGDP.' + world.name_spaces[x]
        print(to_evaluate + ':')
        print(server_status_is_good(eval(to_evaluate))[0])
