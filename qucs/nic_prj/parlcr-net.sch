<Qucs Schematic 0.0.19>
<Properties>
  <View=184,150,949,488,2.01895,0,0>
  <Grid=10,10,1>
  <DataSet=parlcr-net.dat>
  <DataDisplay=parlcr-net.dpl>
  <OpenDisplay=1>
  <Script=parlcr-net.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 14 SUB "1=L=0==" "1=C=0==" "1=R=0==">
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 10 40 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <.PortSym 30 0 2 180>
  <.PortSym -30 0 1 0>
</Symbol>
<Components>
  <L L1 1 470 260 -19 -75 0 0 "L1v" 1 "" 0>
  <R R1 1 390 260 -30 -74 0 0 "R" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C C1 1 420 320 -20 27 0 0 "C1v" 1 "" 0 "neutral" 0>
  <Eqn Eqn1 5 610 340 -47 20 0 0 "L1v=L*1e-6" 1 "C1v=C*1e-12" 1 "yes" 0>
  <Port P2 1 550 260 40 -26 1 2 "2" 1 "analog" 0>
  <Port P1 1 310 260 -106 -22 0 0 "1" 1 "analog" 0>
</Components>
<Wires>
  <420 260 440 260 "" 0 0 0 "">
  <500 260 530 260 "" 0 0 0 "">
  <330 260 360 260 "" 0 0 0 "">
  <330 260 330 320 "" 0 0 0 "">
  <530 260 530 320 "" 0 0 0 "">
  <450 320 530 320 "" 0 0 0 "">
  <330 320 390 320 "" 0 0 0 "">
  <530 260 550 260 "" 0 0 0 "">
  <310 260 330 260 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
