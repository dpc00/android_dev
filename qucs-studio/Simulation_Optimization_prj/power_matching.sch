<QucsStudio Schematic 3.3.2>
<Properties>
View=-24,-19,1003,616,1,0,0
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
Vdc Source 1 30 210 18 -26 0 0 "1 V" 1 "SIL-2" 0 "SIL-2" 0
GND * 1 30 240 0 0 0 0
GND * 1 250 250 0 0 0 0
IProbe current 1 200 160 -26 16 0 0
R R1 1 250 220 15 -26 0 1 "R_load" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
.DC DC1 1 10 300 0 41 0 0 "1e-3" 0 "1e-6" 0 "300" 0 "none" 0
Eqn Eqn1 1 60 487 0 8 0 0 "power=voltage * current=" 1 "yes" 0
R R_intern 1 90 160 -28 -59 0 2 "50" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0 "SMD0603" 0
.Opt Opt1 1 170 300 0 41 0 0 "DC1" 1 "1|500|1e-5|0.1|1|3" 0 "Var=R_load|yes|10|0|1e6|linear" 0 "Goal=power|MAX|1|yes" 0
</Components>
<Wires>
250 160 250 190 "voltage" 280 150 16 ""
230 160 250 160 "" 0 0 0 ""
30 160 30 180 "" 0 0 0 ""
30 160 60 160 "" 0 0 0 ""
120 160 170 160 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
Text 0 10 14 #000000 0 "The most famous optimization task: \n Find the load resistor for getting the highest power out of the source. \n The result is of course well known."
Arrow 310 240 -70 140 20 8 #ff0000 3 1 0
Arrow 160 370 -110 -20 20 8 #ff0000 3 1 0
Text 56 371 12 #ff0000 0 "the simulation \n to optimze"
Text 316 251 12 #ff0000 0 "the parameter that will be changed (= the variable) \n starting value is 10; limits are 0 and 10^{6}"
Text 166 451 12 #ff0000 0 "the parameter that will be maximized \n (= the goal)"
Arrow 100 510 90 -90 20 8 #ff0000 3 1 0
Arrow 350 450 -80 -30 20 8 #ff0000 3 1 0
</Paintings>
