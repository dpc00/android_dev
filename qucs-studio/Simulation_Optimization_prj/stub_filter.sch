<QucsStudio Schematic 3.3.2>
<Properties>
View=16,29,1002,920,1,0,0
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
MLIN MS2 1 280 180 -26 -72 1 0 "RO4003" 0 "1.8 mm" 1 "lenM" 1 "26.85" 0
SUBST RO4003 1 690 160 -30 24 0 0 "3.38" 1 "0.8 mm" 1 "17.5 µm" 1 "0.002" 1 "1.72e-08" 1 "1e-6" 0 "Metal" 1 "Hammerstad" 0 "Kirschning" 0
Pac P2 1 530 240 18 -26 0 0 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 530 270 0 0 0 0
Pac P1 1 50 240 18 -26 0 0 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 50 270 0 0 0 0
MTEE MS1 1 170 180 -26 -91 0 0 "RO4003" 0 "1.8 mm" 1 "1.8 mm" 1 "1.8 mm" 1 "showNumbers" 0
MLIN MS4 1 170 240 15 -26 0 1 "RO4003" 0 "1.8 mm" 1 "lenStub1" 1 "26.85" 0
MOPEN MS6 1 170 300 16 -11 0 3 "RO4003" 0 "1.8 mm" 1 "Kirschning" 0
MTEE MS3 1 380 180 -26 -91 0 0 "RO4003" 0 "1.8 mm" 1 "1.8 mm" 1 "1.8 mm" 1 "showNumbers" 0
MLIN MS5 1 380 240 15 -26 0 1 "RO4003" 0 "1.8 mm" 1 "lenStub2" 1 "26.85" 0
MOPEN MS7 1 380 300 15 -12 0 3 "RO4003" 0 "1.8 mm" 1 "Kirschning" 0
.SP SP1 1 50 360 0 60 0 0 "lin" 1 "2 GHz" 1 "12 GHz" 1 "401" 1 "no" 0 "1" 0 "2" 0 "none" 0
Eqn Eqn1 1 480 377 0 8 0 0 "reject=max(range(dB(S[2,1]), 8GHz, 12GHz))=" 1 "pass=max(range(dB(S[1,1]), 2GHz, 5GHz))+12=" 1 "yes" 0
.Opt Opt1 1 210 360 0 37 0 0 "SP1" 0 "1|2000|1e-5|0.05|1|7" 0 "Var=lenM|yes|0.005|1e-4|1e-2|linear" 0 "Var=lenStub1|yes|0.004|1e-4|1e-2|linear" 0 "Var=lenStub2|yes|0.004|1e-4|1e-2|linear" 0 "Goal=reject|MIN|1|yes" 0 "Goal=pass|BZ|5|yes" 0
</Components>
<Wires>
200 180 250 180 "" 0 0 0 ""
310 180 350 180 "" 0 0 0 ""
530 180 530 210 "" 0 0 0 ""
410 180 530 180 "" 0 0 0 ""
50 180 140 180 "" 0 0 0 ""
50 180 50 210 "" 0 0 0 ""
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
Arrow 410 540 -100 -20 20 8 #ff0000 3 1 0
Text 100 50 14 #000000 0 "Filter with two open-end microstrip stubs."
Arrow 540 520 20 -70 20 8 #ff0000 3 1 0
Text 416 521 12 #ff0000 0 "Between 8 GHz and 12 GHz transfer (S21) as low as possible. \n Between 2 GHz and 5 GHz reflection (S11) below -12 dB."
</Paintings>
