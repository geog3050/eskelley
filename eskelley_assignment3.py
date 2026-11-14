"""Assignment 3: Spatial Overlays and Areal Interpolation.
Complete three functions using ArcPy and pathlib.Path. Prepare and project
copies before analysis; preserve inputs and avoid hardcoded paths or values.
Check input paths, geometry types, fields, coordinate systems, and output names.
Use try/except handling to catch and report errors.
Find and download census boundaries, a census/ACS numeric attribute, and roads (or another dataset with line geometry).
"""
import arcpy
from pathlib import Path
import os
import csv
import math
import random

def hawkid():
    return ["Emma Skelley", "eskelley"]


# Problem 1 (20 points)
def prepare_data(input_fc, output_geodatabase, out_coordinate_system, in_field=None, join_table=None, join_field=None, value_field=None):
    arcpy.env.overwriteOutput = True
    folder = os.path.dirname(input_fc)
    arcpy.env.workspace = folder
    try: #Create new gdb to store outputs
        output_dir = os.path.dirname(input_fc)
        output_name = os.path.basename(output_geodatabase)
        arcpy.management.CreateFileGDB(str(output_dir), str(output_name))
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    
    try: #project shapefiles into preferred coordinate system, then save them to the output geodatabase
        arcpy.env.workspace = output_geodatabase
        projected_fc = os.path.join(output_geodatabase, input_fc).replace('.shp', '_projected' +'.shp')
        bg = arcpy.Project_management(input_fc, projected_fc, out_coordinate_system)
        print(projected_fc)
        arcpy.management.AddField(bg, "SRC_KM2", "DOUBLE")
        arcpy.management.CalculateGeometryAttributes(bg, [["SRC_KM2", "AREA"]], area_unit="SQUARE_KILOMETERS")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))

    try: #join csv table to polygons
        with open(join_table, encoding="utf-8-sig", newline="") as file:
            records = list(csv.DictReader(file))
        table = (Path(output_geodatabase) / (Path(input_fc).stem + "_attributes"))
        arcpy.management.CreateTable(output_geodatabase, Path(table).name)
        arcpy.management.AddField(table, join_field, "TEXT", field_length=12)
        arcpy.management.AddField(table, value_field, "DOUBLE")
        with arcpy.da.InsertCursor(table, [join_field, value_field]) as cur:
            for r in records:
                cur.insertRow([r[join_field], float(r[value_field])])
        arcpy.management.JoinField(projected_fc, join_field, table, join_field, [value_field])
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    pass
def estimatePopulationInZone(source_polygons, population_field, study_zone, output_fc)
    try: #begin to create the study zone buffers that will be later intersected
        N_POLYGONS = 4
        SEED = 15
        BUFFER_METERS = 2000
        bg = source_polygons
        with arcpy.da.SearchCursor(bg, ["GEOID", "SHAPE@"]) as rows:
            candidates = sorted(list(rows), key=lambda row: row[0])
        if not 1 <= N_POLYGONS <= len(candidates):
            raise ValueError("N_POLYGONS must be between 1 and the number of block groups.")
        chosen = random.Random(SEED).sample(candidates, N_POLYGONS)
     except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    try:
        buffer_sites = "polygon_buffer_sites"
        if arcpy.Exists(buffer_sites):
            arcpy.management.Delete(buffer_sites)
        arcpy.management.CreateFeatureclass((Path(polygons)), "polygon_buffer_sites", "POINT", spatial_reference=out_coordinate_system)
        arcpy.management.AddField(buffer_sites, "SITE_ID", "LONG")
        arcpy.management.AddField(buffer_sites, "SITE_NAME", "TEXT", field_length=60)
        arcpy.management.AddField(buffer_sites, "BG_GEOID", "TEXT", field_length=12)
        with arcpy.da.InsertCursor(buffer_sites, ["SHAPE@", "SITE_ID", "SITE_NAME", "BG_GEOID"]) as rows:
            for number, (geoid, geometry) in enumerate(chosen, 1):
                point = arcpy.PointGeometry(geometry.labelPoint, out_coordinate_system) #Assigning coordinate system to point
                rows.insertRow([point, number, f"Site buffer{number}", geoid])
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    
    try: #create the buffers
        if BUFFER_METERS <= 0:
        raise ValueError("BUFFER_METERS must be positive.")
        zone = study_zone
        arcpy.analysis.Buffer(buffer_sites, zone, f"{BUFFER_METERS} Meters", dissolve_option="ALL")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    
    try: #make sure that the CRS is the same 
        source_sref = arcpy.Describe(source_polygons).spatialReference
        zone_sref = arcpy.Describe(study_zone).spatialReference
        if source_sref.factoryCode != zone_sref.factoryCode or source_sref.linearUnitName.lower() != "meter":
            raise ValueError("Inputs must share the same projected CRS in meters.")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))

    try: #intersect the study zone with the original source polygons and calculate the estimates for population
        overlap = output_fc
        arcpy.analysis.Intersect([bg, zone], overlap, join_attributes="ALL")
        for field in ["PART_KM2", "EST_POP"]:
            arcpy.management.AddField(overlap, field, "DOUBLE")
        arcpy.management.CalculateGeometryAttributes(overlap, [["PART_KM2", "AREA"]], area_unit="SQUARE_KILOMETERS")
        fields = [population_field, "SRC_KM2", "PART_KM2", "EST_POP"]
        with arcpy.da.UpdateCursor(overlap, fields) as rows:
            for row in rows:
                population, full_area, part_area, _ = row
                if population is None or population < 0 or full_area <= 0:
                    raise ValueError("Check joined population and original polygon area.")
                fraction = part_area / full_area
                if not -1e-6 <= fraction <= 1 + 1e-6:
                    raise ValueError("Unexpected area fraction; inspect geometry.")
                row[3] = population * fraction
                rows.updateRow(row)
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))

    try: #total the estimates for the study_zone
        totals = {field: 0 for field in fields}
        with arcpy.da.SearchCursor(overlap, fields) as rows:
            for row in rows:
                for i, field in enumerate(fields):
                    if row[1] is not None:
                        totals[field] += row[i]
        for field, total in totals.items():
            print(f"Total for {field}: {total}")
    pass

