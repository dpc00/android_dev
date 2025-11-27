<QucsStudio Schematic 0.0.19>
<Properties>
View=51,-223,638,178,2.16865,0,14
Grid=10,10,1
DataSet=aa-network.dat
DataDisplay=aa-network.dpl
OpenDisplay=1
showFrame=0
FrameText0=Title
FrameText1=Drawn By:
FrameText2=Date:
FrameText3=Revision:
</Properties>
<Symbol>
Line -20 -10 40 0 #000080 2 1
Line 20 -10 0 20 #000080 2 1
Line -30 0 10 0 #000080 2 1
Line 20 0 10 0 #000080 2 1
Line -20 -10 0 20 #000080 2 1
.PortSym 30 0 2 180
.PortSym -30 0 1 0
Line -20 10 40 0 #000080 2 1
.ID -50 34 SERLC "1=L1=1e-6=Inductor1" "1=C1=1e-12=Capacitor1" "1=R1=1=Resistor1"
</Symbol>
<Components>
Port P1 5 160 -130 -69 -43 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Port P2 5 160 130 -61 -41 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
R R1 5 250 90 -77 -29 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0 "SMD0603" 0
Eqn Eqn1 0 350 -90 0 8 0 0 "L1=1=" 1 "C1=1=" 1 "R1=1=" 1 "yes" 0
R R2 5 280 120 -26 -15 0 2 "1E12 Ω" 0 "26.85" 0 "0" 0 "0" 0 "26.85" 0 "US" 0 "SMD0603" 0
GND * 1 310 120 0 0 0 0
Sub IND1 5 250 0 -89 -24 0 1 "inductor.sch" 0 "L1" 1
Sub CAP1 5 250 -90 -90 -22 0 1 "capacitor.sch" 0 "C1" 1
</Components>
<Wires>
250 -130 250 -120 "" 0 0 0 ""
250 -60 250 -30 "" 0 0 0 ""
250 30 250 60 "" 0 0 0 ""
160 -130 250 -130 "" 0 0 0 ""
250 120 250 130 "" 0 0 0 ""
160 130 250 130 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
