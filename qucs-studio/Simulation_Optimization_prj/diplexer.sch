<QucsStudio Schematic 3.3.2>
<Properties>
View=6,-9,1060,818,1,0,0
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
GND * 1 40 320 0 0 0 0
Pac P1 1 40 290 18 -26 0 0 "1" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 240 320 0 0 0 0
GND * 1 390 320 0 0 0 0
Pac P2 1 390 290 18 -26 0 0 "2" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 390 490 0 0 0 0
Pac P3 1 390 460 18 -26 0 0 "3" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
GND * 1 240 490 0 0 0 0
C C2 1 170 380 -24 16 0 0 "HP / L1" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
C C3 1 310 380 -26 15 0 0 "HP / L2" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
L L3 1 240 460 16 -15 0 1 "HP / C1" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
L L1 1 170 210 -26 10 0 0 "L1" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
L L2 1 310 210 -26 10 0 0 "L2" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C1 1 240 290 17 -26 0 1 "C1" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 40 740 0 0 0 0
Pac P4 1 40 710 18 -26 0 0 "4" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
L L4 1 130 630 -26 10 0 0 "11.4nH" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
C C4 1 200 710 17 -26 0 1 "5.073pF" 1 "0" 0 "" 0 "neutral" 0 "SMD0603" 0
GND * 1 200 740 0 0 0 0
L L5 1 270 630 -26 10 0 0 "11.4nH" 1 "0" 0 "" 0 "SELF-WE-PD3S" 0
GND * 1 360 740 0 0 0 0
Pac P5 1 360 710 18 -26 0 0 "5" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0 "SUBCLICK" 0
Eqn Eqn1 1 40 437 0 8 0 0 "L1=11.4 nH=" 1 "C1=5.073 pF=" 1 "L2=11.4 nH=" 1 "HP=1 / (2*pi*1GHz)^2=" 1 "yes" 0
Eqn Goals 1 770 307 0 8 0 0 "transfer=max(abs(S[2,1] - S[5,4]))=" 1 "reflection=max(abs(S[1,1]))=" 1 "yes" 0
.SP SP1 1 890 100 2 60 0 0 "log" 1 "100MHz" 1 "10GHz" 1 "201" 1 "no" 0 "1" 0 "2" 0 "none" 0
.Opt Opt1 0 580 110 0 37 0 0 "SP1" 1 "1|500|1e-4|0.05|1|7" 0 "Var=L1|yes|11.4e-09|3e-9|30e-9|linear" 0 "Var=C1|yes|5.073e-12|2e-12|20e-12|linear" 0 "Var=L2|yes|11.4e-09|3e-9|30e-9|linear" 0 "Goal=transfer|MIN|1|yes" 0 "Goal=reflection|MIN|2|yes" 0
</Components>
<Wires>
40 210 40 260 "" 0 0 0 ""
40 210 120 210 "" 0 0 0 ""
240 210 240 260 "" 0 0 0 ""
240 210 280 210 "" 0 0 0 ""
200 210 240 210 "" 0 0 0 ""
340 210 390 210 "" 0 0 0 ""
390 210 390 260 "" 0 0 0 ""
390 380 390 430 "" 0 0 0 ""
340 380 390 380 "" 0 0 0 ""
120 210 140 210 "" 0 0 0 ""
120 210 120 380 "" 0 0 0 ""
120 380 140 380 "" 0 0 0 ""
240 380 240 430 "" 0 0 0 ""
240 380 280 380 "" 0 0 0 ""
200 380 240 380 "" 0 0 0 ""
40 630 40 680 "" 0 0 0 ""
40 630 100 630 "" 0 0 0 ""
200 630 200 680 "" 0 0 0 ""
200 630 240 630 "" 0 0 0 ""
160 630 200 630 "" 0 0 0 ""
300 630 360 630 "" 0 0 0 ""
360 630 360 680 "" 0 0 0 ""
</Wires>
<Diagrams>
<Rect 540 740 420 350 31 #c0c0c0 1 10 1 1e+08 1 1e+10 0 -60 5 5 1 0 0 0 315 0 225 "frequency (Hz)" "" "">
	<Legend 10 -100 0>
	<"dB(S[2,1])" "" #0000ff 0 3 0 0 0 0 "">
	<"dB(S[5,4])" "" #ff0000 0 3 0 0 0 0 "">
	<"dB(S[3,1])" "" #000000 0 3 0 0 0 0 "">
	<"dB(S[1,1])" "" #ff00ff 0 3 0 0 0 0 "">
	<"dB(S[3,3])" "" #00ff00 0 3 0 0 0 0 "">
</Rect>
</Diagrams>
<Paintings>
Arrow 650 170 230 0 20 8 #ff0000 3 1 0
Text 60 580 16 #000000 0 "1GHz Chebyshev, 0.1dB ripple"
Text 26 11 12 #ff0000 0 "This is how to create a diplexer: \n The circuit at the bottom is a low-pass filter designed by QucsFilter (CTRL+2). \n The circuit above is the same filter together with the equivalent high-pass filter. \n Both filters interact and the result isn't accurate. Check it by pressing F2 key. \n That's why it makes sense to use an optimizer with two goals: \n      "transfer" minimizes the difference to the original transfer curve. \n      "reflection" takes care for a good 50 ohms matching. \n So let's activate the optimization component and press F2 key again. \n The optimized values are transfered to component 'Opt1' by pressing F6 key."
Arrow 760 350 -100 -40 20 8 #ff0000 3 1 0
</Paintings>
