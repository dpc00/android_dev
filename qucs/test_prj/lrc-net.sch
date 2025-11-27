<Qucs Schematic 0.0.19>
<Properties>
  <View=7,61,1084,736,1.28773,74,0>
  <Grid=10,10,1>
  <DataSet=lrc-net.dat>
  <DataDisplay=lrc-net.dpl>
  <OpenDisplay=0>
  <Script=lrc-net.m>
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
  <Pac P1 1 150 220 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 150 250 0 0 0 0>
  <.DC DC1 1 710 160 0 52 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 1 710 290 0 89 0 0 "lin" 1 "1 MHz" 1 "30 MHz" 1 "101" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Pac P2 1 460 220 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 460 250 0 0 0 0>
  <L L1 1 330 160 -26 10 0 0 "8.25 uH" 1 "" 0>
  <C C1 1 330 130 -26 17 0 0 "72 pF" 1 "" 0 "neutral" 0>
</Components>
<Wires>
  <150 160 150 190 "" 0 0 0 "">
  <150 160 280 160 "" 0 0 0 "">
  <360 160 380 160 "" 0 0 0 "">
  <460 160 460 190 "" 0 0 0 "">
  <280 160 300 160 "" 0 0 0 "">
  <280 130 280 160 "" 0 0 0 "">
  <280 130 300 130 "" 0 0 0 "">
  <360 130 380 130 "" 0 0 0 "">
  <380 160 460 160 "" 0 0 0 "">
  <380 130 380 160 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 150 624 505 324 3 #c0c0c0 1 00 1 0 5e+06 3e+07 1 -0.0979857 0.5 1.09982 1 -1 1 1 315 0 225 "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
	<"S[2,1]" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
