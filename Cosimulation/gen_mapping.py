import pandas as pd
import json

def create_gen_mapping(pw, file_path):
    """
    Create a generator mapping dictionary from PowerWorld data and save it to a file.
    
    Args:
        pw: PowerWorld Python API object (e.g., from pw.Connect or similar)
        file_path (str): Path where the generator mapping will be saved as a JSON file
        
    Returns:
        dict: Mapping of generator ID (str) to tuple (BusNum, GenID)
    """
    # Define the fields to retrieve
    gen_fields = ["BusNum", "GenID"]
    
    # Fetch generator data from PowerWorld
    gen_data = pw.GetParametersMultipleElement("Gen", gen_fields)
    
    # Convert to DataFrame
    gen_df = pd.DataFrame(gen_data)
    
    # Initialize the mapping dictionary
    gen_mapping = {}
    gen_id_counter = 1  # Start counter for unique generator IDs
    
    # Iterate over the DataFrame to build the mapping
    for index, row in gen_df.iterrows():
        bus_num = int(row["BusNum"])  # Ensure BusNum is an integer
        gen_id = str(row["GenID"])    # Convert GenID to string
        gen_key = str(gen_id_counter)
        # Use tuple for in-memory dictionary
        gen_mapping[gen_key] = (bus_num, gen_id)
        gen_id_counter += 1
    
    # Save the mapping to the specified file path as JSON with line breaks
    with open(file_path, 'w') as f:
        json_str = json.dumps(gen_mapping)
        formatted_json = '{\n ' + ', \n '.join(
            f'"{k}": {json.dumps(v)}' for k, v in gen_mapping.items()
        ) + '\n}'
        f.write(formatted_json)

    
    return gen_mapping

# Example usage (assuming pw is your PowerWorld API connection)
# pw = pw.Connect(...)  # Initialize PowerWorld connection as needed
# gen_mapping = create_gen_mapping(pw, "path/to/save/gen_mapping.json")
# print(gen_mapping)