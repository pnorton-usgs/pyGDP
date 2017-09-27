from __future__ import print_function
from builtins import input

import pyGDP

"""
This simple client script demonstrates the basic workflow of the Geo Data Portal in python. 

Shapefile upload has not been implemented here.

The CSW Client is very rudimentary, copy and paste of the "dods" url is required.

The client requests only the first time step of a dataset to minimize processing overhead of the demonstration.

"""


def get_input(input_list):
    for i in input_list:
        print(i)

    print('\n' + 'Choose from the list above (hit ENTER for a default):')
    usrinput = str(input())
    assert isinstance(usrinput, str)

    if usrinput == "":
        usrinput = "sample:CONUS_states"
        print(usrinput)
    else:
        while usrinput not in input_list:
            print('not a valid input')
            usrinput = str(input())
            assert isinstance(usrinput, str)
    return usrinput


def get_input_1(input_list):
    for i in input_list:
        print(i)

    print('\n' + 'Choose from the list above (hit ENTER for a default):')
    usrinput = str(input())
    assert isinstance(usrinput, str)

    if usrinput == "":
        usrinput = "STATE"
        print(usrinput)
    else:
        while usrinput not in input_list:
            print('not a valid input')
            usrinput = str(input())
            assert isinstance(usrinput, str)
    return usrinput


def get_input_2(input_list):
    for i in input_list:
        print(i)

    print('\n' + 'Choose from the list above or use "++" to choose all (hit ENTER for a default):')
    usrinput = str(input())
    assert isinstance(usrinput, str)

    if usrinput == "":
        usrinput = "Wisconsin"
        print(usrinput)
    else:
        while usrinput not in input_list:
            if usrinput == '++':
                print("All values selected")
                return input_list
            print('Not a valid input, please try again.')
            usrinput = str(input())
            assert isinstance(usrinput, str)
        print(usrinput)
    return usrinput


def get_input_3(input_list):
    for i in input_list:
        print(i)

    print('\n' + 'Choose an OPeNDAP url from the list above (hit ENTER for a default):')
    usrinput = str(input())
    assert isinstance(usrinput, str)

    if usrinput == "":
        usrinput = "dods://cida.usgs.gov/thredds/dodsC/UofIMETDATA"
        print(usrinput)
    else:
        while 'dods' not in usrinput:
            print("This doesn't appear to be a valid dods url. Please enter an OPeNDAP url.")
            usrinput = str(input())
            assert isinstance(usrinput, str)
    return usrinput


def getinput_4():
    print('Enter a search term or press ENTER to return all datasets in catalog.')
    usrinput = str(input())
    assert isinstance(usrinput, str)
    return usrinput


def get_input_5(input_list):
    for i in input_list:
        print(i)

    print('\n' + 'Choose from the list above (hit ENTER for a default):')
    usrinput = str(input())
    assert isinstance(usrinput, str)

    if usrinput == "":
        usrinput = "surface_downwelling_shortwave_flux_in_air"
        print(usrinput)
    else:
        while usrinput not in input_list:
            print('not a valid input')
            usrinput = str(input())
            assert isinstance(usrinput, str)
    return usrinput


def main():
    # This instantiates a pyGDP web processing object. All other processes are done through the web processing
    # object.
    gdp = pyGDP.pyGDPwebProcessing()

    # Returns a list of shapefiles that are currently sitting on the GDP server.
    # It's possible to upload your own shapefile using the .uploadShapefile function.
    sfiles = gdp.getShapefiles()
    for s in sfiles:
        print(s)
    shapefile = get_input(sfiles)

    print()
    print('Get Attributes:')
    # Gets shapefile dbf attributes of the file you chose from the previous selection process.
    # A good example of levels of detail processed by on GDP.
    attributes = gdp.getAttributes(shapefile)
    attribute = get_input_1(attributes)

    print()
    print('Get values:')
    # Yet another level of detail down on the shapefile. This time it is values of an attribute or shapefile.
    # Does all the web processing necessary to show the user what they are working with.
    values = gdp.getValues(shapefile, attribute)
    value = get_input_2(values)

    print()
    # Allows the user to select a dods dataset for processing. The getDataSetURI function returns a lot of
    # metadata making it helpful to narrow down the search with anyText.
    search_string = getinput_4()
    dataset_uris = gdp.getDataSetURI(anyText=search_string)
    dataset_uri = get_input_3(dataset_uris)

    print()
    print('Getting available data_types... \n')
    # Gives a list of the available data types within the dods dataset for processing.
    data_types = gdp.getDataType(dataset_uri)
    data_type = get_input_5(data_types)

    print()
    print('Getting time range from dataset...')
    # This example only uses the first time range (see submitFeatureWeightedGridStatistics execution)
    time_range = gdp.getTimeRange(dataset_uri, data_type)
    for i in time_range:
        print(i)

    print()
    print('Submitting request...')
    # Time for some heavy web services processing. The submitFeatureWeightedGridStaistics is the end product of
    # all the variable choosing we have done up until this point. It takes a lot of inputs and sends them all
    # through a remote processing algorithm associated with GDP. The result is a file downloaded to the location
    # of the executing script, also returned is the URL associated with the download (it usually gives a csv file).
    output = gdp.submitFeatureWeightedGridStatistics(shapefile, dataset_uri, data_type,
                                                     time_range[0], time_range[0], attribute, value, verbose=True)
    print()
    print(output)
    print()

    print("The resulting ouput file (which should now exist in the folder where " +
          "this example was executed) holds the Feature Weighted Grid Statistics " +
          "(just the mean value if you did the default options) of the area chose " +
          "from the 'value' shapefile (from GDP). \nFor more details refer to comments " +
          "in the main method of this example script.")


if __name__ == "__main__":
    main()
