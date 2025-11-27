<Qucs Schematic 0.0.19>
<Properties>
  <View=63,-219,593,209,2.02804,0,95>
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
  <.ID -20 14 IND "1=V1=1=Value=">
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 10 40 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <.PortSym -30 0 1 0>
  <.PortSym 30 0 2 180>
</Symbol>
<Components>
  <L L1 5 250 -60 12 -15 0 1 "L1" 1 "" 0>
  <Eqn Eqn1 5 410 -110 -47 20 0 0 "L1=V1*1e-6" 1 "yes" 0>
  <Port P2 5 160 20 -49 -48 0 0 "2" 1 "analog" 0>
  <Port P1 5 160 -130 -54 22 0 0 "1" 1 "analog" 0>
</Components>
<Wires>
  <160 -130 250 -130 "" 0 0 0 "">
  <250 -130 250 -90 "" 0 0 0 "">
  <250 -30 250 20 "" 0 0 0 "">
  <160 20 250 20 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
