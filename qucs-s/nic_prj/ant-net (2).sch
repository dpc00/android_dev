<QucsStudio Schematic 0.0.19>
<Properties>
View=172,202,1276,796,1.28283,0,0
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
.PortSym -30 -30 1 0
Line -20 -40 40 0 #000080 2 1
Line -20 -40 0 20 #000080 2 1
Line -30 -30 10 0 #000080 2 1
Line 20 -30 10 0 #000080 2 1
Line -20 -20 40 0 #000080 2 1
Line 20 -40 0 20 #000080 2 1
.PortSym 30 -30 2 180
.ID -50 4 SPN "1=L1=1e-6=Coil" "1=C1=1e-12=Capacitor" "1=R1=1=Resistor"
</Symbol>
<Components>
Port P2 5 490 270 -30 -55 0 0 "2" 1 "analog" 0 "TESTPOINT" 0
Port P1 5 290 250 -29 -42 0 0 "1" 1 "analog" 0 "TESTPOINT" 0
Sub SERLC1 1 400 520 -40 26 0 0 "series-lc.sch" 0 "L1" 1 "C1" 1 "R1" 1
Switch S1 1 490 410 11 -26 0 1 "off" 0 "1 ms" 0 "0" 0 "1e12" 0 "26.85" 0 "SW_PUSH_SMALL" 0
Switch S2 1 880 410 11 -26 0 1 "on" 0 "1 ms" 0 "0" 0 "1e12" 0 "26.85" 0 "SW_PUSH_SMALL" 0
Sub PARLC1 1 770 520 -39 25 0 0 "parallel-lc.sch" 0 "L1" 1 "C1" 1 "R1" 1
</Components>
<Wires>
490 270 490 380 "" 0 0 0 ""
490 270 880 270 "" 0 0 0 ""
880 270 880 380 "" 0 0 0 ""
880 440 880 520 "" 0 0 0 ""
490 440 490 520 "" 0 0 0 ""
430 520 490 520 "" 0 0 0 ""
290 520 370 520 "" 0 0 0 ""
290 250 680 250 "" 0 0 0 ""
680 520 740 520 "" 0 0 0 ""
800 520 880 520 "" 0 0 0 ""
290 250 290 520 "" 0 0 0 ""
680 250 680 520 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
