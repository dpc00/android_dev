<QucsStudio Schematic 0.0.19>
<Properties>
View=203,-178,686,210,1.96392,0,0
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
.ID -20 14 CAP "1=V1=10=Value"
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
Eqn Eqn1 1 550 -110 -47 20 0 0 "C1=V1*1e-12=" 1 "yes" 0
Port P1 5 310 -130 -67 17 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Port P2 5 300 30 -67 13 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
C C1 5 390 -60 21 -15 0 1 "C1" 1 "1e-9" 0 "0" 0 "neutral" 0 "SMD0603" 0
</Components>
<Wires>
310 -130 390 -130 "" 0 0 0 ""
390 -130 390 -90 "" 0 0 0 ""
390 -30 390 30 "" 0 0 0 ""
300 30 390 30 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
