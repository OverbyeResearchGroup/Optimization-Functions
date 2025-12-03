from esa import SAW
import os
import pandas as pd
from julia.api import Julia
from julia import Main
from convert_to_Matpower_files import write_matpower_case
from PM_solver import run_powermodels_opf
from PW_update import update_powerworld_from_json
from gen_mapping import create_gen_mapping


# Initialize counter
count = 0
    # === Set file paths ===
pwb_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Test_Cases\Texas2K_ScenarioA.PWB" #change case to run here
output_m_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\Test_CaseH.m" #change where .m file is saved here
json_output_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\opf_results1.json" # change where .json is saved here
gen_map_file_path =r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\gen_map.json"
Branch_data_file_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\branch_data.csv"
bus_data_file_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\bus_data.csv"
gen_data_file_path = r"C:\Users\natep\Documents\Classes\Op_research\Spring_2025\Result Data\gen_data.csv"

print("Connecting to PowerWorld and opening case...")
pw = SAW(pwb_path)

#Make function that can create a gen_mapping
print("Making generator map")
gen_mapping = create_gen_mapping(pw, gen_map_file_path)

# Define Julia binary path
julia_bindir = r"C:\Users\Owner\AppData\Local\Programs\Julia-1.11.4\bin"
os.environ['JULIA_BINDIR'] = julia_bindir
julia = Julia(compiled_modules=False)

# --- BRANCH DATA ---
# Attributes: "BusNum", "BusNum:1", "LineR", "LineX", "LineB", "LineMVA", "LineStatus"
branch_fields = ["BusNum", "BusNum:1", "LineCircuit", "LineStatus", "LineR", "LineX", 
                    "LineAMVA", "LineAMVA:1", "LineAMVA:2", "LineMW", "LineMVR", "LineMVA"]
branch_data = pw.GetParametersMultipleElement("Branch", branch_fields)
branch_df = pd.DataFrame(branch_data)
# Save to CSV
branch_df.to_csv(Branch_data_file_path, index=False)
print("Branch data saved")

BaseMVA = 100

while count < 3:  # change this to howerver many iterations you want it to solve through
    print("Loop Restarting")
    count += 1
    print("Solving Powerflow in Powerworld")
    pw.SolvePowerFlow()
    pw.SaveCase(pwb_path)
    
    # --- BUS DATA ---
    # Attributes: "BusNum", "BusNomVolt", "BusPUVolt", "BusAngle"
    bus_fields = ["BusNum", "BusNomVolt", "BusPUVolt", "BusAngle"]
    bus_data = pw.GetParametersMultipleElement("Bus", bus_fields)
    bus_df = pd.DataFrame(bus_data)
    #print("\nBus Data:")
    #print(bus_df)
    # --- GENERATOR DATA ---
    # Attributes: "BusNum", "GenID", "GenMW", "GenMVR"
    gen_fields = ["BusNum", "GenID", "GenMW", "GenMVR"]
    gen_data = pw.GetParametersMultipleElement("Gen", gen_fields)
    gen_df = pd.DataFrame(gen_data)
    #print("\nGenerator Data:")
    #print(gen_df)

    # --- LOAD DATA ---
    # Attributes: "BusNum", "LoadID", "LoadMW", "LoadMVR"
    load_fields = ["BusNum", "LoadID", "LoadMW", "LoadMVR"]
    load_data = pw.GetParametersMultipleElement("Load", load_fields)
    load_df = pd.DataFrame(load_data)



    write_matpower_case(output_m_path, BaseMVA, bus_df, gen_df, load_df, branch_df) 
    #this function generates a .m file after you solve the powerworld case
    print(f"MATPOWER case file written to {output_m_path}")

    #This function runs Powermodels opf solution then creates a json with result data
    run_powermodels_opf(output_m_path, json_output_path)

    #function that places data into powerworld then saves it to the powerworld case
    update_powerworld_from_json(pwb_path, json_output_path, gen_mapping)

print("Saving final bus, branch, and generator data")
# --- Bus Data ---
bus_data = pw.GetParametersMultipleElement("Bus", bus_fields)
bus_df = pd.DataFrame(bus_data, columns=bus_fields)
bus_df.to_csv(bus_data_file_path, index=False)
print("Bus data saved")

# --- Generator Data ---
gen_data = pw.GetParametersMultipleElement("Gen", gen_fields)
gen_df = pd.DataFrame(gen_data, columns=gen_fields)
gen_df.to_csv(gen_data_file_path, index=False)
print("Gen data saved")

# --- Branch Data ---
branch_fields = ["BusNum", "BusNum:1", "LineCircuit", "LineStatus", "LineR", "LineX", 
                    "LineAMVA", "LineAMVA:1", "LineAMVA:2", "LineMW", "LineMVR", "LineMVA"]
branch_data = pw.GetParametersMultipleElement("Branch", branch_fields)
branch_df = pd.DataFrame(branch_data)
# Save to CSV
branch_df.to_csv(Branch_data_file_path, index=False)
print("Branch data saved")


