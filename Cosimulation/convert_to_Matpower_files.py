#this function generates a .m file after you solve the powerworld case

def write_matpower_case(filename, baseMVA, bus_df, gen_df, load_df, branch_df):
    with open(filename, 'w') as f:
        f.write("function mpc = Test_Case1\n")
        f.write("mpc.version = '2';\n")
        f.write(f"mpc.baseMVA = {baseMVA:.2f};\n\n")

        # Bus data
        f.write("%% bus data\n")
        f.write("mpc.bus = [\n")
        for i, row in enumerate(bus_df.itertuples(index=False)):
            bus_i = int(row.BusNum)
            Vbase = float(row.BusNomVolt)
            Vm = float(row.BusPUVolt)
            Va = float(row.BusAngle)

            Pd = load_df.loc[load_df["BusNum"] == bus_i, "LoadMW"].sum() if not load_df.empty else 0.0
            Qd = load_df.loc[load_df["BusNum"] == bus_i, "LoadMVR"].sum() if not load_df.empty else 0.0

            f.write(f"{bus_i}\t{'3' if i == 0 else '2'}\t{Pd:.2f}\t{Qd:.2f}\t0.00\t0.00\t1\t{Vm:.7f}\t{Va:.6f}\t{Vbase:.2f}\t1\t1.100\t0.900\n")
        f.write("];\n\n")

        # Generator data
        f.write("%% generator data\n")
        f.write("mpc.gen = [\n")
        for row in gen_df.itertuples(index=False):
            bus = int(row.BusNum)
            Pg = float(row.GenMW)
            Qg = float(row.GenMVR)
            f.write(f"{bus}\t{Pg:.2f}\t{Qg:.2f}\t9900\t-9900\t1.0000\t{baseMVA:.2f}\t1\t1000.00\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t10.0\n")
        f.write("];\n\n")

        # Generator cost data (placeholder)
        f.write("%% generator cost data\n")
        f.write("mpc.gencost = [\n")
        for _ in gen_df.itertuples(index=False):
            f.write("2\t0\t0\t4\t0\t0\t1\t0\n")
        f.write("];\n\n")

        # Branch data
            # Branch data
        f.write("%% branch data\n")
        f.write("mpc.branch = [\n")
        for _, row in branch_df.iterrows():
            fbus = int(row["BusNum"])
            tbus = int(row["BusNum:1"])
            r = float(row["LineR"])
            x = float(row["LineX"])
            b = float(row.get("LineB", 0.0))
            rateA = float(row.get("LineAMVA", 1000.0))
            status = 1 if row.get("LineStatus", "Closed") == "Closed" else 0
            line_mw = float(row.get("LineMW", 0.0))
            line_mvr = float(row.get("LineMVR", 0.0))
            line_mva = float(row.get("LineMVA", 0.0))
            f.write(f"{fbus}\t{tbus}\t{r:.6f}\t{x:.6f}\t{b:.6f}\t{rateA:.2f}\t{rateA:.2f}\t{rateA:.2f}\t0.0\t0.0\t{status}\t0.00\t0.00\t{line_mw:.2f}\t{line_mvr:.2f}\t{line_mva:.2f}\t{line_mvr:.2f}\n")
        f.write("];\n\n")

        # Bus names
        f.write("%% bus names\n")
        f.write("mpc.bus_name = {\n")
        for i, row in enumerate(bus_df.itertuples(index=False)):
            f.write(f"'Bus {int(row.BusNum)}';\n")
        f.write("};\n\n")

        # Generator unit types (placeholder)
        f.write("%% Generator Unit Types\n")
        f.write("mpc.gentype = {\n")
        for _ in gen_df.itertuples(index=False):
            f.write("'UN';\n")
        f.write("};\n\n")

        # Generator fuel types (placeholder)
        f.write("%% Generator Fuel Types\n")
        f.write("mpc.genfuel = {\n")
        for _ in gen_df.itertuples(index=False):
            f.write("'unknown';\n")
        f.write("};\n")