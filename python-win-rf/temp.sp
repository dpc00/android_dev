* EQUIVALENT CIRCUIT FOR VECTOR FITTED S-MATRIX
* Created using scikit-rf vectorFitting.py
*
.SUBCKT s_equivalent p1 p2 
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
R11 nt11_inv 0 4.769
X1 nt11 0 rl_admittance res=778.616m ind=929.190p
X2 nt11_inv 0 rcl_vccs_admittance res=1.625 cap=434.120p ind=41.934n gm=73.073m mult=1
X3 nt11_inv 0 rcl_vccs_admittance res=21.599 cap=32.797p ind=841.753n gm=11.064m mult=-1
X4 nt11_inv 0 rl_admittance res=985.043m ind=194.877n
* transfer network for s12
F12 0 a1 V12 0.02
F12_inv a1 0 V12_inv 0.02
V12 nt2 nt12 0
V12_inv nt2 nt12_inv 0
* transfer admittances for S12
R12 nt12 0 6.459
X5 nt12_inv 0 rl_admittance res=14.519 ind=17.327n
X6 nt12 0 rcl_vccs_admittance res=1.644 cap=429.029p ind=42.432n gm=110.548m mult=-1
X7 nt12_inv 0 rcl_vccs_admittance res=33.088 cap=21.409p ind=1.289u gm=21.307m mult=-1
X8 nt12 0 rl_admittance res=1.003 ind=198.425n
*
* port 2
R2 a2 0 50.0
V2 p2 a2 0
H2 nt2 nts2 V2 50.0
E2 nts2 0 p2 0 1
* transfer network for s21
F21 0 a2 V21 0.02
F21_inv a2 0 V21_inv 0.02
V21 nt1 nt21 0
V21_inv nt1 nt21_inv 0
* transfer admittances for S21
R21 nt21 0 6.459
X9 nt21_inv 0 rl_admittance res=14.519 ind=17.327n
X10 nt21 0 rcl_vccs_admittance res=1.644 cap=429.029p ind=42.432n gm=110.548m mult=-1
X11 nt21_inv 0 rcl_vccs_admittance res=33.088 cap=21.409p ind=1.289u gm=21.307m mult=-1
X12 nt21 0 rl_admittance res=1.003 ind=198.425n
* transfer network for s22
F22 0 a2 V22 0.02
F22_inv a2 0 V22_inv 0.02
V22 nt2 nt22 0
V22_inv nt2 nt22_inv 0
* transfer admittances for S22
R22 nt22_inv 0 4.769
X13 nt22 0 rl_admittance res=778.616m ind=929.190p
X14 nt22_inv 0 rcl_vccs_admittance res=1.625 cap=434.120p ind=41.934n gm=73.073m mult=1
X15 nt22_inv 0 rcl_vccs_admittance res=21.599 cap=32.797p ind=841.753n gm=11.064m mult=-1
X16 nt22_inv 0 rl_admittance res=985.043m ind=194.877n
.ENDS s_equivalent
*
.SUBCKT rcl_vccs_admittance n_pos n_neg res=1k cap=1n ind=100p gm=1m mult=1
L1 n_pos 1 {ind}
C1 1 2 {cap}
R1 2 n_neg {res}
G1 n_pos n_neg 1 2 {gm} m={mult}
.ENDS rcl_vccs_admittance
*
.SUBCKT rl_admittance n_pos n_neg res=1k ind=100p
L1 n_pos 1 {ind}
R1 1 n_neg {res}
.ENDS rl_admittance
