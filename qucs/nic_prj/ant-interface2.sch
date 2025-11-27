<Qucs Schematic 0.0.19>
<Properties>
  <View=156,123,1617,904,0.836018,0,0>
  <Grid=10,10,1>
  <DataSet=ant-interface2.dat>
  <DataDisplay=ant-interface2.dpl>
  <OpenDisplay=1>
  <Script=ant-interface2.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 -16 SUB>
  <Line -20 20 40 0 #000080 2 1>
  <Line 20 20 0 -40 #000080 2 1>
  <Line -20 -20 40 0 #000080 2 1>
  <Line -20 20 0 -40 #000080 2 1>
</Symbol>
<Components>
  <GND * 1 210 310 0 0 0 0>
  <R R1 1 540 460 -16 -45 0 0 "R1" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C C1 1 470 400 13 -38 0 0 "C1" 0 "" 0 "neutral" 0>
  <L L1 1 440 460 -10 10 0 0 "L1" 0 "" 0>
  <SPfile X1 1 1160 240 -26 -77 0 0 "C:/projects/vna/4mloop.s1p" 1 "polar" 0 "linear" 0 "open" 0 "1" 0>
  <L L5 1 820 350 16 -11 0 3 "L5" 0 "" 0>
  <R R5 1 360 350 15 -26 0 1 "R5" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <.Opt Opt1 1 920 540 0 53 0 0 "Sim=DC1" 0 "DE=3|300|2|20|0.85|1|3|2e-4|10|100" 0 "Var=R1|no|0|0|300|LIN_DOUBLE" 0 "Var=Zp|no|50|0|3e3|LIN_DOUBLE" 0 "Var=f|yes|2.519360E+007|1e6|30e6|LIN_DOUBLE" 0 "Var=lcr|yes|4.205101E+006|1e5|1e7|LIN_DOUBLE" 0 "Var=Zout|no|50|0|3e3|LIN_DOUBLE" 0 "Var=L5|yes|9.322334E-007|3e-9|3e-6|LIN_DOUBLE" 0 "Var=R5|no|150|0|30000|LIN_DOUBLE" 0 "Var=C2|yes|3.381495E-011|1e-12|1e-9|LIN_DOUBLE" 0 "Goal=S11G|MIN|0" 0>
  <.DC DC1 1 920 440 0 53 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <GND * 1 400 460 0 0 0 0>
  <GND * 1 360 380 0 0 0 0>
  <C C2 1 480 300 13 -38 0 0 "C2" 0 "" 0 "neutral" 0>
  <Eqn OptValues2 5 350 570 -28 15 0 0 "R1=0" 1 "Zp=50" 1 "f=5.99e+06" 1 "lcr=7.48e+06" 1 "Zout=50" 1 "L5=1.02e-06" 1 "R5=150" 1 "C2=9.67e-10" 1 "yes" 0>
  <.SP SP1 5 1220 420 0 91 0 0 "log" 0 "1e6" 0 "30e6" 0 "200" 0 "yes" 0 "1" 0 "2" 0 "yes" 0 "no" 0>
  <GND * 1 1160 270 0 0 0 0>
  <Eqn OptValues1 5 1260 560 -28 15 0 0 "sf1=1e6" 1 "sf2=30e6" 1 "yes" 0>
  <Eqn Eqn1 5 1270 730 -47 20 0 0 "L1=sqrt(lcr)/(2*pi*f)" 1 "C1=1/(2*pi*f*sqrt(lcr))" 1 "S11G=abs(min(S[1,1],1e6:30e6))" 1 "yes" 0>
  <Pac P1 1 210 280 18 -26 0 1 "1" 1 "Zout" 1 "-5 dBm" 0 "1 GHz" 0 "26.85" 0>
</Components>
<Wires>
  <210 240 210 250 "" 0 0 0 "">
  <210 240 450 240 "" 0 0 0 "">
  <360 300 450 300 "" 0 0 0 "">
  <360 300 360 320 "" 0 0 0 "">
  <590 400 590 430 "" 0 0 0 "">
  <500 400 590 400 "" 0 0 0 "">
  <470 460 510 460 "" 0 0 0 "">
  <570 460 590 460 "" 0 0 0 "">
  <590 430 590 460 "" 0 0 0 "">
  <590 430 820 430 "" 0 0 0 "">
  <820 380 820 430 "" 0 0 0 "">
  <450 240 450 300 "" 0 0 0 "">
  <400 400 440 400 "" 0 0 0 "">
  <400 400 400 460 "" 0 0 0 "">
  <400 460 410 460 "" 0 0 0 "">
  <510 300 590 300 "" 0 0 0 "">
  <590 300 590 400 "" 0 0 0 "">
  <820 240 1130 240 "" 0 0 0 "">
  <820 240 820 320 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
