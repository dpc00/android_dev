<Qucs Schematic 0.0.19>
<Properties>
  <View=156,101,1318,917,1.02496,0,0>
  <Grid=10,10,1>
  <DataSet=test1_copy1.dat>
  <DataDisplay=test1_copy1.dpl>
  <OpenDisplay=1>
  <Script=test1_copy1.m>
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
  <GND * 1 770 330 0 0 0 0>
  <SPfile X1 1 770 300 -26 -77 0 0 "C:/projects/vna/4mloop.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
  <.DC DC1 1 960 150 0 53 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <GND * 1 210 310 0 0 0 0>
  <Eqn OptValues1 5 1000 610 -28 15 0 0 "OG=(avg(S[1,1],1e6:300e6))" 1 "yes" 0>
  <Pac P1 1 210 280 18 -26 0 1 "1" 1 "50 Ohm" 1 "-5 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Sub NIC1 1 450 270 -26 48 0 0 "opamp-nic.sch" 0>
  <.SP SP1 1 970 330 0 91 0 0 "lin" 1 "1 MHz" 1 "30 MHz" 1 "300" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Eqn Eqn1 1 660 440 -47 20 0 0 "Fr=16.4e6" 1 "yes" 0>
  <L L1 1 450 420 -26 10 0 0 "9 uH" 1 "" 0>
  <C C1 1 510 420 -26 17 0 0 "9 pF" 1 "" 0 "neutral" 0>
</Components>
<Wires>
  <480 300 740 300 "" 0 0 0 "">
  <210 240 420 240 "" 0 0 0 "">
  <210 240 210 250 "" 0 0 0 "">
  <420 420 420 460 "" 0 0 0 "">
  <480 240 510 240 "" 0 0 0 "">
  <510 240 510 380 "" 0 0 0 "">
  <380 380 510 380 "" 0 0 0 "">
  <380 380 380 460 "" 0 0 0 "">
  <380 460 420 460 "" 0 0 0 "">
  <550 350 550 420 "" 0 0 0 "">
  <420 350 550 350 "" 0 0 0 "">
  <420 300 420 350 "" 0 0 0 "">
  <420 300 430 300 "" 0 0 0 "">
  <540 420 550 420 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
