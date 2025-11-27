<Qucs Schematic 0.0.19>
<Properties>
  <View=51,-213,661,178,2.04348,0,0>
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
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <.PortSym 30 0 2 180>
  <.PortSym -30 0 1 0>
  <Line -20 10 40 0 #000080 2 1>
  <.ID -50 34 SERLC "1=L1=1e-6=Inductor1=" "1=C1=1e-12=Capacitor1=" "1=R1=1=Resistor1=" "1=CS=0=ShortCap=" "1=LS=0=ShortCoil=">
</Symbol>
<Components>
  <Port P2 5 160 130 -61 -41 0 0 "2" 1 "analog" 0>
  <Relais S1 1 380 -90 -12 -15 1 2 "0.5 V" 0 "0.1 V" 0 "0" 0 "1e12" 0 "26.85" 0>
  <Port P1 5 160 -130 -69 -43 0 0 "1" 1 "analog" 0>
  <Sub CAP1 5 250 -90 -90 -22 0 1 "capacitor.sch" 0 "C1" 1>
  <Vdc V1 1 460 -90 18 -26 0 1 "CS" 1>
  <GND * 1 460 -60 0 0 0 0>
  <R R1 5 250 90 -77 -29 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <Sub IND1 5 250 0 -89 -24 0 1 "inductor.sch" 0 "L1" 1>
  <Vdc V2 1 540 0 18 -26 0 1 "LS" 1>
  <Relais S2 1 460 0 -79 -26 1 2 "0.5 V" 0 "0.1 V" 0 "0" 0 "1e12" 0 "26.85" 0>
  <GND * 1 540 30 0 0 0 0>
</Components>
<Wires>
  <160 -130 250 -130 "" 0 0 0 "">
  <250 -130 250 -120 "" 0 0 0 "">
  <250 -130 350 -130 "" 0 0 0 "">
  <250 -60 250 -40 "" 0 0 0 "">
  <250 -40 350 -40 "" 0 0 0 "">
  <350 -60 350 -40 "" 0 0 0 "">
  <350 -130 350 -120 "" 0 0 0 "">
  <410 -120 460 -120 "" 0 0 0 "">
  <410 -60 460 -60 "" 0 0 0 "">
  <160 130 250 130 "" 0 0 0 "">
  <250 120 250 130 "" 0 0 0 "">
  <250 40 250 60 "" 0 0 0 "">
  <250 40 430 40 "" 0 0 0 "">
  <250 -40 250 -30 "" 0 0 0 "">
  <250 30 250 40 "" 0 0 0 "">
  <430 -40 430 -30 "" 0 0 0 "">
  <350 -40 430 -40 "" 0 0 0 "">
  <490 30 540 30 "" 0 0 0 "">
  <490 -30 540 -30 "" 0 0 0 "">
  <430 30 430 40 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
