import os
import json
import subprocess
import time

# Define the folder containing LAS files
las_folder = '/home/abbyhildebrandt/pointcloud/great_divide_demo'
pipeline_file_path = '/home/abbyhildebrandt/pointcloud/great_divide_demo/pipeline_gd.json'


# Load the existing pipeline configuration
with open(pipeline_file_path, 'r') as file:
    pipeline = json.load(file)

# Define the interval for printing progress (10 minutes)
progress_interval = 600  # 600 seconds = 10 minutes


# Loop through each LAS file in the folder
for filename in os.listdir(las_folder):
    if filename.endswith('.las'):
        # Extract just the file name (not the full path)
        file_name_only = os.path.basename(filename)
        
        # Update the pipeline configuration with the new file name
        pipeline['pipeline'][0]['filename'] = file_name_only
        
        # Save the updated pipeline configuration to a new file
        updated_pipeline_file_path = f'pipeline_{file_name_only}.json'
        with open(updated_pipeline_file_path, 'w') as file:
            json.dump(pipeline, file, indent=2)
        
        print(f"Starting ingest of {updated_pipeline_file_path}")

        start_time = time.time()  # Record the start time
        
        # Execute the pipeline with the updated configuration
        try:
            result = subprocess.run(['pdal', 'pipeline', updated_pipeline_file_path],
                                    capture_output=True, text=True)
            
            # Check if the subprocess completed successfully
            if result.returncode == 0:
                print(f"Success for {filename}")
            else:
                print(f"Error for {filename}")
                print("Error message:", result.stderr)
        except Exception as e:
            print(f"Exception occurred for {filename}: {e}")

        # Print progress message every 10 minutes
        while result.returncode is None:  # Loop while the subprocess is running
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            if elapsed_time >= progress_interval:
                print("Processing...")
                start_time = current_time  # Reset the start time for the next interval
            
            # Sleep for a short time before checking again
            time.sleep(30)  # Check every 30 seconds
            
