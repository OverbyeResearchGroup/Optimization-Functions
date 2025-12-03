from esa import SAW
import json
import pandas as pd
import math



def update_powerworld_from_json(pwb_path, json_path, gen_mapping):
    """
    Update a PowerWorld case with generator and bus data from a PowerModels JSON solution.
    Prints system state before and after updates.

    Parameters:
    - pwb_path (str): Path to the PowerWorld case file (.pwb).
    - json_path (str): Path to the PowerModels JSON solution file.
    - gen_mapping (dict, optional): Dictionary mapping JSON gen_id to (BusNum, GenID).
      If None, will auto-map generators based on bus numbering.

    Returns:
    - bool: True if successful, False if an error occurs.
    """

    pw = SAW(pwb_path)
        
    # Get actual base MVA from the case
    BaseMVA = 100

    # --- Get existing generators to auto-create mapping if needed ---
    gen_fields = ["BusNum", "GenID", "GenMW", "GenMVR"]
    '''existing_gens = pw.GetParametersMultipleElement("Gen", ["BusNum", "GenID"])
        
     Create default mapping if not provided
    if gen_mapping is None:
        gen_mapping = {}
        # Create mapping based on existing generators (JSON gen_id -> (BusNum, GenID))
        for i, gen in enumerate(existing_gens, start=1):
            gen_id_str = str(i)  # JSON uses string keys
            gen_mapping[gen_id_str] = (gen["BusNum"], gen["GenID"])
        #print(f"Auto-generated gen_mapping: {gen_mapping}")'''

    # --- Bus Data ---
    bus_fields = ["BusNum", "BusNomVolt", "BusPUVolt", "BusAngle"]
    bus_data = pw.GetParametersMultipleElement("Bus", bus_fields)
    bus_df = pd.DataFrame(bus_data, columns=bus_fields)


    # --- Generator Data ---
    gen_data = pw.GetParametersMultipleElement("Gen", gen_fields)
    gen_df = pd.DataFrame(gen_data, columns=gen_fields)

    # === Load the JSON solution ===
    with open(json_path, "r") as f:
        solution = json.load(f)

    # === Update bus voltages and angles ===
    param_list_bus = ["BusNum", "BusPUVolt", "BusAngle"]
    value_list_bus = []

    for bus_id, bus_data in solution.get("bus", {}).items():
        bus_num = int(bus_id)
        volt = float(bus_data.get("vm", 1.0))
        angle_rad = float(bus_data.get("va", 0.0))
        angle_deg = math.degrees(angle_rad)  # Convert radians to degrees
        print(f"Updating bus {bus_num}: Volt={volt:.4f}, Angle={angle_deg:.2f}°")
        value_list_bus.append([bus_num, volt, angle_deg])

    if value_list_bus:
        print("Applying changes to buses...")
        pw.ChangeParametersMultipleElement("Bus", param_list_bus, value_list_bus)

    # === Update generator outputs ===
    param_list_gen = ["BusNum", "GenID", "GenMW", "GenMVR"]
    value_list_gen = []

    for gen_id, gen_data in solution.get("gen", {}).items():
        if gen_id not in gen_mapping:
            print(f"Warning: Generator {gen_id} not found in mapping, skipping...")
            continue
                
        bus_num, gen_id_str = gen_mapping[gen_id]
        pg = float(gen_data.get("pg", 0.0)) * BaseMVA  # pu → MW
        qg = float(gen_data.get("qg", 0.0)) * BaseMVA  # pu → MVAr
            
        print(f"Updating generator at bus {bus_num}, ID {gen_id_str}: "
                f"GenMW={pg:.2f} MW, GenMVR={qg:.2f} MVAr")
        value_list_gen.append([bus_num, gen_id_str, pg, qg])

    if value_list_gen:
        print("Applying changes to generators...")
        pw.ChangeParametersMultipleElement("Gen", param_list_gen, value_list_gen)

    # Save the case
    print("Changes made Saving Case")
    pw.SaveCase(pwb_path)
    return True
