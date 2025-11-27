<Qucs Schematic 0.0.19>
<Properties>
  <View=173,-232,924,305,1.65375,0,0>
  <Grid=10,10,1>
  <DataSet=aa-network.dat>
  <DataDisplay=aa-network.dpl>
  <OpenDisplay=1>
  <Script=aa-network.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 14 MAGANT "1=L1=1e-6=Inductor1=" "1=C1=1e-12=Capacitor1=" "1=L2=1e-12=Inductor2=" "1=R2=10=Rrad=" "1=C2=1e-12=Capacitor2=">
  <.PortSym -30 0 1 0>
  <.PortSym 30 0 2 0>
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 10 40 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
</Symbol>
<Components>
  <Port P1 5 240 -130 -23 12 0 0 "1" 1 "analog" 0>
  <Port P2 5 240 130 -23 12 0 0 "2" 1 "analog" 0>
  <L L3 5 530 -10 -85 7 0 1 "L1" 1 "" 0>
  <C C3 5 590 -10 -30 55 0 1 "C1" 1 "" 0 "neutral" 0>
  <R R1 5 720 50 30 -24 0 1 "R2" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C C4 5 720 -10 27 -25 0 1 "C2" 1 "" 0 "neutral" 0>
  <L L4 5 720 -70 26 -13 0 1 "L2" 1 "" 0>
</Components>
<Wires>
  <530 -130 530 -40 "" 0 0 0 "">
  <530 20 530 130 "" 0 0 0 "">
  <530 -130 590 -130 "" 0 0 0 "">
  <590 -130 590 -40 "" 0 0 0 "">
  <530 130 590 130 "" 0 0 0 "">
  <590 20 590 130 "" 0 0 0 "">
  <240 -130 530 -130 "" 0 0 0 "">
  <240 130 530 130 "" 0 0 0 "">
  <590 -130 720 -130 "" 0 0 0 "">
  <720 -130 720 -100 "" 0 0 0 "">
  <720 80 720 130 "" 0 0 0 "">
  <590 130 720 130 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
