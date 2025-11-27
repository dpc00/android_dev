<QucsStudio Schematic 3.3.2>
<Properties>
View=0,0,1176,848,1,0,0
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
GND * 1 40 190 0 0 0 0
C C1 1 210 160 19 -11 0 1 "C1_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
L L1 1 150 110 -26 10 0 0 "L1_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
GND * 1 210 190 0 0 0 0
.SP SP1 1 40 240 0 61 0 0 "lin" 1 "0.5 GHz" 1 "2 GHz" 1 "76" 1 "no" 0 "1" 0 "2" 0 "none" 0
Pac P1 1 40 160 18 -26 0 0 "1" 1 "12.5 ohms" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
C C2 1 370 160 18 -12 0 1 "C2_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
L L2 1 310 110 -26 10 0 0 "L2_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
GND * 1 370 190 0 0 0 0
GND * 1 530 190 0 0 0 0
L L3 1 470 110 -26 10 0 0 "L3_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C3 1 530 160 18 -12 0 1 "C3_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 690 190 0 0 0 0
GND * 1 800 190 0 0 0 0
L L4 1 630 110 -26 10 0 0 "L4_L" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C4 1 690 160 17 -13 0 1 "C4_C" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
Pac P2 1 800 160 18 -26 0 0 "2" 1 "50 ohms" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
.Opt Opt1 5 190 240 0 37 0 0 "SP1" 0 "5|6000|0.95|0.8|50|15" 0 "Var=L1_L|yes|1e-9|5e-11|2e-8|linear" 0 "Var=L2_L|yes|1e-9|5e-11|2e-8|linear" 0 "Var=L3_L|yes|1e-9|5e-11|2e-8|linear" 0 "Var=L4_L|yes|1e-9|5e-11|2e-8|linear" 0 "Var=C1_C|yes|1e-12|5e-13|2e-11|linear" 0 "Var=C2_C|yes|1e-12|5e-13|2e-11|linear" 0 "Var=C3_C|yes|1e-12|5e-13|2e-11|linear" 0 "Var=C4_C|yes|1e-12|5e-13|2e-11|linear" 0 "Goal=inputMatch|MIN|1|yes" 0
Eqn Eqn1 1 40 467 0 8 0 0 "inputMatch=max(dB(S[1,1]))=" 1 "yes" 0
</Components>
<Wires>
40 110 40 130 "" 0 0 0 ""
40 110 120 110 "" 0 0 0 ""
180 110 210 110 "" 0 0 0 ""
210 110 210 130 "" 0 0 0 ""
210 110 280 110 "" 0 0 0 ""
340 110 370 110 "" 0 0 0 ""
370 110 370 130 "" 0 0 0 ""
370 110 440 110 "" 0 0 0 ""
500 110 530 110 "" 0 0 0 ""
530 110 530 130 "" 0 0 0 ""
530 110 600 110 "" 0 0 0 ""
660 110 690 110 "" 0 0 0 ""
690 110 690 130 "" 0 0 0 ""
690 110 800 110 "" 0 0 0 ""
800 110 800 130 "" 0 0 0 ""
</Wires>
<Diagrams>
<Rect 80 740 270 190 31 #c0c0c0 1 00 1 0 50 119 0 -15 1 -5 1 0 0 0 315 0 225 "" "" "">
	<Legend 10 -100 0>
	<"goal.conv" "" #0000ff 0 3 0 0 0 0 "">
</Rect>
<Rect 540 520 340 230 31 #c0c0c0 1 00 1 5e+08 5e+08 1.8e+09 1 -52.352 10 -13.2323 1 0 0 0 315 0 225 "" "" "">
	<Legend 10 -100 0>
	<"dB(S[1,1])" "" #0000ff 0 3 0 0 0 0 "">
	<"dB(S[2,2])" "" #ff0000 0 3 0 1 0 0 "">
</Rect>
<Tab 670 280 210 50 71 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"max(dB(S[2,2]))" "" #0000ff 0 3 1 0 0 0 "">
</Tab>
</Diagrams>
<Paintings>
Text 40 10 14 #000000 0 "Perform broadband matching (12.5\\ohm to 50\\ohm) with a 4-stage LC circuit. \n This is a complex task with a rough initial estimate and several local minima. \n Hence, only heuristic methods like differential evolution (DE) will succeed."
Arrow 360 700 -130 -10 20 8 #000000 2 1 0
Text 366 601 12 #000000 0 "Algorithms like Nelder-Mead stop optimizing when the termination tolerance is reached. \n I.e. the maximum number of iterations is an upper limit that is usually not fully exploited. \n  \n For heuristic methods like DE the only termination criterion is the maximum iteration count \n that is given by the user. Thus, it's important to know if this number is sufficient or too high. \n The course of the goal variable is a good indicator for this. If it's still descending at the end \n of the optimization, the number of iterations must be increased. \n In order to get "goal.conv" the user must switch it on within the optimization component."
</Paintings>
