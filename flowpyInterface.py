# Flowpy v07
# The code yields a shapefile of lines with attribute "magnitude" without a spatial reference.
# The code is written in Python 2.6 and needs ogr to run. You can find more information about ogr and its installation at: gdal.org
# Alan Glennon, 19 October 2009


import flowpyv07
import os, sys

# ----------------------------------------------
# Modify the following to your preference.

# type of flow calculation -- 1 is two way flow; 2 is gross flow; 3 is net flow
typeofflowcalculation = 1
# output filename (do not include file suffix shp or kml)
outputfilename = 'flowlines'
# output directory path
outputfilepath = 'c://flowpy/output'
# input matrix filename with its full path
inputinteractionfile = 'c:/flowpy/bankinteract.txt'
# input points filename with its full path
inputpointfile = 'c:/flowpy/bankpoints.txt'
# You can also make a KML of the results: 1 makes a KML. Any other value (like 0) skips KML output.
MakeaKML = 0
# ----------------------------------------------
# ----------------------------------------------
# The following lines take your preferences and sends them to Flowpy for processing. 
flowpyv07.shapefilemaker(typeofflowcalculation,outputfilepath,outputfilename+'.shp',inputinteractionfile,inputpointfile)

# makes a KML
if MakeaKML == 1:
    kmloutput = outputfilename+'.kml'
    ogrprep = 'ogr2ogr -f KML '+kmloutput+'.kml '+outputfilename+'.shp'
    os.system(ogrprep)
else:
    pass
