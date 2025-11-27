<QucsStudio Schematic 3.3.2>
<Properties>
View=63,-219,593,209,2.02804,0,13
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
.ID -20 14 IND "1=V1=1=Value"
Line -20 -10 40 0 #000080 2 1
Line 20 -10 0 20 #000080 2 1
Line -20 10 40 0 #000080 2 1
Line -20 -10 0 20 #000080 2 1
Line -30 0 10 0 #000080 2 1
Line 20 0 10 0 #000080 2 1
.PortSym -30 0 1 0
.PortSym 30 0 2 180
</Symbol>
<Components>
Eqn Eqn1 5 410 -110 -47 20 0 0 "L1=V1*1e-6=" 1 "yes" 0
Port P2 5 160 20 -49 -48 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
Port P1 5 160 -130 -54 22 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
L L1 5 250 -60 12 -15 0 1 "L1" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
Eqn Eqn2 0 410 0 0 8 0 0 "V1=1=" 1 "yes" 0
GND * 0 250 20 0 0 0 1
</Components>
<Wires>
160 -130 250 -130 "" 0 0 0 ""
250 -130 250 -90 "" 0 0 0 ""
250 -30 250 20 "" 0 0 0 ""
160 20 250 20 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
