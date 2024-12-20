# lidar
A repo for lidar data management and other process storage. 


## Setup 
Pdal is the only package necessary for this ingestion process. It is highly recommended that you set up an anaconda or miniconda environment specifically to house the PDAL package, as it has lots of dependencies and doesn't play nicely with others. See more information at https://pdal.io/en/2.8.2/ . 
As listed on PDALs homepage (listed above), create a new environment and run `conda install -c conda-forge pdal python-pdal gdal` to install PDAL. 

 - If you are needing access to the GIS-Automation VM PostgreSQL Database for lidar storage, please reachout to Josh with Neighborhood IT, Abby Hildebrandt, or Jacob Paul.

## Contents of This Repository: 

1. pipeline_template.json
    This pipeline contains the pg_pointcloud specific instructions for importing the data into postgres. For more information about exactly how to format this pipeline, see https://pgpointcloud.github.io/pointcloud/quickstart.html#running-a-pipeline . This pipeline is referenced in the loopthru.py execution script referenced below. 

2. loopthru.py
    This python script allows the user to loop thru all the las files in a folder and ingest them using a single command, instead of going file by file. The loopthru script takes 2 inputs, the location of the above pipeline json, and the location of the las files.

NOTE: The loopthru file and the pipeline json should be located within the folder containing the las files when the user runs the loop thru file.

3. export_pipeline_template.json
    This pipeline is the most basic form of exporting the PostgreSQL table into a las file, to be brought into a GIS software or sent to a consultant. Note that this pipeline will export the entire table into one las file, which is likely not conducive for large data transfers. 
 

#### Naming Convention and Best Storage Practices: 
    
- Each dataset should be saved in a separate table in postgres. 
- The naming convention should be as follows: "PROJECTNAME_CONTRACTOR_DATEOFFLY DAY/MONTH/YEAR"
- The user should make a copy of the json and py files listed above, save them to the folder containing the las files, and rename them to: 
    - loopthru_'project name'.py 
    - pipeline_'projectname'.json

### A few SQL queries and what they do: 

1. `SELECT COUNT(*), SUM(PC_NumPoints(pa)) FROM public.[tablename];` 
    Counts the number of points and patches in the table. 
    
2. 
``` 
SELECT ST_AsGeoJSON(
        ST_Transform(
            ST_SetSRID(
                ST_Extent((PC_Envelope(pa))::geometry), 
                [SRID] 
            ),
            4326
        )
) AS geojson_bounding_box
FROM public.[tablename];
``` 
Queries for the bounding box of the pcpatches within the table, and converts to a readable format. User must enter the table name and SRID, referenced in **public.scoutprojects_referenceguide** 

3. 
```
SELECT SUM(PC_NumPoints(pa)) AS points_in_bbox
FROM public.keyholewind_geoterra_02102024
WHERE PC_Intersects(pa, ST_MakeEnvelope(6399183.99, 2132471.29, 6432142.96, 2163994.4, 2229));
``` 
Calculate point density of a given bounding box. Note the bounding box must be in easting northing format (Projected Coordinate Format). To get the total project bounding box, run the below query. 

```
SELECT ST_Extent((PC_Envelope(pa))::geometry) AS bounding_box FROM public.[tablename];
```
4. 
``` 
SELECT 
    MIN(PC_Get(pt, 'Z')) AS min_z,
    MAX(PC_Get(pt, 'Z')) AS max_z,
    AVG(PC_Get(pt, 'Z')) AS avg_z
FROM (
    SELECT PC_Explode(pa) AS pt
    FROM public.[tablename]
) exploded_points;
```
Calculates the maximum, minimum, and average z value, in Ft. 

## Reference Guide
Upon completion of data ingest, the user should add a new row to the **public.scoutprojects_referenceguide**, which specifies: 
- Table Name of data that was ingested 
- SRID
- Primary Key ID (integer in order)
- Contractor 
- Date of Flight in Day/Month/Year

Enter this information manually by adding a new row to the table. 

## QAQC 

After ingesting the data, its important to run Quality Control on the dataset.
- Does the summary sheet that comes with the data in accordance with our spec?  
- Did all the las files come from the consultant in order? Are there any numbers missing? 
- Are the las files sized appropriately? Are any of them egregiously large or small? 
- Did the data ingest throw any errors? 
- When running `SELECT COUNT(*), SUM(PC_NumPoints(pa)) FROM public.[tablename];` , does the number of patches, multiplied by patch size, equal the total number of points ? 
- Pull the data into a map in QGIS. Does the data cover the expected project area? 


## Alternative Deliverables 

#### DTM: 
The GIS team can provide a DTM for Engineering or any other department that might require one. We will need a .las file or bounding box of the area of interest. 
Example: 
![Alt text](images\great_divide_test5.png)
