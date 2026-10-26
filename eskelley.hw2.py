###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Emma Skelley", "eskelley"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    import arcpy
    import os
    arcpy.env.workspace = workspace
    try: 
        featureclasses = arcpy.ListFeatureClasses()
        for fc in featureclasses:
            desc = arcpy.Describe(fc) 
            shape = desc.shapeType
            if shape == 'NoneType':
                print(f"The shapefile {fc} has no feature class.") #Just in case there is a problem with the shapefile, this will identify if there is no feature class listed
            else:
                print(f"The shapefile {fc} is a {shape} feature class.") #This will create a loop that will print the feature class and its shape type based on the input feature classes
    except arcpy.ExecuteError: 
        print('Error was caught!')
        print(arcpy.GetMessages(0))
###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    import arcpy
    import os
    arcpy.env.workspace = workspace
    fields = arcpy.ListFields(inputFc) #This will create a fields variable that holds all the fields for the input feature class
    numericfield = {'Integer', 'Float', 'Double'} #This variable will only find field types with the interested numerical types
    try:
        for field in fields:
            if field.type in numericfield:
                print(f'{field.name} is a {field.type}') #This will create a loop that will only print the field name and type when it matches the numericfield variable
    except arcpy.ExecuteError:
        print('Error was caught!')
        print(arcpy.GetMessages(0))
###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    import arcpy
    import os
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_geodatabase
    try:
        output_dir = os.path.dirname(output_geodatabase)
        output_name = os.path.basename(output_geodatabase)
        arcpy.management.CreateFileGDB(output_dir, output_name) #This will create new geodatabase to store particular shapefiles 
        featureclasses = arcpy.ListFeatureClasses()
        for fc in featureclasses:
            desc = arcpy.Describe(fc)
            shape = desc.shapeType
            if shape in shapeType:
                arcpy.CopyFeatures_management(fc, os.path.join(output_geodatabase, fc)) #This will create a loop that will search through feature classes and only copy the particular shape fcs into the new geodatabase
    except arcpy.ExecuteError:
        print('Error was caught!')
        print(arcpy.GetMessages(0))
###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    import arcpy
    import os
    try:
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True 
        joinFC = arcpy.management.AddJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, 'KEEP_COMMON') #This tool will join the input table into the input feature class
        join_result = arcpy.management.CopyFeatures(joinFC, 'joinFC') #Here the results from the join will be created as a new feature class deposited into the workspace
        matched_records = (arcpy.management.GetCount(join_result)) 
        matched_count = int(matched_records[0])
        original_records = (arcpy.management.GetCount(inputTable))
        original_count = int(original_records[0])
        unmatched_count = matched_count - original_count #This process takes the records from the join results as well as the input table and creates counts for them both while converting them to integers
        print(f"There are {matched_count} matched records and {unmatched_count} unmatched records.") #Those counts are then subtracted and printed for the user to compare how many results were actually joined; zero unmatched counts indicates the function joined correctly
    except arcpy.ExecuteError:
        print('Error was caught!')
        print(arcpy.GetMessages(0))
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
