<QucsStudio Schematic 0.0.19>
<Properties>
View=213,-178,941,410,1.99483,0,0
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
.ID -20 14 MAGANT "1=L1=1e-6=Inductor1" "1=L2=1e-6=Inductor2" "1=C1=1e-12=Capacitor1" "1=C2=1e-12=Capacitor2" "1=R1=10=Rrad1"
.PortSym -30 0 1 0
.PortSym 30 0 2 0
Line -20 -10 40 0 #000080 2 1
Line 20 -10 0 20 #000080 2 1
Line -20 10 40 0 #000080 2 1
Line -20 -10 0 20 #000080 2 1
Line -30 0 10 0 #000080 2 1
Line 20 0 10 0 #000080 2 1
</Symbol>
<Components>
Port P3 5 280 -130 -60 17 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Port P2 5 280 130 -59 -49 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
L L1 5 350 -40 -23 -86 0 1 "L1V" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
L L2 5 510 -90 -19 -13 0 3 "L2V" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
C C2 5 510 0 -22 -39 0 3 "C2V" 1 "1e-12" 0 "0" 0 "neutral" 0 "SMD0603" 0
C C1 5 430 10 -26 -62 0 1 "C1V" 1 "1e-12" 0 "0" 0 "neutral" 0 "SMD0603" 0
Eqn Eqn1 1 600 -100 0 8 0 0 "L1V=L1*1e-6=" 1 "L2V=L2*1e-6=" 1 "C1V=C1*1e-12=" 1 "C2V=C2*1e-12=" 1 "yes" 0
R R2 5 510 80 -24 -50 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0 "SMD0603" 0
</Components>
<Wires>
280 -130 350 -130 "" 0 0 0 ""
280 130 350 130 "" 0 0 0 ""
350 130 430 130 "" 0 0 0 ""
350 -130 430 -130 "" 0 0 0 ""
350 -130 350 -70 "" 0 0 0 ""
510 110 510 130 "" 0 0 0 ""
510 30 510 50 "" 0 0 0 ""
510 -130 510 -120 "" 0 0 0 ""
510 -60 510 -30 "" 0 0 0 ""
430 130 510 130 "" 0 0 0 ""
430 -130 510 -130 "" 0 0 0 ""
430 -130 430 -20 "" 0 0 0 ""
430 40 430 130 "" 0 0 0 ""
350 -10 350 130 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
