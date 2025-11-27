<QucsStudio Schematic 3.3.2>
<Properties>
View=0,-119,1097,750,1,0,20
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.sch
OpenDisplay=1
showFrame=0
FrameText0=Title
FrameText1=Drawn By:
FrameText2=Date:
FrameText3=Revision:
</Properties>
<Symbol>
</Symbol>
<Components>
GND * 1 40 150 0 0 0 0
L L1 1 150 40 -26 10 0 0 "L1_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C1 1 220 120 17 -26 0 1 "C1_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 220 150 0 0 0 0
L L2 1 290 40 -26 10 0 0 "L2_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
GND * 1 360 150 0 0 0 0
Pac P2 1 360 120 18 -26 0 0 "2" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
Pac P1 1 40 120 18 -26 0 0 "1" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
L L5 1 330 220 -26 -44 0 0 "L5_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C4 1 270 220 -26 10 0 0 "C4_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 360 330 0 0 0 0
Pac P4 1 360 300 18 -26 0 0 "3" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
L L3 1 210 220 -26 -44 0 0 "L3_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C2 1 150 220 -26 10 0 0 "C2_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
L L4 1 240 300 8 -14 0 1 "L4_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C3 1 210 300 -79 -9 0 1 "C3_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 240 330 0 0 0 0
GND * 1 220 490 0 0 0 0
GND * 1 360 490 0 0 0 0
Pac P7 1 40 610 18 -26 0 0 "5" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 40 640 0 0 0 0
L L7 1 150 530 -26 10 0 0 "14.83nH" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C7 1 220 610 17 -26 0 1 "4.076pF" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 220 640 0 0 0 0
L L8 1 290 530 -26 10 0 0 "14.83nH" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
Pac P8 1 360 610 18 -26 0 0 "6" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 360 640 0 0 0 0
C C5 1 150 380 -27 10 0 0 "HP/L1_L" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
C C6 1 290 380 -27 10 0 0 "HP/L2_L" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
L L6 1 220 460 17 -26 0 1 "HP/C1_C" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
Pac P6 1 360 460 18 -26 0 0 "4" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
Eqn Eqn1 1 20 437 0 8 0 0 "HP=0.25 / (2*pi*1GHz)^2=" 1 "yes" 0
Eqn Goals 1 750 17 0 8 0 0 "transfer=max(abs(S[1,2] - S[5,6]))=" 1 "reflection=max(abs(S[1,1]))=" 1 "yes" 0
.SP SP1 1 450 30 0 60 0 0 "log" 1 "100MHz" 1 "30GHz" 1 "620" 1 "no" 0 "1" 0 "2" 0 "none" 0
.Opt Opt1 1 600 30 0 37 0 0 "SP1" 1 "2|5000|1e-4|0.1|1|7" 0 "Var=L1_L|yes|1.483e-08|1.483e-09|1.483e-07|linear" 0 "Var=L2_L|yes|1.483e-08|1.483e-09|1.483e-07|linear" 0 "Var=C1_C|yes|4.076e-12|4.076e-13|4.076e-11|linear" 0 "Var=C2_C|yes|1.281e-12|1.281e-13|1.281e-11|linear" 0 "Var=L3_L|yes|4.943e-09|4.943e-10|4.943e-08|linear" 0 "Var=C4_C|yes|1.281e-12|1.281e-13|1.281e-11|linear" 0 "Var=L5_L|yes|4.943e-09|4.943e-10|4.943e-08|linear" 0 "Var=C3_C|yes|1.359e-12|1.359e-13|1.359e-11|linear" 0 "Var=L4_L|yes|4.661e-09|4.661e-10|4.661e-08|linear" 0 "Goal=transfer|MIN|1|yes" 0 "Goal=reflection|MIN|4|yes" 0
</Components>
<Wires>
40 40 40 90 "" 0 0 0 ""
40 40 120 40 "" 0 0 0 ""
220 40 220 90 "" 0 0 0 ""
360 40 360 90 "" 0 0 0 ""
220 40 260 40 "" 0 0 0 ""
180 40 220 40 "" 0 0 0 ""
320 40 360 40 "" 0 0 0 ""
360 220 360 270 "" 0 0 0 ""
240 220 240 270 "" 0 0 0 ""
210 270 240 270 "" 0 0 0 ""
210 330 240 330 "" 0 0 0 ""
220 380 220 430 "" 0 0 0 ""
360 380 360 430 "" 0 0 0 ""
220 380 260 380 "" 0 0 0 ""
180 380 220 380 "" 0 0 0 ""
320 380 360 380 "" 0 0 0 ""
40 530 40 580 "" 0 0 0 ""
220 530 220 580 "" 0 0 0 ""
360 530 360 580 "" 0 0 0 ""
220 530 260 530 "" 0 0 0 ""
180 530 220 530 "" 0 0 0 ""
320 530 360 530 "" 0 0 0 ""
40 530 120 530 "" 0 0 0 ""
120 40 120 220 "" 0 0 0 ""
120 220 120 380 "" 0 0 0 ""
</Wires>
<Diagrams>
<Rect 560 630 410 290 31 #c0c0c0 1 10 1 1e+08 1 3e+10 0 -40 5 0 1 0 0 0 315 0 225 "frequency (Hz)" "" "">
	<Legend 10 -100 0>
	<"dB(S[1,1])" "" #0000ff 0 3 0 0 0 0 "">
	<"dB(S[1,2])" "" #ff0000 0 3 0 0 0 0 "">
	<"dB(S[1,3])" "" #ff00ff 0 3 0 0 0 0 "">
	  <Mkr 1.00104e+09 10 -270 3 1 0 0 0 50>
	<"dB(S[1,4])" "" #00ff00 0 3 0 0 0 0 "">
	<"dB(S[5,6])" "" #00ffff 0 3 0 0 0 0 "">
</Rect>
</Diagrams>
<Paintings>
Text 46 -79 12 #ff0000 0 "Let's create a triplexer. Use QucsFilter (CTRL+2) to design three Chebyshev filters: \n 1) low-pass filter with 1GHz cut-off frequency \n 2) band-pass filter from 1GHz to 4GHz \n 3) high-pass filter with 4GHz cut-off frequency \n All filters interact and thus S11 needs to be improved by the optimizer."
</Paintings>
