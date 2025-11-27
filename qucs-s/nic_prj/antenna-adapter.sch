<Qucs Schematic 0.0.22>
<Properties>
  <View=58,-194,971,598,1.00253,0,0>
  <Grid=10,10,1>
  <DataSet=antenna-adapter.dat>
  <DataDisplay=antenna-adapter.dpl>
  <OpenDisplay=1>
  <Script=>
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
  <GND * 1 560 70 0 0 0 0>
  <GND * 1 150 0 0 0 0 3>
  <GND * 1 410 60 0 0 0 1>
  <Vac V1 1 180 0 -26 18 0 0 "1 mV" 0 "1 GHz" 0 "0" 0 "0" 0>
  <.AC AC1 1 710 90 0 52 0 0 "log" 1 "1 MHz" 1 "30 MHz" 1 "30" 1 "no" 0>
  <SPICE X1 1 490 0 -26 -77 0 0 "C:/projects/python-win-rf/temp.cir" 0 "_netp1,_netp2" 0 "no" 0 "none" 0>
  <GND * 1 490 30 0 0 0 0>
  <Sub S11_Probe1 1 340 -110 -40 34 0 0 "S11_Probe.sch" 0 "{Z0}" 1>
  <Sub S12_Probe1 1 620 -110 -40 34 0 0 "S12_Probe.sch" 0 "{Z0}" 1>
  <L L1 1 210 60 -36 65 0 0 "{L1}" 1 "" 0>
  <R R1 5 560 40 15 -26 0 1 "{Z0}" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R R2 5 240 0 -26 15 0 0 "{Z0}" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <.DC DC1 1 710 -10 0 54 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <Eqn Eqn3 1 360 250 -47 20 0 0 "Z0=50" 1 "yes" 0>
  <Sub SUB1 5 340 30 -12 -89 0 0 "FloatLNic.sch" 0>
  <C C1 1 210 100 -32 89 0 0 "18 pF" 1 "" 0 "neutral" 0>
  <Eqn Eqn2 1 360 140 -47 20 0 0 "L1=34e-6" 1 "5e-6" 0>
  <GND * 1 110 90 0 0 0 0>
</Components>
<Wires>
  <520 0 560 0 "" 0 0 0 "">
  <560 0 560 10 "" 0 0 0 "">
  <370 0 460 0 "" 0 0 0 "">
  <270 0 280 0 "" 0 0 0 "">
  <370 60 410 60 "" 0 0 0 "">
  <240 60 310 60 "" 0 0 0 "">
  <560 -90 560 0 "" 0 0 0 "">
  <280 0 310 0 "" 0 0 0 "">
  <280 -90 280 0 "" 0 0 0 "">
  <180 60 180 100 "" 0 0 0 "">
  <240 60 240 100 "" 0 0 0 "">
  <110 60 180 60 "" 0 0 0 "">
  <110 60 110 90 "" 0 0 0 "">
  <400 -90 400 -90 "nS11" 440 -150 0 "">
  <680 -90 680 -90 "nS12" 720 -150 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
