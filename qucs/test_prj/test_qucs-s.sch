<Qucs Schematic 0.0.22>
<Properties>
  <View=-43,0,1182,994,1,0,105>
  <Grid=10,10,1>
  <DataSet=test_qucs-s.dat>
  <DataDisplay=test_qucs-s.dpl>
  <OpenDisplay=0>
  <Script=test_qucs-s.m>
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
  <R R1 1 660 250 -134 -26 0 3 "50 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <SPICE X1 1 470 180 -26 -77 0 0 "C:/projects/python-win-rf/temp.cir" 1 "_netp1,_netp2" 0 "no" 0 "none" 0>
  <Vac V1 1 270 260 18 -26 0 1 "1 V" 1 "1 GHz" 0 "0" 0 "0" 0>
  <GND * 1 660 280 0 0 0 0>
  <GND * 1 470 210 0 0 0 0>
  <GND * 1 270 290 0 0 0 0>
  <.AC AC1 1 920 130 0 52 0 0 "lin" 1 "1 MHz" 1 "30 MHz" 1 "101" 1 "no" 0>
  <R R2 1 340 180 -26 15 0 0 "50 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
</Components>
<Wires>
  <500 180 660 180 "" 0 0 0 "">
  <660 180 660 220 "" 0 0 0 "">
  <270 180 310 180 "" 0 0 0 "">
  <270 180 270 230 "" 0 0 0 "">
  <370 180 440 180 "V1" 320 70 19 "">
  <660 180 660 180 "V2" 690 70 0 "">
</Wires>
<Diagrams>
  <Rect 98 852 731 511 3 #c0c0c0 1 00 1 1e+06 2e+06 3e+07 1 -0.1 0.1 1.1 1 -1 0.2 1 315 0 225 "" "" "">
	<"ngspice/ac.v(v1)" #0000ff 0 3 0 0 0>
	<"ngspice/ac.v(v2)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
