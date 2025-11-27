<Qucs Schematic 0.0.19>
<Properties>
  <View=-2378,-137,-662,1115,1.00821,139,0>
  <Grid=10,10,1>
  <DataSet=antenna-adapter2.dat>
  <DataDisplay=antenna-adapter2.dpl>
  <OpenDisplay=0>
  <Script=antenna-adapter2.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.ID -20 -16 SUB>
  <Line -20 20 40 0 #000080 2 1>
  <Line 20 20 0 -40 #000080 2 1>
  <Line -20 -20 40 0 #000080 2 1>
  <Line -20 20 0 -40 #000080 2 1>
</Symbol>
<Components>
  <GND * 1 -2140 20 0 0 1 1>
  <Pac P2 5 -2090 20 -37 21 1 0 "1" 1 "50" 1 "-40 dBm" 0 "1 GHz" 0 "26.85" 0>
  <SPfile X1 1 -1460 20 -26 -77 0 0 "C:/projects/sNp/4mloop.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
  <GND * 1 -1460 50 0 0 0 0>
  <C C1 1 -1570 20 -20 27 0 0 "C1v" 1 "" 0 "neutral" 0>
  <Sub NIC1 1 -1930 50 -20 44 0 0 "opamp-nic.sch" 0 "200 Ohm" 1>
  <.DC DC1 1 -1260 30 0 57 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 1 -1260 130 0 100 0 0 "lin" 0 "F1" 0 "F2" 0 "101" 0 "no" 0 "1" 0 "2" 0 "yes" 0 "yes" 0>
  <.Opt Opt1 0 -1250 280 0 57 0 0 "Sim=SP1" 0 "DE=3|130|2|20|0.85|1|7552688|1e-2|10|100" 0 "Var=LCr1|yes|1.05|1|1e9|LIN_DOUBLE" 0 "Var=Fr1|yes|2.87e+07|1e6|30e6|LIN_DOUBLE" 0 "Goal=OG1|MIN|3" 0>
  <Eqn Eqn1 5 -1200 420 -47 20 0 0 "F1=1e6" 1 "F2=30e6" 1 "Z0=50" 1 "vs1=rtoswr(S[1,1])" 1 "OG1=avg(abs(vs1),1e3:30e6)" 1 "yes" 0>
  <Eqn Eqn3 5 -1200 620 -47 20 0 0 "L1=sqrt(LCr1)/(2*pi*Fr1)*1e6" 1 "C1=1/(sqrt(LCr1)*2*pi*Fr1)*1e12" 1 "yes" 0>
  <L L1 1 -1680 20 -19 -75 0 0 "L1v" 1 "" 0>
  <Eqn Eqn4 5 -1580 170 -47 20 0 0 "L1v=L1*1e-6" 1 "C1v=C1*1e-12" 1 "yes" 0>
  <C C2 1 -1890 200 -20 27 0 0 "C1v" 1 "" 0 "neutral" 0>
  <L L2 1 -1980 200 -26 25 0 0 "L1v" 1 "" 0>
  <Eqn OptValues1 1 -1200 760 -28 15 0 0 "LCr1=1.053311E+000" 1 "Fr1=2.873375E+007" 1 "yes" 0>
</Components>
<Wires>
  <-2140 20 -2120 20 "" 0 0 0 "">
  <-1540 20 -1490 20 "" 0 0 0 "">
  <-2060 20 -1960 20 "" 0 0 0 "">
  <-2050 80 -1960 80 "" 0 0 0 "">
  <-1650 20 -1630 20 "" 0 0 0 "">
  <-1730 20 -1710 20 "" 0 0 0 "">
  <-1730 20 -1730 60 "" 0 0 0 "">
  <-1730 60 -1630 60 "" 0 0 0 "">
  <-1630 20 -1600 20 "" 0 0 0 "">
  <-1630 20 -1630 60 "" 0 0 0 "">
  <-1900 20 -1730 20 "" 0 0 0 "">
  <-2050 80 -2050 200 "" 0 0 0 "">
  <-2050 200 -2010 200 "" 0 0 0 "">
  <-1950 200 -1920 200 "" 0 0 0 "">
  <-1860 200 -1830 200 "" 0 0 0 "">
  <-1900 80 -1830 80 "" 0 0 0 "">
  <-1830 80 -1830 200 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect -2182 882 582 301 3 #c0c0c0 1 00 1 1e+06 2e+06 3e+07 1 0 100 600 1 -1 0.5 1 315 0 225 "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
  </Rect>
  <Tab -2180 449 543 100 3 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"L1" #0000ff 0 3 0 0 0>
	<"C1" #0000ff 0 3 0 0 0>
	<"LCr1" #0000ff 0 3 0 0 0>
	<"Fr1" #0000ff 0 3 1 0 0>
  </Tab>
</Diagrams>
<Paintings>
</Paintings>
