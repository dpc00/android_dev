<Qucs Schematic 0.0.22>
<Properties>
  <View=0,0,1082,800,1,0,0>
  <Grid=10,10,1>
  <DataSet=test.dat>
  <DataDisplay=test.dpl>
  <OpenDisplay=1>
  <Script=test.m>
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
  <Vdc V1 1 320 180 18 -26 0 1 "1 V" 1>
  <GND * 1 320 210 0 0 0 0>
  <R R1 1 610 130 -26 15 0 0 "50 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <GND * 1 640 130 0 0 0 0>
  <SPICE X1 1 490 130 -26 -77 0 0 "C:/projects/python-win-rf/temp.cir" 1 "_netp1,_netp2" 0 "yes" 0 "none" 0>
  <GND * 1 490 160 0 0 0 0>
  <.DC DC1 1 60 210 0 52 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.AC AC1 1 60 330 0 52 0 0 "lin" 1 "1 MHz" 1 "10 MHz" 1 "19" 1 "no" 0>
</Components>
<Wires>
  <520 130 580 130 "" 0 0 0 "">
  <320 130 320 150 "" 0 0 0 "">
  <320 130 460 130 "vin" 340 40 8 "">
  <520 130 520 130 "vout" 610 30 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