# Problem 3 (40 points)
def summarizeLineLength(lines, polygons, polygon_id_field, output_fc):
    try: #make sure that the CRS is the same 
        polygons_sref = arcpy.Describe(polygons).spatialReference
        lines_sref = arcpy.Describe(lines).spatialReference
        if polygons_sref.factoryCode != lines_sref.factoryCode or polygons_sref.linearUnitName.lower() != "meter":
            raise ValueError("Inputs must share the same projected CRS in meters. Project to the same CRS.")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))

    try: #intersect the lines and polygon features and then measure the lengths of lines
        intersection = arcpy.analysis.Intersect([lines, polygons], "intersected_polylines", join_attributes="ALL")
        arcpy.management.AddField(intersection, length_field, "DOUBLE")
        arcpy.management.CalculateGeometryAttributes(intersection, [[length_field, "LENGTH"]], "METERS")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))

    try: #create a summary table that will sum the lengths of lines, then join to the output_fc
        summary_table = os.path.join(lines, "summary_table")
        arcpy.Statistics_analysis("intersected_polygons", summary_table, [["LINE_KM", "SUM"]], "ZONE_ID")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
            print('Error was caught!')
            print(arcpy.GetMessages(0))
    
    try: #copy the features of the polygons into the output_fc and join the totals back in the output from the summary table    
        arcpy.management.CopyFeatures(polygons, output_fc)
        arcpy.management.AddField(output_fc, length_field, "DOUBLE")
        arcpy.management.JoinField(output_fc, "ZONE_ID", "summary_table", "ZONE_ID", ["SUM_LINE_KM"])
        with arcpy.da.UpdateCursor(output_fc, ["SUM_LINE_KM", "LINE_KM"]) as rows:
            for row in rows: 
                row[1] = row[0] if row[0] is not None else 0.0
                rows.updateRow(row)
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    
    try: #print line length totals
        with arcpy.da.SearchCursor(output_fc, ["ZONE_ID", "LINE_KM"]) as rows:
            for row in rows:
                print(f"Polygon {row[0]} has {row[1]} km of lines")
    except arcpy.ExecuteError: # if any errors are found, this will return the error code and describe the type of error
        print('Error was caught!')
        print(arcpy.GetMessages(0))
    pass


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == "__main__" and hawkid()[1] == "hawkid":
    print("### Error: YOU MUST provide your HawkID in the hawkid() function.")
