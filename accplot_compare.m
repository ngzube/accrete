%% Import and plot final data from accrete5e run
% Used with specific dataset

eps38_1 = dlmread('eps17.dat');
%eps38_0 = dlmread('eps23.dat');
% Collision at time = 77746960; 35 is then absorbed
%eps35_0 = dlmread('eps17.dat');
eps35_1 = dlmread('eps23.dat');

mass38_1 = dlmread('follow17.dat');
mass35_1 = dlmread('follow23.dat');

%% Plot tungsten anomaly

endt = 542; % last cell of 35 before collision with 38
figure(1);
x1 = eps38_1(:,2)/1e6;
y1 = eps38_1(:,3);
x2 = eps35_1(:,2)/1e6;
y2 = eps35_1(:,3);
% x3 = eps38_0(1:endt,2)/1e6;
% y3 = eps38_0(1:endt,3);
% x4 = eps35_0(1:endt,2)/1e6;
% y4 = eps35_0(1:endt,3);
plot(x1,y1,x2,y2)
title('Tungsten anomaly vs. time');
axis([0, 100, -1, 15]);
%max([max(x1), max(x2)])
xlabel('Time (Myr)');
ylabel('\Delta\epsilon_W');
legend('17 (k=1)','23 (k=1)','Location', 'Best');
legend('boxoff');
print('Wanomly','-dpng')

%% Plot mass vs. time

endt = 7; % last cell of 35 before collision with 38
figure(2);
x1 = mass38_1(:,1)/1e6;
y1 = log10(mass38_1(:,6));

%x1(size(x1,1)+1) = 150;
%y1(size(y1,1)+1) = y1(size(y1,1));

x2 = mass35_1(:,1)/1e6;
y2 = log10(mass35_1(:,6));
%x2 = mass35_1(1:endt,1)/1e6;
%y2 = log10(mass35_1(1:endt,6));
stairs(x1,y1)
hold on
stairs(x2,y2,'--')
hold off
title('Mass vs. time');
%axis([0, 1.2*max(x), 0, 1.2*max(y)]);
axis([0, 100, -1.0, 0.5]);
xlabel('Time (Myr)');
ylabel('Log_{10}(mass, M_E)');
legend('17','23','Location', 'Northeast');
legend('boxoff');
print('Mass','-dpng')
