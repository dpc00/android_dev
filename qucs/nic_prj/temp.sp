* EQUIVALENT CIRCUIT FOR VECTOR FITTED S-MATRIX
* Created using scikit-rf vectorFitting.py
*
.SUBCKT s_equivalent p1 
*
* port 1
R1 a1 0 50.0
V1 p1 a1 0
H1 nt1 nts1 V1 50.0
E1 nts1 0 p1 0 1
* transfer network for s11
F11 0 a1 V11 0.02
F11_inv a1 0 V11_inv 0.02
V11 nt1 nt11 0
V11_inv nt1 nt11_inv 0
* transfer admittances for S11
R11 nt11_inv 0 1.060
X1 nt11 0 rl_admittance res=474.214m ind=856.918p
X2 nt11_inv 0 rcl_vccs_admittance res=1.048 cap=384.642p ind=44.385n gm=66.566m mult=1
X3 nt11_inv 0 rcl_vccs_admittance res=1.989 cap=1.086n ind=85.817n gm=39.792m mult=1
X4 nt11_inv 0 rl_admittance res=498.122m ind=71.126n
.ENDS s_equivalent
*
.SUBCKT rcl_vccs_admittance n_pos n_neg res=1k cap=1n ind=100p gm=1m mult=1
L1 n_pos 1 {ind}
C1 1 2 {cap}
R1 2 n_neg {res}
G1 n_pos n_neg 1 2 {gm} m={mult}
.ENDS rcl_admittance
*
.SUBCKT rl_admittance n_pos n_neg res=1k ind=100p
L1 n_pos 1 {ind}
R1 1 n_neg {res}
.ENDS rl_admittance
