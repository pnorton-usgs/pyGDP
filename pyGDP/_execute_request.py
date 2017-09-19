from __future__ import (absolute_import, division, print_function)

from owslib.wps import WebProcessingService, monitorExecution
from .namespaces import WPS_URL
from .namespaces import WPS_attempts
from time import strftime, sleep

from owslib.util import log


def dodsReplace(dataSetURI, verbose=False):
    if "/dodsC" in dataSetURI:
        dataSetURI = dataSetURI.replace("https", "dods").replace("http", "dods")
    return dataSetURI


def _executeRequest(processid, inputs, output, verbose=False, outputFilePath=None, sleepSecs=10, async=False):
    """
    This function makes a call to the Web Processing Service with
    the specified user inputs.
    """
    wps = WebProcessingService(WPS_URL, verbose=verbose)

    if async:
        # Return the execution object. This can be monitored via user-supplied code
        return wps.execute(processid, inputs, output)
    else:
        # Blocks waiting for the execution to complete and then returns the file path to the results
        execution = wps.execute(processid, inputs, output)

        # sleepSecs = sleepSecs
        err_count = 1

        while not execution.isComplete():
            try:
                monitorExecution(execution, sleepSecs, download=False)  # monitors for success
                err_count = 1
            except Exception:
                log.warning('An error occurred while checking status, checking again. ' +
                            'Sleeping {} seconds...'.format(sleepSecs))
                err_count += 1

                if err_count > WPS_attempts:
                    raise Exception('The status document failed to return, status checking has aborted. ' +
                                    'There has been a network or server issue preventing the status document ' +
                                    'from being retrieved, the request may still be running. For more information, ' +
                                    'check the status url {}'.format(execution.statusLocation))
                # sleep(sleepSecs)    # monitorExecution calls checkStatus which handles the sleeping

        # Check for any problems with the execution result
        _check_for_execution_errors(execution)

        # Attempt to retrieve the file
        if outputFilePath is None:
            outputFilePath = 'gdp_' + processid.replace('.', '-') + '_' + strftime("%Y-%m-%dT%H-%M-%S-%Z")

        done = False
        err_count = 1
        while not done:
            try:
                # 20170919 PAN: the getOutput routine called by monitorExecution does not
                #               return any formal exception unless the execution did not succeed.
                #               What exception is being caught here?
                monitorExecution(execution, download=True, filepath=outputFilePath)
                done = True
            except Exception:
                log.warning('An error occurred while trying to download the result file, trying again.')
                err_count += 1
                sleep(sleepSecs)

                if err_count > WPS_attempts:
                    raise Exception('The process completed successfully, but an error occurred while downloading ' +
                                    'the result. You may be able to download the file using the link at the bottom ' +
                                    'of the status document: {}'.format(execution.statusLocation))

        return outputFilePath


def _check_for_execution_errors(execution):
    """wps does not raise python errors if something goes wrong on the server side
    we will check for errors, and the succeeded status and raise python
    Exceptions as needed
    """
    errmsg = ""

    if execution.status == "ProcessFailed":
        errmsg = "The remote process failed!\n"

    if execution.errors:
        # something went wrong, it would be a shame to pass silently
        errmsg += "\n".join([err.text for err in execution.errors])

    if errmsg:
        raise Exception(errmsg)
