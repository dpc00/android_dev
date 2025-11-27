C = 30e-12;
L = 23e-6
R = 50

f = linspace(1e6,30e6,501);

% 100pf series capacitor
a = a_series(1./(2j*pi*f*C));

% 20nH series inductor
a = a_mul(a, a_series(2j*pi*f*L));

% 50 ohm shunt resistor
a = a_mul(a, a_shunt(1/R*ones(size(f))));


s = a2s(a)

figure
plot(f,20*log10(squeeze(abs(s(1,1,:)))));
hold on;
grid on;
plot(f,20*log10(squeeze(abs(s(2,1,:)))),'r--');
ylim([-50 0]);
legend('s11','s21');

write_touchstone('s',f,s,"test.s2p")


