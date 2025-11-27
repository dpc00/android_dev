[type,fa1,s1,R1,c] = read_touchstone("C:\\projects\\sNp\\4mloop.s1p")
% a1 = s2a(s1,R)

figure;
plot(fa1,squeeze(abs(s1(1,1,:))));
hold on;
grid on;
ylim([0,1]);
legend('s11');


R2 = 1500;

LCR = 1e6;
F = 15e6;

C = 1/(2*pi*F*sqrt(LCR));
L = sqrt(LCR)/(2*pi*F);

printf("C = %e, L = %e\n",C,L);

span = .01e6;
cf = 15e6;
f1= cf - span/2;
f2 = cf + span/2;

% fa2 = linspace(f1,f2,201);
fa2 = fa1;

% capacitor
a1 = a_series(1./(2j*pi*fa2*C));
a2 = a_shunt(1./(2j*pi*fa2*C));

% inductor
a3 = a_series(2j*pi*fa2*L);
a4 = a_shunt(2j*pi*fa2*L);

% resistor
a5 = a_series(1/R2*ones(size(fa2)));
a6 = a_shunt(1/R2*ones(size(fa2)));


a7 = a_mul(a2, a4, a6);

s2 = a2s(a7);

figure;
plot(fa2,squeeze(abs(s2(1,1,:))));
hold on;
grid on;
plot(fa2,squeeze(abs(s2(2,1,:))),'r--');
ylim([0,1]);
legend('s11','s21');

write_touchstone('s',fa2,s2,"octave-lcr.s2p");

