<Qucs Schematic 0.0.19>
<Properties>
  <View=200,177,1056,836,1.16238,0,0>
  <Grid=10,10,1>
  <DataSet=test1.dat>
  <DataDisplay=test1.dpl>
  <OpenDisplay=1>
  <Script=test1.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <GND * 1 260 320 0 0 0 0>
  <Sub NIC1 1 460 270 2 -8 0 0 "FloatC_NIC.sch" 0>
  <Sub NIC2 1 410 270 -26 -9 0 0 "FloatL_NIC.sch" 0>
  <.DC DC1 1 680 240 0 53 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.Opt Opt1 0 250 480 0 53 0 0 "Sim=SP1" 0 "DE=3|50|2|20|0.85|1|3|1e-2|6|8" 0 "Var=L1|no|0.000231|1e-9|1e-3|LIN_DOUBLE" 0 "Var=C1|no|6.33e-10|1e-15|1e-9|LIN_DOUBLE" 0 "Var=Zsl|no|4.53e+03|0|5000|LIN_DOUBLE" 0 "Var=R1|no|36.3|0|40|LIN_DOUBLE" 0 "Goal=OG|MAX|0" 0>
  <.SP SP1 1 680 340 0 91 0 0 "log" 0 "1 MHz" 0 "30 MHz" 0 "200" 0 "no" 0 "1" 0 "2" 0 "yes" 0 "yes" 0>
  <SPfile X1 5 580 240 -26 -23 0 0 "C:/projects/vna/4mloop.s1p" 0 "polar" 0 "linear" 0 "open" 0 "1" 0>
  <GND * 1 580 330 0 0 0 0>
  <Pac P2 5 580 300 18 -26 0 1 "2" 1 "Zsl" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P1 5 260 290 18 -26 0 1 "1" 1 "Zsl" 1 "-50 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn Eqn1 5 720 500 -47 20 0 0 "VSWR=rtoswr(S[1,1])" 1 "Gain=abs(S[2,1])^2" 1 "OG=abs(avg(Gain,1e6:30e6))" 1 "yes" 0>
  <L L1 1 410 420 -26 10 0 0 "L1" 0 "" 0>
  <R R1 1 380 370 15 -26 0 1 "R1" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C C1 1 490 420 -26 17 0 0 "C1" 0 "" 0 "neutral" 0>
  <Eqn OptValues6 5 720 630 -28 15 0 0 "Fres=1/(2*pi*sqrt(L1*C1))" 1 "yes" 0>
  <Eqn OptValues7 1 490 580 -28 15 0 0 "L1=0.000231" 1 "C1=6.33e-10" 1 "Zsl=3200" 1 "R1=3.627675E+001" 1 "yes" 0>
</Components>
<Wires>
  <260 240 260 260 "" 0 0 0 "">
  <260 240 380 240 "" 0 0 0 "">
  <380 210 380 240 "" 0 0 0 "">
  <380 210 460 210 "" 0 0 0 "">
  <460 210 460 240 "" 0 0 0 "">
  <440 200 440 240 "" 0 0 0 "">
  <440 200 520 200 "" 0 0 0 "">
  <520 200 520 240 "" 0 0 0 "">
  <520 240 550 240 "" 0 0 0 "">
  <440 300 440 420 "" 0 0 0 "">
  <380 300 380 340 "" 0 0 0 "">
  <380 400 380 420 "" 0 0 0 "">
  <520 300 520 420 "" 0 0 0 "">
  <460 300 460 420 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
