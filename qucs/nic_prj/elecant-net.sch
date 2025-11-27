<QucsStudio Schematic 0.0.19>
<Properties>
View=20,-183,761,178,2.08227,0,0
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
.ID -20 14 ELECANT "1=L1=1e-6=Inductor1" "1=L2=1e-12=Inductor2" "1=C1=1e-12=Capacitor1" "1=C2=1e-12=Capacitor2" "1=R1=10=Rrad"
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
Port P2 5 170 130 -110 -43 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
Port P3 5 170 -130 -101 13 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
R R1 5 280 -170 -26 15 0 0 "9e9" 0 "26.85" 0 "0" 0 "0" 0 "26.85" 0 "US" 0 "SMD0603" 0
Eqn Eqn1 1 540 -100 0 8 0 0 "L1V=L1*1e-6=" 1 "L2V=L2*1e-6=" 1 "C1V=C1*1e-12=" 1 "C2V=C2*1e-12=" 1 "yes" 0
L L1 5 200 -130 -28 25 0 2 "L1V" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
C C1 5 280 -130 -29 27 0 2 "C1V" 1 "0" 0 "0" 0 "neutral" 0 "SMD0603" 0
L L2 5 330 -10 -87 -16 0 1 "L2V" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
C C2 5 390 -10 -29 41 0 1 "C2V" 1 "0" 0 "0" 0 "neutral" 0 "SMD0603" 0
R R2 5 450 -10 14 -14 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0 "SMD0603" 0
</Components>
<Wires>
330 -130 330 -40 "" 0 0 0 ""
330 20 330 130 "" 0 0 0 ""
330 -130 390 -130 "" 0 0 0 ""
330 130 390 130 "" 0 0 0 ""
170 130 330 130 "" 0 0 0 ""
230 -130 250 -130 "" 0 0 0 ""
310 -130 330 -130 "" 0 0 0 ""
390 -130 390 -40 "" 0 0 0 ""
390 20 390 130 "" 0 0 0 ""
390 -130 450 -130 "" 0 0 0 ""
390 130 450 130 "" 0 0 0 ""
450 20 450 130 "" 0 0 0 ""
450 -130 450 -40 "" 0 0 0 ""
310 -170 310 -130 "" 0 0 0 ""
250 -170 250 -130 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
