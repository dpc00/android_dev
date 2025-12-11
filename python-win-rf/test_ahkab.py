import ahkab.netlist_parser as ahnp

cfn = r"C:\Qucs-S\spice4qucs\spice4qucs.cir"

if __name__ == "__main__":
    (c, d, p) = ahnp.parse_circuit(cfn)
    print(c)
    print(d)
    print(p)
