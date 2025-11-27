<QucsStudio Schematic 3.3.2>
<Properties>
View=16,34,1050,890,1,0,0
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.sch
OpenDisplay=1
showFrame=0
FrameText0=Titel
FrameText1=Gezeichnet von:
FrameText2=Datum:
FrameText3=Revision:
</Properties>
<Symbol>
</Symbol>
<Components>
GND * 1 200 230 0 0 0 0
Vdc V1 1 380 120 18 -26 0 0 "5V" 1 "battery" 0 "SIL-2" 0
GND * 1 380 150 0 0 0 0
IProbe Idd 1 320 90 -9 16 1 2
_MOSFET T1 1 200 120 10 -20 1 0 "pfet" 0 "-1.6" 0 "4.87e-3" 0 "1.98" 0 "0.75" 0 "1.25e-3" 0 "0.84" 0 "0.84" 0 "0.5" 0 "65f" 0 "1" 0 "0.0001" 0 "T1_L" 1 "0" 0 "1e-07" 0 "50.7n" 0 "42.2n" 0 "69.5n" 0 "46.6p" 0 "55.9p" 0 "0.8" 0 "0.46" 0 "0.5" 0 "0" 0 "0.33" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "1" 0 "1" 0 "26.85" 0 "26.85" 0 "1.11" 0 "7.02e-4" 0 "1108.0" 0 "SOT23" 0
_MOSFET T2 1 200 200 8 -26 0 0 "nfet" 0 "1" 0 "6.37e-3" 0 "1.24" 0 "0.75" 0 "625u" 0 "0.14" 0 "0.14" 0 "0.5" 0 "85 fA" 0 "1" 0 "0.0001" 0 "T2_L" 1 "0" 0 "1e-07" 0 "36n" 0 "30n" 0 "124n" 0 "19.8 pF" 0 "23.7 pF" 0 "0.8" 0 "0.46" 0 "0.5" 0 "0" 0 "0.33" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "1" 0 "1" 0 "26.85" 0 "26.85" 0 "1.11" 0 "7.02e-4" 0 "1108.0" 0 "SOT23" 0
.DC DC1 1 450 60 0 37 0 0 "0.001" 0 "1 nA" 0 "500" 0 "none" 0
GND * 1 60 220 0 0 0 0
Vdc V2 1 60 190 18 -26 0 0 "Vin" 1 "battery" 0 "SIL-2" 0
Eqn Eqn1 1 460 257 0 8 0 0 "switch=abs(xvalue(output.V, 2.5) - 2.5)=" 1 "current=abs(max(Idd.I) - 1e-3)=" 1 "yes" 0
.SW SW1 1 620 60 0 61 0 0 "DC1" 1 "Vin" 1 "lin" 1 "0" 1 "5" 1 "101" 1
.Opt Opt1 1 750 60 0 37 0 0 "SW1" 1 "1|1000|1e-5|0.05|1|7" 0 "Var=T1_L|yes|0.0001|5e-5|1e-3|linear" 0 "Var=T2_L|yes|0.0001|5e-5|1e-3|linear" 0 "Goal=switch|MIN|1|yes" 0 "Goal=current|MIN|100|yes" 0
</Components>
<Wires>
200 90 290 90 "" 0 0 0 ""
200 150 200 170 "output" 290 180 13 ""
170 120 170 160 "" 0 0 0 ""
350 90 380 90 "" 0 0 0 ""
170 160 170 200 "" 0 0 0 ""
60 160 170 160 "input" 90 110 85 ""
</Wires>
<Diagrams>
<Tab 580 570 350 50 71 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"xvalue(output.V, 2.5)" "" #0000ff 0 3 1 0 0 0 "">
	<"max(Idd.I)" "" #0000ff 0 3 1 0 0 0 "">
</Tab>
<Rect 100 570 410 220 31 #c0c0c0 1 00 1 0 0 0 1 0 0 0 1 0 0 0 315 0 225 "" "" "">
	<Legend 10 -100 0>
	<"input.V" "" #0000ff 0 3 0 0 0 0 "">
	<"output.V" "" #ff0000 0 3 0 0 0 0 "">
	<"Idd.I" "" #00ff00 0 3 0 0 1 0 "">
	  <Mkr 2.5 20 -270 3 1 0 0 0 50>
</Rect>
<Tab 660 640 270 50 71 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"T1_L.opt" "" #0000ff 0 3 1 0 0 0 "">
	<"T2_L.opt" "" #0000ff 0 3 1 0 0 0 "">
</Tab>
</Diagrams>
<Paintings>
Text 590 360 14 #000000 0 "Another famous example: CMOS inverter \n Optimize channel length to get \n 1) switchung at half of the supply voltage \n 2) a maximum switching current of 1mA"
Arrow 700 460 0 50 20 8 #000000 2 1 0
Arrow 610 150 -120 -40 20 8 #ff0000 2 1 0
Arrow 740 130 -80 0 20 8 #ff0000 2 1 0
Text 586 591 14 #000000 0 "Result:"
</Paintings>
