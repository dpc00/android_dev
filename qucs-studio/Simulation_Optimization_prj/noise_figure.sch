<QucsStudio Schematic 3.3.2>
<Properties>
View=-50,-54,940,885,1,0,65
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.dpl
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
Pac P1 1 -10 300 18 -26 0 0 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 -10 330 0 0 0 0
GND * 1 -10 210 0 0 0 0
Vdc V1 1 -10 180 18 -26 0 0 "5 V" 1 "SIL-2" 0 "SIL-2" 0
GND * 1 320 290 0 0 0 0
BiasT X1 1 350 170 -20 16 0 2 "1 uH" 0 "1 uF" 0
Pac P2 1 470 200 18 -26 0 0 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 470 230 0 0 0 0
IProbe Icc 1 240 140 -26 16 0 0
GND * 1 230 330 0 0 0 0
Idc Ibb 1 230 300 18 -26 0 0 "50µA" 1 "SIL-2" 0
_BJT BC850B 1 320 260 8 -26 0 0 "npn" 0 "1.8e-14" 0 "0.9955" 0 "1.005" 0 "0.14" 0 "0.03" 0 "80" 0 "12.5" 0 "5e-14" 0 "1.46" 0 "1.72e-13" 0 "1.27" 0 "400" 0 "35.5" 0 "0" 0 "0" 0 "0.25" 0 "0.6" 0 "0.56" 0 "1.3e-11" 0 "0.75" 0 "0.33" 0 "4e-12" 0 "0.54" 0 "0.33" 0 "1" 0 "0" 0 "0.75" 0 "0" 0 "0.5" 0 "6.4e-10" 0 "0" 0 "0" 0 "0" 0 "5.072e-08" 0 "26.85" 0 "0" 0 "1" 0 "1" 0 "0" 0 "1" 0 "1" 0 "0" 0 "0" 0 "3" 0 "1.11" 0 "26.85" 0 "1" 0 "7.02e-4" 0 "1108.0" 0 "SOT23" 0
.SP SP1 1 -10 390 0 61 0 0 "list" 1 "1 MHz" 0 "10 MHz" 0 "10 MHz" 1 "yes" 1 "1" 0 "2" 0 "none" 0
GND * 1 130 330 0 0 0 0
L L1 1 130 300 11 -24 0 3 "coil" 1 "0" 0 "0" 0 "SELF-WE-PD3S" 0
C C1 1 100 260 -26 -54 0 2 "cap" 1 "0" 0 "0" 0 "neutral" 0 "SMD0603" 0
Eqn Eqn1 0 370 337 0 8 0 0 "cap=64.28pF=" 1 "coil=3.86µH=" 1 "yes" 0
.Opt Opt1 1 140 390 0 41 0 0 "SP1" 1 "2|500|1e-4|0.2|1|7" 0 "Var=cap|yes|10e-9|1e-12|1e-6|linear" 0 "Var=coil|yes|10e-6|1e-9|1e-3|linear" 0 "Goal=NF|MIN|1|yes" 0
</Components>
<Wires>
-10 140 -10 150 "" 0 0 0 ""
-10 140 210 140 "" 0 0 0 ""
320 170 320 230 "" 0 0 0 ""
380 170 470 170 "" 0 0 0 ""
270 140 350 140 "" 0 0 0 ""
230 260 290 260 "" 0 0 0 ""
230 260 230 270 "" 0 0 0 ""
-10 260 -10 270 "" 0 0 0 ""
-10 260 70 260 "" 0 0 0 ""
130 260 130 270 "" 0 0 0 ""
130 260 230 260 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
Text -10 20 14 #000000 0 "Optimization task with two variables: \n Find the input impedance for lowest noise figure. \n The values in 'Eqn1' are the exact ones."
Arrow 130 460 -100 0 20 8 #ff0000 3 1 0
Arrow 280 590 -70 -40 20 8 #ff0000 3 1 0
Text 86 591 12 #ff0000 0 "the niose figure will be minimized \n (= the goal)"
Arrow 130 590 20 -40 20 8 #ff0000 3 1 0
Arrow 510 540 -150 -30 20 8 #ff0000 3 1 0
Text 346 541 12 #ff0000 0 "An easy way to add variables to the optimizer: \n 1) Click right mouse button onto component parameter. \n 2) Choose first topic in the menu."
</Paintings>
