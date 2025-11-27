<Qucs Schematic 0.0.22>
<Properties>
  <View=173,-360,993,305,1.65375,0,172>
  <Grid=10,10,1>
  <DataSet=capacitor.dat>
  <DataDisplay=capacitor.dpl>
  <OpenDisplay=1>
  <Script=capacitor.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 14 CAP "1=R1=10=Rrad=" "1=V1=10e9=Value=">
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 10 40 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <.PortSym -30 0 2 0>
  <.PortSym 30 0 1 180>
</Symbol>
<Components>
  <Port P2 5 310 130 -67 13 0 0 "2" 1 "analog" 0 "v" 0 "" 0>
  <Port P3 5 310 -130 -67 17 0 0 "1" 1 "analog" 0 "v" 0 "" 0>
  <R R1 5 390 50 -82 -16 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <Eqn Eqn1 1 550 -110 -47 20 0 0 "C1=V1*1e-12" 1 "yes" 0>
  <C C1 5 390 -60 21 -15 0 1 "C1" 1 "" 0 "neutral" 0>
</Components>
<Wires>
  <310 -130 390 -130 "" 0 0 0 "">
  <390 -130 390 -90 "" 0 0 0 "">
  <390 -30 390 20 "" 0 0 0 "">
  <310 130 390 130 "" 0 0 0 "">
  <390 80 390 130 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
