from __future__ import (absolute_import, division, print_function)

import os
import zipfile


def shapeToZip(inShape, outZip=None, allFiles=True):
    """Packs a shapefile to ZIP format.

    arguments
    -inShape -  input shape file

    -outZip -   output ZIP file (optional)
      default: <inShapeName>.zip in same folder as inShape
      (If full path not specified, output is written to
      to same folder as inShape)

    -allFiles - Include all files? (optional)
      True (default) - all shape file components
      False - just .shp,.shx,.dbf,.prj,shp.xml files

    reference: Esri, Inc, 1998, Esri Shapefile Technical Description
      http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf

    author: Curtis Price, cprice@usgs.gov"""

    if not os.path.splitext(inShape)[1] == ".shp":
        raise Exception("inShape must be a *.shp")

    if not os.path.exists(inShape):
        raise Exception("{} not found".format(inShape))

    # get shapefile root name "path/file.shp" -> "file"
    # and shapefile path
    root_name = os.path.splitext(os.path.basename(inShape))[0]
    inShape = os.path.realpath(inShape)
    in_dir = os.path.dirname(inShape)

    # output zip file path
    if outZip in [None, ""]:
        # default output: shapefilepath/shapefilename.zip
        out_dir = in_dir
        outZip = os.path.join(out_dir, root_name) + ".zip"
    else:
        out_dir = os.path.dirname(outZip)
        if out_dir.strip() in ["", "."]:
            # if full path not specified, use input shapefile folder
            out_dir = os.path.dirname(os.path.realpath(inShape))
        else:
            # if output path does exist, raise an exception
            if not os.path.exists(out_dir):
                raise Exception("Output folder {} not found".format(out_dir))
        outZip = os.path.join(out_dir, outZip)
        # enforce .zip extension
        outZip = os.path.splitext(outZip)[0] + ".zip"

    if not os.access(out_dir, os.W_OK):
        raise Exception("Output directory {} not writeable".format(out_dir))

    if os.path.exists(outZip):
        os.unlink(outZip)

    try:
        # open zipfile
        zf = zipfile.ZipFile(outZip, 'w', zipfile.ZIP_DEFLATED)

        # write shapefile parts to zipfile
        shape_ext = ["shp", "shx", "dbf", "prj", "shp.xml"]

        if allFiles:
            shape_ext += ["sbn", "sbx", "fbn", "fbx", "ain", "aih", "isx", "mxs", "atx", "cpg"]

        for f in ["%s.%s" % (os.path.join(in_dir, root_name), ext) for ext in shape_ext]:
            if os.path.exists(f):
                zf.write(f, os.path.basename(f))
                # print f # debug print
        return outZip
    except Exception as msg:
        raise Exception("Could not write zipfile {}\n{}".format(outZip, str(msg)))
    finally:
        zf.close()
