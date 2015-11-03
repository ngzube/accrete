%% Import and plot final data from accrete5e run

% General example
eps = dlmread('eps.dat');
end_ = dlmread('end.dat');
follow = dlmread('follow.dat');
%followgmt = dlmread('followgmt.dat');
% "output.dat" is the collision data file read by accrete5e. Not needed.
%output = dlmread('output.dat', '', 1, 0);
%kval = load('accrete4.inp') % .inp files cannot be read

%% Plot tungsten anomaly

% General example
figure(1);
x = eps(:,2)/1e6;
y = eps(:,3);
plot(x,y)
title('Tungsten anomaly vs. time');
%axis([0, max(x), 0, 1.2*max(y)]);
axis([0, 150, -1, 20]);
xlabel('Time (Myr)');
ylabel('\Delta\epsilon_W');
legend('k = 1', 'Location', 'Best');
print('Wanomaly','-dpng')

%% Plot mass vs. time

% General example
figure(2);
x = follow(:,1)/1e6;
%y = follow(:,3);
y = log10(follow(:,3));
stairs(x,y)
hold on
xax = 0:max(x);
yax = xax*0 + 1;
plot(xax,yax,'--')
hold off
title('Mass vs. time');
%axis([0, 1.2*max(x), 0, 1.2*max(y)]);
axis([0, 150, -1, 0.5]);
xlabel('Time (Myr)');
ylabel('Log_{10}(mass, M_E)');
legend('"target" (proto-Earth)', 'Location', 'Best');
print('Mass','-dpng')
