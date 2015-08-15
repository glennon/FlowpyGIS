FlowpyGIS
=========

A Python 2.7 script to convert an origin-destination (OD) matrix to a shapefile. The flowpyv*.py part of things does the work (reorganizes the input OD table and feeds your data to GDAL/OGR). I also created a basic Interface script, flowpyInterface.py to assist in passing the variables to the main script. The .htm file in the repo gives some more info about the required inputs and such.

Ages ago, I made a short demo video --> http://vimeo.com/9264988

For novices the easiest way to get this code rolling is to run it from the shell of FWTools.

Cem Gulluoglu created a plugin for QGIS that offers a GUI for this FlowpyGIS code; The plugin is probably the easiest way to use the software for a normal user. The plugin can be found within QGIS' official plugin repository. More info [here](http://95.9.195.180/).
