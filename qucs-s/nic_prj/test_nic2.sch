<QucsStudio Schematic 0.0.19>
<Properties>
View=-255,-162,1374,993,0.668398,0,27
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.dpl
OpenDisplay=0
showFrame=0
FrameText0=Title
FrameText1=Drawn By:
FrameText2=Date:
FrameText3=Revision:
</Properties>
<Symbol>
.ID -20 14 SUB
Line -20 -10 40 0 #000080 2 1
Line 20 -10 0 20 #000080 2 1
Line -20 10 40 0 #000080 2 1
Line -20 -10 0 20 #000080 2 1
</Symbol>
<Components>
GND * 1 10 0 0 0 0 3
GND * 1 660 0 0 0 0 1
SPfile X1 5 500 0 -26 -21 0 0 "C:/projects/sNp/temp.s2p" 0 "2" 0 "polar" 0 "linear" 0 "short" 0 "none" 0 "block" 0 "SOT23" 0
GND * 1 500 40 0 0 0 0
GND * 1 340 60 0 0 0 0
GND * 1 150 60 0 0 0 0
L L1 5 250 0 -29 -49 0 0 "L1" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C1 5 150 30 19 0 0 1 "C1" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
C C2 5 340 30 22 2 0 1 "C2" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
Pac P1 1 40 0 -33 -118 0 3 "1" 1 "50" 1 "-40 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
Pac P2 1 590 0 -26 -122 0 1 "2" 1 "0" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
Eqn Eqn1 5 920 300 0 8 0 0 "VSWR=(1+abs(S[1,1]))/(1-abs(S[1,1]))=" 1 "OG=min(VSWR)=" 1 "Z0=50=" 1 "yes" 0
Eqn Eqn3 1 860 -30 0 8 0 0 "y=1=" 1 "yes" 0
.SP SP1 5 540 100 0 87 0 0 "lin" 0 "F1" 0 "F2" 0 "60" 0 "no" 0 "1" 0 "2" 0 "none" 0
Eqn Eqn2 5 860 110 0 8 0 0 "BW=1e3=" 1 "Fc=18e+06=" 1 "F1=Fc-BW=" 1 "F2=Fc+BW=" 1 "yes" 0
.Opt Opt1 5 540 230 0 50 0 0 "SP1" 0 "6|2000|0.95|0.8|50|7" 0 "Var=L1|yes|2.30312e-06|0|1e-3|linear" 0 "Var=C1|yes|3.34567e-10|0|1e-9|linear" 0 "Var=C2|yes|1.99469e-11|0|1e-9|linear" 0 "Var=Z0|no|50|1|9000|linear" 0 "Goal=OG|MIN|1|yes" 0
</Components>
<Wires>
500 30 500 40 "" 0 0 0 ""
620 0 660 0 "" 0 0 0 ""
530 0 560 0 "" 0 0 0 ""
70 0 150 0 "" 0 0 0 ""
280 0 340 0 "" 0 0 0 ""
150 0 220 0 "" 0 0 0 ""
340 0 470 0 "" 0 0 0 ""
</Wires>
<Diagrams>
<Tab -94 953 928 98 71 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"L1.opt" "" #0000ff 0 3 1 0 0 0 "">
	<"C1.opt" "" #0000ff 0 3 1 0 0 0 "">
	<"C2.opt" "" #0000ff 0 3 1 0 0 0 "">
	<"OG" "" #0000ff 0 3 1 0 0 0 "">
</Tab>
<Rect -112 703 529 439 31 #c0c0c0 1 00 1 1.7999e+07 200 1.8001e+07 1 -0.100517 0.2 1.10596 1 0 0 0 315 0 225 "" "" "">
	<Legend 10 -100 0>
	<"VSWR" "" #ff00ff 0 3 0 0 0 0 "">
	  <Mkr 1.8e+07 252 -523 3 1 0 0 0 50>
	<"S[1,1]" "" #ff0000 0 3 0 0 0 0 "">
	  <Mkr 1.7999e+07 112 -203 3 1 0 0 0 50>
</Rect>
</Diagrams>
<Paintings>
</Paintings>
