Overview
This project automates a closed-loop workflow between PowerWorld Simulator and Julia/PowerModels:

Open and solve a PowerWorld case (power flow).
Export the solved state to a MATPOWER-format .m file.
Run an AC OPF in Julia using PowerModels on that .m file.
Push the OPF results (e.g., generator dispatch) back into the PowerWorld case.
Repeat for a specified number of iterations.
Save final bus, branch, and generator data to CSV.
The provided main script coordinates these steps using helper modules included in the zip:

convert_to_Matpower_files.py: Creates a MATPOWER case (.m) from PowerWorld data.
PM_solver.py: Calls Julia/PowerModels to solve an OPF and writes a JSON results file.
PW_update.py: Updates the PowerWorld case from the OPF results JSON.
gen_mapping.py: Creates a generator mapping between PowerWorld and MATPOWER/PowerModels.
What’s in the zip

To use this code:
OS: Windows 10/11 (PowerWorld SimAuto is Windows-only).
PowerWorld Simulator with SimAuto (COM) licensed and installed.
SimAuto must be registered and accessible to Python via COM.
PowerWorld and Python should be the same “bitness” (both 64-bit recommended).
Python: 3.9–3.12.
Julia: 1.11.4 

Python packages:
pandas
julia (PyJulia)
esa (a SimAuto wrapper exposing SAW class)
The script uses from esa import SAW. Ensure you have a package providing SAW (SimAuto Wrapper). 
This may be an internal/company package or an open-source ESA that wraps SimAuto. 
If you don’t already have it, install your organization’s SimAuto wrapper or consult your PowerWorld automation library provider.

Typical Python setup
Option A: Using pip
python -m venv .venv
.venv\Scripts\activate
pip install pandas julia
Install your SAW/ESA package. If available on PyPI: pip install <your-esa-package-name>. If not, install from its source (e.g., pip install -e path\to\esa).
First-time PyJulia setup (recommended):
python -c "import julia; julia.install()"
Option B: requirements.txt
If a requirements.txt is included, run:
pip install -r requirements.txt
Then run: python -c "import julia; julia.install()"
Julia packages
Open a Julia REPL and install required packages:

Press ] to enter Pkg mode, then:
add PowerModels
add Ipopt
add JSON
add JuMP
Notes:

PowerModels uses MATPOWER parsing internally, so MATLAB/MATPOWER is not required.
Ipopt will be your nonlinear solver for AC OPF. You may need to accept artifact downloads the first time.
PowerWorld SimAuto setup

Ensure SimAuto is installed and registered. From the PowerWorld installation folder, you can register SimAuto (consult PowerWorld documentation).
Confirm that you can automate PowerWorld from Python using your ESA/SAW library.
Close any open PowerWorld GUI instances or ensure SimAuto can open and save the same .pwb file without conflicts.
Unzip and configure file paths

Unzip the project to a working directory you have read/write access to (not Program Files).
Open main.py in a text editor.
Edit the configuration variables near the top:
pwb_path: Full path to your .pwb case file to run.
output_m_path: Where to write the MATPOWER .m file.
json_output_path: Where to write the OPF results JSON.
gen_map_file_path: Where to write the generator mapping JSON.
Branch_data_file_path, bus_data_file_path, gen_data_file_path: Where to save CSV outputs.
BaseMVA: Base MVA used in the MATPOWER case (100 by default).
julia_bindir: The full path to your Julia bin folder (e.g., C:\Users\YourName\AppData\Local\Programs\Julia-1.11.4\bin).
Tips:

Use raw strings r"..." or double backslashes in Windows paths.
Ensure the directories exist before running.
The script overwrites the .pwb case with updates each iteration (pw.SaveCase(pwb_path)). If you want to preserve the original, copy it first and point pwb_path to the copy.
What the script does

Connects to PowerWorld via SAW and opens the specified .pwb case.
Creates a generator mapping (PowerWorld bus/gen IDs to MATPOWER generator indices) and saves it to gen_map.json.
Saves initial branch data to CSV.
Iterates count times (default 2):
Solves a power flow in PowerWorld.
Exports bus, gen, and load data from PowerWorld.
Writes a MATPOWER .m case (write_matpower_case).
Runs OPF via Julia/PowerModels (run_powermodels_opf) and writes a JSON of results.
Updates the PowerWorld case using the JSON (update_powerworld_from_json).
After the loop, exports final bus, gen, and branch data to CSV.
How to run

Open a terminal in the project folder.
Activate your virtual environment if you created one (e.g., .venv\Scripts\activate).
Run:
python main.py
Watch the console for:
Connecting to PowerWorld and opening case...
Making generator map
Loop Restarting
Solving Powerflow in Powerworld
MATPOWER case file written to ...
OPF JSON written to ...
Updated PowerWorld from JSON
Saving final bus, branch, and generator data
Outputs you should see

The PowerWorld .pwb case updated with OPF dispatches (saved in place).
A MATPOWER case file (.m) at output_m_path.
An OPF results JSON at json_output_path.
A gen_map.json mapping file.
CSVs:
branch_data.csv (initial snapshot and again at end)
bus_data.csv (final)
gen_data.csv (final)
Customizing the loop count

The script uses while count < 2: for two iterations. Increase or decrease 2 as needed, or replace with a for-loop for clarity.
Common issues and troubleshooting

Cannot import esa or SAW:
Ensure you have the correct ESA/SAW library that wraps PowerWorld SimAuto. This is often organization-specific. Install or add it to PYTHONPATH.
SimAuto/COM errors (e.g., CLSID not registered, access denied):
Register SimAuto properly.
Match 64-bit PowerWorld with 64-bit Python.
Run the terminal “as Administrator” if needed to test, then adjust permissions.
Julia not found or JULIA_BINDIR incorrect:
Update julia_bindir to your installed Julia path (...\Julia-1.11.x\bin).
Ensure os.environ['JULIA_BINDIR'] is set before from julia.api import Julia.
Run python -c "import julia; julia.install()" once.
PowerModels/Ipopt not installed:
In Julia: ] add PowerModels Ipopt JSON JuMP
Permission/file path issues:
Ensure output directories exist and you have write permissions.
Avoid OneDrive-protected or restricted folders if you see path/locking errors.
Case locking:
Close PowerWorld GUI if it is holding a lock on the .pwb file. Let SimAuto handle opening/saving.
Best practices

Keep a backup of your original .pwb case. The script saves updates to the same file path.
Use a dedicated output directory for .m, .json, and .csv artifacts.
Version control your Python modules (convert_to_Matpower_files.py, etc.) so changes are tracked.
Log outputs for reproducibility.
Support matrix and assumptions

Windows only (due to SimAuto).
Requires a valid PowerWorld Simulator license with SimAuto.
Uses AC OPF via PowerModels + Ipopt. Solver settings can be customized in PM_solver.py if needed (e.g., tolerances, solver choice).

This workflow integrates proprietary software (PowerWorld) via SimAuto; ensure you comply with your license agreements.
The helper modules are provided as-is. Document any institutional or third-party licenses that apply within your organization.
Quick checklist before first run

PowerWorld + SimAuto installed and registered.
Python env with pandas, julia, and your ESA/SAW package.
PyJulia installed and initialized (python -c "import julia; julia.install()").
Julia installed; packages PowerModels, Ipopt, JSON, JuMP added.
Paths in main.py updated for your machine (pwb_path, output paths, julia_bindir).
Output directories created.