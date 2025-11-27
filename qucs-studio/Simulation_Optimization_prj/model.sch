<QucsStudio Schematic 3.3.2>
<Properties>
View=0,0,1219,800,1,0,0
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
.DC DC1 1 20 100 0 37 0 0 "0.001" 0 "1 nA" 0 "500" 0 "none" 0
IProbe Id 1 290 320 -26 16 0 0
GND * 1 350 400 0 0 0 0
GND * 1 180 400 0 0 0 0
Vdc V1 1 180 370 18 -26 0 0 "Vd" 1 "battery" 0 "SIL-2" 0
Diode D1 1 350 370 15 -26 0 1 "Is" 1 "N" 1 "10 fF" 0 "0.5" 0 "0.7 V" 0 "0.5" 0 "0.0 fF" 0 "0.0" 0 "2.0" 0 "Rs" 1 "0.0 ps" 0 "0" 0 "0.0" 0 "1.0" 0 "1.0" 0 "0" 0 "1 mA" 0 "26.85" 0 "3.0" 0 "1.11" 0 "0.0" 0 "0.0" 0 "0.0" 0 "0.0" 0 "0.0" 0 "0.0" 0 "26.85" 0 "1.0" 0 "7.02e-4" 0 "1108.0" 0 "normal" 0 "D5" 0
.SW SW1 1 180 100 0 61 0 0 "DC1" 1 "Vd" 1 "list" 1 "5 Ohm" 0 "50 Ohm" 0 "0.1;0.2;0.3;0.4;0.5;0.6;0.7;0.8;0.9;0.95" 1
Eqn EqnOpt 1 600 307 0 8 0 0 "fit=max(log10(Id.I/Im)^2)=" 1 "Is=1e-10=" 1 "N=1=" 1 "Rs=0=" 1 "yes" 0
Eqn Measurement 1 30 457 0 8 0 0 "Im=[2.65E-8,2.33E-7,1.68E-6,1.24E-5,9.96E-5,8.27E-4,5.95E-3,2.68E-2,7.32E-2,1.01E-1]=" 1 "yes" 0
.Opt Opt1 1 530 100 0 37 0 0 "SW1" 1 "0|1000|1e-5|0.1|1|7" 0 "Var=Is|yes|1e-10|1e-11|1e-08|linear" 0 "Var=N|yes|1|1|2|linear" 0 "Var=Rs|yes|0|0|5|linear" 0 "Goal=fit|MIN|1|yes" 0
</Components>
<Wires>
180 320 180 340 "" 0 0 0 ""
180 320 260 320 "" 0 0 0 ""
350 320 350 340 "" 0 0 0 ""
320 320 350 320 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
Text 16 21 14 #000000 0 "This optimization should fit measurement data from a real diode (1N4148) to the model. \n The fit function uses a logarithmic comparison because the values span many decades."
Arrow 170 190 -110 -40 20 8 #ff0000 2 1 0
Arrow 520 170 -300 0 20 8 #ff0000 2 1 0
Arrow 530 230 -130 150 20 8 #ff0000 2 1 0
Arrow 590 340 -50 -70 20 8 #ff0000 2 1 0
</Paintings>
