<Qucs Schematic 0.0.19>
<Properties>
  <View=80,123,1342,911,0.962901,0,0>
  <Grid=10,10,1>
  <DataSet=ant-interface1.dat>
  <DataDisplay=ant-interface1.dpl>
  <OpenDisplay=1>
  <Script=ant-interface1.m>
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
  <GND * 1 790 270 0 0 0 0>
  <SPfile X1 1 790 240 -26 -77 0 0 "C:/projects/vna/4mloop.s1p" 1 "polar" 0 "linear" 0 "open" 0 "1" 0>
  <.Opt Opt1 0 660 540 0 53 0 0 "Sim=DC1" 0 "DE=9|300|2|20|0.85|1|3|2e-6|10|100" 0 "Var=R1|yes|0.324|0|300|LIN_DOUBLE" 0 "Var=Zp|yes|197|0|3e3|LIN_DOUBLE" 0 "Var=f|yes|2.03e+07|1e6|30e6|LIN_DOUBLE" 0 "Var=lcr|yes|1e+05|1e5|1e7|LIN_DOUBLE" 0 "Var=R2|yes|1.4e+07|3e3|30e6|LIN_DOUBLE" 0 "Goal=S11|MIN|1" 0>
  <.DC DC1 1 660 440 0 53 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 5 960 420 0 91 0 0 "lin" 0 "1e6" 0 "30e6" 0 "116" 0 "yes" 0 "1" 0 "2" 0 "yes" 0 "no" 0>
  <Eqn Eqn1 5 1010 570 -47 20 0 0 "L1=sqrt(lcr)/(2*pi*f)" 1 "C1=1/(2*pi*f*sqrt(lcr))" 1 "S11=abs(avg(S[1,1],1e6:30e6))" 1 "yes" 0>
  <R R1 1 560 300 -16 -45 0 0 "R1" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C C1 1 490 240 13 -38 0 0 "C1" 0 "" 0 "neutral" 0>
  <L L1 1 460 300 -10 10 0 0 "L1" 0 "" 0>
  <R R2 1 510 360 -26 15 0 0 "R2" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <GND * 1 380 360 0 0 0 0>
  <GND * 1 220 340 0 0 0 0>
  <Pac P3 1 220 310 18 -26 0 1 "1" 1 "Zp" 1 "-5 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn OptValues1 1 250 490 -28 15 0 0 "R1=3.236278E-001" 1 "Zp=1.973828E+002" 1 "f=2.030044E+007" 1 "lcr=1.001877E+005" 1 "R2=1.400605E+007" 1 "yes" 0>
</Components>
<Wires>
  <520 240 620 240 "" 0 0 0 "">
  <490 300 530 300 "" 0 0 0 "">
  <380 300 430 300 "" 0 0 0 "">
  <380 360 480 360 "" 0 0 0 "">
  <380 300 380 360 "" 0 0 0 "">
  <620 240 630 240 "" 0 0 0 "">
  <620 200 620 240 "" 0 0 0 "">
  <220 200 620 200 "" 0 0 0 "">
  <220 200 220 280 "" 0 0 0 "">
  <590 300 600 300 "" 0 0 0 "">
  <600 270 600 300 "" 0 0 0 "">
  <540 360 630 360 "" 0 0 0 "">
  <630 240 760 240 "" 0 0 0 "">
  <630 240 630 360 "" 0 0 0 "">
  <460 240 460 270 "" 0 0 0 "">
  <460 270 600 270 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
