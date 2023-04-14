MIMO_data = readmatrix("bit_data.csv");

fanspeeds = MIMO_data(:, (1:3));
fanspeed_means = mean(fanspeeds, 1);
fanspeeds = fanspeeds - fanspeed_means;

ball_levels = MIMO_data(:, (5:7));
level_means = mean(ball_levels, 1);
ball_levels = ball_levels - level_means;

%time_samples = MIMO_data(:, 8);

%bit = iddata(ball_levels, fanspeeds,'SamplingInstants', time_samples);
bit = iddata(ball_levels, fanspeeds,'Ts',0.6);
bit.InputName  = {'Fan_4';'Fan_3';'Fan_2'};
bit.OutputName = {'Level_4';'Level_3';'Level_2'};

% nx = 1:10;
% % bit_ssest = ssest(bit, nx, 'Ts', 0.6)
% compare(bit_ssest, bit)

A = ones(n); B = ones(n); C = eye(n); D = zeros(n); K = zeros(n);
dt= 0.6;
n=3;
q0= zeros(n,2);

sys_initial = idss(A,B,C,D,K,q0(:,1),dt);
sys_initial.Structure.C.Free = false;

opt = ssestOptions('EnforceStability', true);

sys_ssest = ssest(bit, sys_initial, opt);

compare(sys_ssest, bit)
