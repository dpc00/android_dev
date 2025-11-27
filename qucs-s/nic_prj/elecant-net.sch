<Qucs Schematic 0.0.22>
<Properties>
  <View=63,-219,593,209,2.02804,0,0>
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
  <.ID -20 14 ELECANT "1=L1=1e-6=Inductor1=" "1=C1=1e-12=Capacitor1=" "1=R1=10=Rrad=">
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
  <Port P3 5 160 -130 -84 20 0 0 "1" 1 "analog" 0 "v" 0 "" 0>
  <Port P2 5 160 130 -23 12 0 0 "2" 1 "analog" 0 "v" 0 "" 0>
  <R R1 5 250 70 18 -18 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <L L1 5 250 -10 12 -15 0 1 "L1" 1 "" 0>
  <C C1 5 250 -90 -33 -80 0 3 "C1" 1 "" 0 "neutral" 0>
  <R R2 5 300 -90 -15 -26 0 3 "9e9 Ohm" 0 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
</Components>
<Wires>
  <160 -130 250 -130 "" 0 0 0 "">
  <160 130 250 130 "" 0 0 0 "">
  <250 100 250 130 "" 0 0 0 "">
  <250 20 250 40 "" 0 0 0 "">
  <300 -130 300 -120 "" 0 0 0 "">
  <250 -130 250 -120 "" 0 0 0 "">
  <250 -130 300 -130 "" 0 0 0 "">
  <300 -60 300 -50 "" 0 0 0 "">
  <250 -60 250 -50 "" 0 0 0 "">
  <250 -50 250 -40 "" 0 0 0 "">
  <250 -50 300 -50 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
