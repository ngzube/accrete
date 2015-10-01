% Import and plot final data from accrete5e run

eps = dlmread('eps.dat');
end_ = dlmread('end.dat');
follow = dlmread('follow.dat');
followgmt = dlmread('followgmt.dat');
% % "output.dat" is the collision data file read by accrete5e. Not needed
% % here.
% output = dlmread('output.dat', '', 1, 0);

% Plot eps data: tracking of one object
plot(eps(:,2)/10e6, eps(:,3))
title('Hf-W chronology of asteroids and terrestrial planets');
axis([0, 1.2*max(eps(:,2))/10e6, 0, 1.2*max(eps(:,3))]);
xlabel('Time (Myr)');
ylabel('\Delta\epsilon_W');
legend('k = 1', 'Location', 'Best');