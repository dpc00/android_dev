<QucsStudio Schematic 3.3.2>
<Properties>
View=203,-200,1038,453,1.66604,0,232
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
.PortSym -30 0 1 0
Line -20 -10 40 0 #000080 2 1
Line -20 -10 0 20 #000080 2 1
Line -30 0 10 0 #000080 2 1
.PortSym 30 0 2 180
Line 20 -10 0 20 #000080 2 1
Line 20 0 10 0 #000080 2 1
Line -20 10 40 0 #000080 2 1
.ID -50 34 PARLC "1=L1=1e-6=Inductor1" "1=C1=1e-12=Capacitor1" "1=R1=1=Resistor1"
</Symbol>
<Components>
Port P2 5 310 250 -67 13 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
R R1 1 380 210 30 -27 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0 "SMD0603" 0
Sub IND1 1 380 90 -97 -27 0 1 "inductor.sch" 0 "L1" 1
Port P1 5 320 0 -67 17 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Sub CAP1 1 500 90 37 -31 0 1 "capacitor.sch" 0 "C1" 1
</Components>
<Wires>
310 250 380 250 "" 0 0 0 ""
380 240 380 250 "" 0 0 0 ""
380 120 380 180 "" 0 0 0 ""
380 0 380 60 "" 0 0 0 ""
320 0 380 0 "" 0 0 0 ""
380 0 500 0 "" 0 0 0 ""
380 250 500 250 "" 0 0 0 ""
500 120 500 250 "" 0 0 0 ""
500 0 500 60 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
