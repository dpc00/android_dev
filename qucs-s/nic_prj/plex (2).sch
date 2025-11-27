<QucsStudio Schematic 0.0.19>
<Properties>
View=206,95,898,657,1.57594,0,27
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
.ID -20 44 PLEX "1=SS=0=Series/Shunt Select"
Line -20 -40 40 0 #000080 2 1
Line -20 40 40 0 #000080 2 1
Line -20 -40 0 80 #000080 2 1
Line 20 -30 10 0 #000080 2 1
Line -30 30 10 0 #000080 2 1
Line 30 30 -10 0 #000000 0 1
Line 20 -40 0 80 #000080 2 1
Line 20 20 0 -40 #000000 0 1
Line 20 30 10 0 #000080 2 1
.PortSym 30 -30 3 180
.PortSym 30 30 2 180
.PortSym -30 30 1 0
</Symbol>
<Components>
GND * 1 280 560 0 0 0 0
GND * 1 340 350 0 0 0 0
Port A 1 400 370 -8 37 0 1 "1" 0 "analog" 0 "TESTPOINT" 0
GND * 1 540 350 0 0 0 1
Port C 1 400 270 -10 -65 0 3 "3" 0 "analog" 0 "TESTPOINT" 0
GND * 1 640 170 0 0 0 1
GND * 1 540 230 0 0 0 3
Inv Y1 5 470 440 27 -26 0 1 "1 V" 0 "0" 0 "old" 0 "old" 0
Vdc V1 5 280 530 25 -9 0 0 "SS" 1 "battery" 0 "SIL-2" 0
Port B 1 630 370 -8 39 0 1 "2" 0 "analog" 0 "TESTPOINT" 0
Relais S5 5 520 320 -26 -49 0 1 "0.5 V" 0 "0" 0 "0" 0 "1e12" 0 "26.85" 0 "TRANSF-MICRO" 0
Relais S4 5 590 200 -26 49 1 3 "0.5 V" 0 "0" 0 "0" 0 "1e12" 0 "26.85" 0 "TRANSF-MICRO" 0
Relais S1 5 370 320 49 -26 0 0 "0.5 V" 0 "0" 0 "0" 0 "1e12" 0 "26.85" 0 "TRANSF-MICRO" 0
</Components>
<Wires>
470 350 470 410 "" 0 0 0 ""
400 350 400 370 "" 0 0 0 ""
400 290 490 290 "" 0 0 0 ""
550 290 630 290 "" 0 0 0 ""
540 350 550 350 "" 0 0 0 ""
470 350 490 350 "" 0 0 0 ""
400 270 400 290 "" 0 0 0 ""
280 480 280 500 "" 0 0 0 ""
280 480 470 480 "" 0 0 0 ""
470 470 470 480 "" 0 0 0 ""
620 170 640 170 "" 0 0 0 ""
630 230 630 290 "" 0 0 0 ""
620 230 630 230 "" 0 0 0 ""
340 170 340 270 "" 0 0 0 ""
340 170 560 170 "" 0 0 0 ""
540 230 560 230 "" 0 0 0 ""
280 270 280 480 "" 0 0 0 ""
340 270 340 290 "" 0 0 0 ""
280 270 340 270 "" 0 0 0 ""
630 290 630 370 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
