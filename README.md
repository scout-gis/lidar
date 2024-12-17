# lidar
A repo for lidar data management and other process storage. 


## Setup 
Pdal is the only package necessary for this ingestion process. It is highly recommended that you set up an anaconda or miniconda environment specifically to house the PDAL package, as it has lots of dependencies and doesn't play nicely with others. See more information at https://pdal.io/en/2.8.2/ . 
As listed on PDALs homepage (listed above), create a new environment and run `conda install -c conda-forge pdal python-pdal gdal` to install PDAL. 

 - IF you are needing access to the GIS-Automation VM PostgreSQL Database for lidar storage, please reachout to Josh with Neighborhood IT, Abby Hildebrandt, or Jacob Paul.

Contents of This Repository: 

1. pipeline_template.json
    This pipeline contains the pg_pointcloud specific instructions for importing the data into postgres. For more information about exactly how to format this pipeline, see https://pgpointcloud.github.io/pointcloud/quickstart.html#running-a-pipeline . This pipeline is referenced in the loopthru.py execution script referenced below. 

2. loopthru.py
    This python script allows the user to loop thru all the las files in a folder and ingest them using a single command, instead of going file by file. The loopthru script takes 2 inputs, the location of the above pipeline json, and the location of the las files. 

 NOTE: The loopthru file and the pipeline json should be located within the folder containing the las files when the user runs the loop thru file.  

#### Naming Convention and Best Storage Practices: 
    
- Each dataset should be saved in a separate table in postgres. 
- The naming convention should be as follows: "[project name]__[contractor who flew the lidar]__[date the lidar was flown]"
