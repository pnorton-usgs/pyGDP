pyGDP
=====

[![Build Status](https://travis-ci.org/USGS-CIDA/pyGDP.svg?branch=master)](https://travis-ci.org/USGS-CIDA/pyGDP)

pyGDP provides a fast and efficient way of making calls to the USGS GeoData Portal.

pyGDP has the following algorithms:
	- FeatureCategoricalGridCoverage
	- FeatureWeightedGridStatistics
	- FeatureCoverageOPenDap
	- FeatureCoverageWCSIntersection

**Before using the Geo Data Portal via Python, please read the scalability guidelines.**  
https://my.usgs.gov/confluence/display/GeoDataPortal/Geo+Data+Portal+Scalability+Guidelines

Additional documentation can be found at the Geo Data Portal wiki.
https://my.usgs.gov/confluence/pages/viewpage.action?pageId=250937417

Dependencies
=================

pyGDP request OWSLib and lxml (which, in turn, uses libxml2 and libxslt).

Usage
=================

You can find example usages and scripts in the examples folder.

Installation
==================
Use of virtualenv and pip is highly recommended.
Sample commands to install pyGDP as a virtual env on a mac/unix operating system are given below.
Similar commands can be used on windows.

```
git clone https://github.com/USGS-CIDA/pyGDP.git
virtualenv -p /usr/bin/python2.7 pyGDP/venv
source pyGDP/venv/bin/activate
cd pyGDP
pip install -r requirements.txt -r requirements-dev.txt
pip install .
lettuce Lettuce_Tests/features/ --tag=-not_working
```

Anaconda and other package managers can be used.

`conda install -c conda-forge pygdp`

Support
=================
Contact gdp@usgs.gov for questions, issues.

Thanks
=================
1. Dave Blodgett
2. Jordan I Walker
3. Jordan Read
4. Steve Kochaver

Disclaimer
----------
This software is in the public domain because it contains materials that originally came from the U.S. Geological Survey,
an agency of the United States Department of Interior.
For more information, see the official USGS copyright policy at [http://www.usgs.gov/visual-id/credit_usgs.html#copyright](http://www.usgs.gov/visual-id/credit_usgs.html#copyright).


Although this software program has been used by the U.S. Geological Survey (USGS),
no warranty, expressed or implied,
is made by the USGS or the U.S. Government as to the accuracy and functioning of the program and related program material nor shall the fact of distribution constitute any such warranty,
and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


 [![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)
