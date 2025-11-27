<QucsStudio Schematic 0.0.19>
<Properties>
View=99,210,946,547,1.50379,0,0
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.dpl
OpenDisplay=1
showFrame=0
FrameText0=Title
FrameText1=Drawn By:
FrameText2=Date:
FrameText3=Revision:
</Properties>
<Symbol>
.ID -20 44 NIC "1=FBr=200 Ohm=Resistors"
.PortSym -30 -30 1 0
.PortSym 30 -30 2 0
.PortSym -30 30 3 0
.PortSym 30 30 4 0
Line -20 -40 40 0 #000080 2 1
Line 20 -40 0 80 #000080 2 1
Line -20 40 40 0 #000080 2 1
Line -20 -40 0 80 #000080 2 1
Line -30 -30 10 0 #000080 2 1
Line 20 -30 10 0 #000080 2 1
Line -30 30 10 0 #000080 2 1
Line 20 30 10 0 #000080 2 1
</Symbol>
<Components>
OpAmp OP3 1 270 320 -31 -95 0 1 "1e6" 1 "15 V" 0
OpAmp OP4 1 740 320 -31 -99 1 1 "1e6" 1 "15 V" 0
Port P1 1 150 380 -23 12 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Port P2 1 840 380 -32 14 0 2 "2" 1 "analog" 0 "TESTPOINT" 0
Port P3 1 340 380 11 17 0 2 "3" 1 "analog" 0 "TESTPOINT" 0
Port P4 1 650 380 -23 12 0 0 "4" 1 "analog" 0 "TESTPOINT" 0
R R2 1 340 320 15 -26 0 1 "FBr" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
R R1 1 150 320 15 -26 0 1 "FBr" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
R R4 1 840 310 26 -38 1 1 "FBr" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
R R3 1 640 310 -88 -26 1 1 "FBr" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
</Components>
<Wires>
250 350 250 380 "" 0 0 0 ""
150 380 250 380 "" 0 0 0 ""
290 350 290 380 "" 0 0 0 ""
290 380 340 380 "" 0 0 0 ""
720 350 720 380 "" 0 0 0 ""
760 350 760 380 "" 0 0 0 ""
760 380 840 380 "" 0 0 0 ""
740 250 740 280 "" 0 0 0 ""
650 380 720 380 "" 0 0 0 ""
270 250 270 280 "" 0 0 0 ""
270 250 340 250 "" 0 0 0 ""
340 250 340 290 "" 0 0 0 ""
340 350 340 380 "" 0 0 0 ""
150 250 270 250 "" 0 0 0 ""
150 250 150 290 "" 0 0 0 ""
150 350 150 380 "" 0 0 0 ""
740 250 840 250 "" 0 0 0 ""
840 250 840 280 "" 0 0 0 ""
840 340 840 380 "" 0 0 0 ""
640 250 740 250 "" 0 0 0 ""
640 250 640 280 "" 0 0 0 ""
640 340 650 340 "" 0 0 0 ""
650 340 650 380 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
