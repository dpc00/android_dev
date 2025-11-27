<Qucs Schematic 0.0.22>
<Properties>
  <View=63,-219,593,209,2.02804,0,0>
  <Grid=10,10,1>
  <DataSet=inductor.dat>
  <DataDisplay=inductor.dpl>
  <OpenDisplay=1>
  <Script=inductor.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 14 IND "1=R1=10=Rrad=" "1=V1=1e-6=Value=">
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 10 40 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <.PortSym 30 0 1 180>
  <.PortSym -30 0 2 0>
</Symbol>
<Components>
  <Port P3 5 160 -130 -84 20 0 0 "1" 1 "analog" 0 "v" 0 "" 0>
  <Port P2 5 160 130 -23 12 0 0 "2" 1 "analog" 0 "v" 0 "" 0>
  <R R1 5 250 50 18 -18 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <L L1 5 250 -60 12 -15 0 1 "L1" 1 "" 0>
  <Eqn Eqn1 5 410 -110 -47 20 0 0 "L1=V1*1e-6" 1 "yes" 0>
</Components>
<Wires>
  <160 -130 250 -130 "" 0 0 0 "">
  <250 -130 250 -90 "" 0 0 0 "">
  <250 -30 250 20 "" 0 0 0 "">
  <160 130 250 130 "" 0 0 0 "">
  <250 80 250 130 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
