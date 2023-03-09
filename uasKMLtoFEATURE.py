# Drone KML flight lines to feature

# This is a notebook that is to be run from the UAS Operations aprx
# originally this was created in a jupyter notebook, but can run as a single script.

# new cells in the notebook will be marked with a comment identifying them as such.

# This notebook takes kml files from the DJI Agras Management Platform and converts them to a Feature.
# This feature is then placed in the UAS Operations.gdb 
# The name of the file matches up with the Name field of the corresponding spray block shape.

#cell 1 

import arcpy
import os
os.system("color")

kmlDir = r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras"
arcpy.env.overwriteOutput = True
print('overwrite output is enabled')

#user input for naming drone spray line.
inputSprayLineFileName = input("Enter file name for Drone Treatment Line in this format Date_Area_Chemical example: Jan1_OgdenBay_NatularG ")

print(' {}  is what the finished file will be named.'.format(inputSprayLineFileName))


# Group titled FUNCTIONS

#cell 2


# create shapefile from drone kml
# first you need to have the kml downloaded from agras managment
# placed as the only files in the following directory 
#\\sever\COMPANY DATA FILES\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras
def kml_to_feature():
#     arcpy.env.addOutputsToMap = 0
    arcpy.env.overwriteOutput = True
#got this from https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/kml-to-layer.htm
# Set workspace (where all the KMLs are)
    arcpy.env.workspace = kmlDir
# Set local variables and location for the consolidated file geodatabase
    out_location = r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras"
    gdb = 'AllKMLLayers.gdb'
    gdb_location = os.path.join(out_location, gdb)
# Create the primary file geodatabase
    arcpy.management.CreateFileGDB(out_location, gdb)
# Convert all KMZ and KML files found in the current workspace
    for kmz in arcpy.ListFiles('*.KM*'):
        print("CONVERTING: {0}".format(os.path.join(arcpy.env.workspace, kmz)))
        kmzFile = os.path.join(arcpy.env.workspace, kmz)
        arcpy.conversion.KMLToLayer(kmzFile, out_location) 
    print('starting to transfer to gdb')
# Change the workspace to fGDB location
    arcpy.env.workspace = out_location
# Loop through all the file geodatabases in the workspace
    wks = arcpy.ListWorkspaces('*', 'FileGDB')
# Skip the primary GDB
    wks.remove(gdb_location)
    #     arcpy.env.addOutputsToMap = 1
    for fgdb in wks:
    # Change the workspace to the current file geodatabase
        arcpy.env.workspace = fgdb
    # For every feature class inside, copy it to the primary and use the name 
    # from the original fGDB  
        feature_classes = arcpy.ListFeatureClasses('*', '', 'Placemarks')
        for fc in feature_classes:
            print("COPYING: {} FROM: {}".format(fc, fgdb))
            fcCopy = os.path.join(fgdb, 'Placemarks', fc)
            arcpy.conversion.FeatureClassToFeatureClass(fcCopy, gdb_location, fgdb[fgdb.rfind(os.sep) + 1:-4])
#         arcpy.management.Delete(fgdb)
        
    print('finished kml_to_layer')
    print('starting merge....')
    
    def merge():
        arcpy.env.addOutputsToMap = 1
        outputSprayLineFileName = r"M:\USERS COMPUTERS\Design\Documents\ArcGIS\Projects\UAS Operations\UAS Operations.gdb\{}".format(inputSprayLineFileName)
#         Name =  r"M:\USERS COMPUTERS\Design\Documents\ArcGIS\Projects\UAS Operations\UAS Operations.gdb\test"
        outputGDB = r"M:\USERS COMPUTERS\Design\Documents\ArcGIS\Projects\UAS Operations\UAS Operations.gdb"
        arcpy.env.workspace =  r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras\AllKMLLayers.gdb"
        fcs = arcpy.ListFeatureClasses()
        print('merging..... output to ' + outputSprayLineFileName)
        arcpy.management.Merge(fcs, outputSprayLineFileName)
        print('finished Merge')
    merge()
def deleteKML():
    arcpy.env.workspace = r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras"
    for kmz in arcpy.ListFiles('*.KM*'):
        if arcpy.Exists(kmz):
            print("Deleting: {0}".format(os.path.join(arcpy.env.workspace, kmz)))
            kmzFile = os.path.join(arcpy.env.workspace, kmz)
            arcpy.management.Delete(kmz)
        print('kml and kmz files deleted from working directory')

def deleteGDB():
    arcpy.env.workspace = r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras"
    for gdb in arcpy.ListFiles('*.gdb*'):
        if arcpy.Exists(gdb):
            gdbFile = os.path.join(arcpy.env.workspace, gdb)
            print("Deleting: {0}".format(os.path.join(arcpy.env.workspace, gdb)))
            arcpy.management.Delete(gdbFile)
        print('Deleted all GDB from working directory')

def deleteLYRX():
    arcpy.env.workspace = r"M:\USERS COMPUTERS\Design\Desktop\Drone Documents\Flight Log Backups\Agras"
    for lyrx in arcpy.ListFiles('*.lyrx*'):
        if arcpy.Exists(lyrx):
            lyrxFile = os.path.join(arcpy.env.workspace, lyrx)
            print('Deleting: {0}'.format(os.path.join(arcpy.env.workspace, lyrx)))
            arcpy.management.Delete(lyrxFile)
        print('Deleted all .lyrx files from working directory')
        
print('functions are set up')

def droneSprayLines():
    kml_to_feature()
    deleteKML()
    deleteGDB()
    deleteLYRX()


# cell 3   RUNNING THE FUNCTIONS

droneSprayLines()

