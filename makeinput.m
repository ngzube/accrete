% Script to create an input file for accrete5e.

% Accepts input from a window and prints a txt file to be used by
% accrete5e.

prompt = {'nprov: UNKNOWN. for loop max. 1 indicates chondritic?', ...
    'ff, Equilibration fraction (0 = complete, 1 = none)', ...
    'tstop: The time code will stop', ...
    'iray: toggle between Raymond or OBrien input', ...
    'ilog: plotting toggle', ...
    'idsc: UNKNOWN', ...
    'ixmix: sets imix to control mixing/re-equilibration', ...
    'xmix: min mass required for a "large" impact', ...
    'xratc: used in mixing with IF XRAT >= XRATC, IBIG = 1, ICIRC++', ...
    'ifol: ID of particle to be followed', ...
    'dw: tungsten partition coefficient. DW = -F2(1-Y) / (F1*Y)', ...
    'tscale: allows timescale to be artificially stretched', ...
    'kmax: # of time steps', ...
    'kstep: variable used in MOD(k,kstep) to occationally write', ...
    'dt: timestep in yrs', ...
    'ypmx: plotting y-axis'}; 
variable_names = {'nprov','ff','tstop','iray','ilog','idsc','ixmix', ...
    'xmix','xratc','ifol','dw','tscale','kmax','kstep','dt', ...
    'ypmx'};
dlg_title = 'accrete5e Input';
num_lines = 1;
default_fig20 = {'6','0.','1.5e8','1','1','100','1', ...
    '100.','0.7','38','0.034','1.','20000','100','2.5e5', ...
    '20.'};
options.Interpreter = 'tex';
answer = inputdlg(prompt,dlg_title,num_lines,default_fig20,options);


% Create string of the responses to be written to .inp file
inp = char(answer);
outp = [''];
singlerow = [''];

for i = 1:size(inp,1)
    for j = 1:size(inp,2)
        if(inp(i,j) ~= ' ')
            singlerow = [singlerow,inp(i,j)];
        end
    end
        outp = [outp,char(variable_names(i)),'=',singlerow,','];
        singlerow = [''];
end

outpfin = sprintf(' &inp\n%s\n&end',outp);
dlmwrite('accrete4.inp',outpfin,'delimiter','');

