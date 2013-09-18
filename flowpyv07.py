# Flowpy -- takes a square interaction matrix, a corresponding set of point coordinates, and
# and creates a shapefile of flow lines from them. You can choose magnitudes as "raw" two way flow,
# net flow, or gross flow.

# Flowpy is written in Python 2.6 and requires ogr to run.
# Alan Glennon, 19 October 2009

def shapefilemaker(typeofcalculation,fulldirectorystring,outputfilename,fulldirODinput,fulldirPTinput):
        import ogr, os, sys
        #directory location of output file
        os.chdir(fulldirectorystring)
        #location of input file
        odmatrixfilename = fulldirODinput
        nodefilename = fulldirPTinput
        # type of flow calculation -- 1 is two way flow; 2 is gross flow; 3 is net flow

        try: 
            odmatrix = open(odmatrixfilename, 'r')
            nodes = open(nodefilename,'r')
        except IOError, e:
            print 'file open error:', e
            sys.exit()

        numberofnodes = 0
        for line in nodes:
                numberofnodes += 1
        nodes.close

        # interaction file is read. Output result is myodmatrix[rows][columns]
        rows = 0
        myodmatrix = []
        for icounter in xrange(numberofnodes):
                        myodmatrix.append([])
                        for jcounter in xrange(numberofnodes):
                                myodmatrix[icounter].append(icounter+jcounter)

        for eachLine in odmatrix:
                        separatestrings = eachLine.split()
                        columns = 0
                        while columns < numberofnodes:
                            onevalue = float(separatestrings[columns])
                            myodmatrix[rows][columns] = onevalue
                            columns += 1
                        rows += 1
        odmatrix.close

        # points file is read. Output result is mypoints[ptrows][ptcolumns]
        ptrows = 0
        mypoints = []
        for kcounter in xrange(numberofnodes):
                        mypoints.append([])
                        for lcounter in xrange(2):
                                mypoints[kcounter].append(kcounter+lcounter)

        nodesagain = open(nodefilename,'r')
        for eachLine2 in nodesagain:
                        separatestrings2 = eachLine2.split()
                        ptcolumns = 0
                        while ptcolumns < 2:
                                onevalue2 = float(separatestrings2[ptcolumns])
                                mypoints[ptrows][ptcolumns] = onevalue2
                                ptcolumns += 1
                        ptrows += 1
        nodesagain.close


        #START setup creation of shapefile

        # get the driver
        driver = ogr.GetDriverByName('ESRI Shapefile')
        # create a new data source and layer
        if os.path.exists(outputfilename):
            driver.DeleteDataSource(outputfilename)
        ds = driver.CreateDataSource(outputfilename)
        if ds is None:
            print 'Could not create file'
            sys.exit(1)
        layer = ds.CreateLayer('flow', geom_type=ogr.wkbLineString)
        fieldDefn = ogr.FieldDefn('magnitude', ogr.OFTReal)
        layer.CreateField(fieldDefn)
        # END setup creation of shapefile

        #START two way flow calculation. 
        if typeofcalculation == 1:
            counter1 = 0
            counter2 = 0
            while counter2 < numberofnodes:
                    while counter1 < numberofnodes:
                            linester = ogr.Geometry(ogr.wkbLineString)
                            linester.AddPoint(mypoints[counter2][0],mypoints[counter2][1])
                            linester.AddPoint(mypoints[counter1][0],mypoints[counter1][1])
                            featureDefn = layer.GetLayerDefn()
                            feature = ogr.Feature(featureDefn)
                            feature.SetGeometry(linester)
                            feature.SetField('magnitude',myodmatrix[counter2][counter1])
                            layer.CreateFeature(feature)
                            counter1 = counter1 + 1
                    counter2 = counter2 + 1
                    counter1 = 0
        #FINISH two way flow calculation


        #START gross flow calculations
        if typeofcalculation == 2:
            g = 0
            h = 0
            while g < numberofnodes:
                while h < numberofnodes:
                            if (g <= h):
                                    linester = ogr.Geometry(ogr.wkbLineString)
                                    linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                    linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                    if h==g: grossmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])/2
                                    else: grossmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])
                                    featureDefn = layer.GetLayerDefn()
                                    feature = ogr.Feature(featureDefn)
                                    feature.SetGeometry(linester)
                                    feature.SetField('magnitude',grossmagnitude)
                                    layer.CreateFeature(feature)
                            h += 1
                h = 0
                g += 1
        #FINISH gross flow calculations

        #START net flow calculations
        if typeofcalculation == 3:
            g = 0
            h = 0
            while g < numberofnodes:
                while h < numberofnodes:
                            if (g <= h):
                                    if h==g: netmagnitude = (myodmatrix[g][h] + myodmatrix[h][g])/2
                                    else: netmagnitude = (myodmatrix[g][h] - myodmatrix[h][g])
                                    if netmagnitude < 0:
                                        linester = ogr.Geometry(ogr.wkbLineString)
                                        linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                        linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                        featureDefn = layer.GetLayerDefn()
                                        feature = ogr.Feature(featureDefn)
                                        feature.SetGeometry(linester)
                                        feature.SetField('magnitude',netmagnitude * (-1))
                                        layer.CreateFeature(feature)
                                    else:
                                        linester = ogr.Geometry(ogr.wkbLineString)
                                        linester.AddPoint(mypoints[g][0], mypoints[g][1])
                                        linester.AddPoint(mypoints[h][0], mypoints[h][1])
                                        featureDefn = layer.GetLayerDefn()
                                        feature = ogr.Feature(featureDefn)
                                        feature.SetGeometry(linester)
                                        feature.SetField('magnitude',netmagnitude)
                                        layer.CreateFeature(feature)
                            h += 1
                h = 0
                g += 1
        #FINISH net flow calculations

        # shapefile cleanup
        # destroy the geometry and feature and close the data source
        linester.Destroy()
        feature.Destroy()
        ds.Destroy()

