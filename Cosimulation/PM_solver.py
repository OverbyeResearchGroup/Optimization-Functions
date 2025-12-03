import json
import os
from julia.api import Julia
from julia import Main


#This function runs Powermodels opf solution then creates a json with result data
def run_powermodels_opf(m_file_path, json_output_path):
    """
    Run PowerModels OPF on a Matpower .m file, convert pg, qg, and pg_cost to MW, MVAr,
    and MW-based cost, and save a formatted JSON output.

    Parameters:
    - m_file_path (str): Path to the Matpower .m file.
    - json_output_path (str): Path to save the formatted JSON output.

    Returns:
    - bool: True if successful, False if an error occurs.
    """
    # Set Julia binary path
    os.environ['JULIA_BINDIR'] = r"C:\Users\Owner\AppData\Local\Programs\Julia-1.11.4\bin"
    
    # Initialize Julia
    julia = Julia(compiled_modules=False)
    
    # Verify input file exists
    if not os.path.exists(m_file_path):
        print(f"Matpower .m file not found at: {m_file_path}")
        return False
    
    # Assign Python variables to Julia's Main module
    Main.m_file_path = m_file_path
    Main.json_output_path = json_output_path
    
    # Run Julia code
    Main.eval("""
    using PowerModels
    using Ipopt
    using JSON

    # ------------------------------------------------------------------
    # 1. Load the MATPOWER case
    # ------------------------------------------------------------------
    data = PowerModels.parse_file(m_file_path)

    # ------------------------------------------------------------------
    # 2. LOCK ALL GENERATOR INJECTIONS (P & Q) to their current values
    # ------------------------------------------------------------------
    for (g_id, gen) in get(data, "gen", Dict())
        pg = gen["pg"]          # current active power (p.u.)
        qg = gen["qg"]          # current reactive power (p.u.)

        # Tight bounds: pmin = pmax = pg,  qmin = qmax = qg
        gen["pmin"] = pg
        gen["pmax"] = pg
        gen["qmin"] = qg
        gen["qmax"] = qg
    end

    # ------------------------------------------------------------------
    # 3. Solve a *pure* power-flow (no optimization)
    # ------------------------------------------------------------------
    #   run_pf  →  solves the nonlinear PF equations with the fixed injections
    #   ACPPowerModel → rectangular (current-voltage) formulation (most stable)
    result = solve_ac_pf(data, Ipopt.Optimizer;
                    setting = Dict{String,Any}("output" => Dict{String,Any}("branch_flows" => true)))

    # ------------------------------------------------------------------
    # 4. Export the solution (voltages, flows, etc.) – generator values
    #     are unchanged because they were never free variables
    # ------------------------------------------------------------------
    solution = result["solution"]

    # Base MVA (fallback to 100.0)
    baseMVA = haskey(data, "baseMVA") ? data["baseMVA"] : 100.0

    # Write JSON for downstream Python code
    open(json_output_path, "w") do f
        write(f, JSON.json(solution))
    end
    """)
    
    # Format the JSON output
    with open(json_output_path, 'r') as f:
        data = json.load(f)
    
    # Write formatted JSON
    with open(json_output_path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=False)
    
    # Print formatted JSON
    #print(json.dumps(data, indent=4, sort_keys=False))
    
    return True