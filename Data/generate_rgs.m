clear;

N = 7200;
Nu = 1;
ch = 1;
Type = 'rgs';

Band_prbs = [0 1];
Range_prbs = [50 68];

Band2 = [0.01, 0.27];
Band3 = [0.01, 0.27];
Band4 = [0.01, 0.27];

Range4 = [50 61];
Range3 = [45 70];
Range2 = [55 66];
Range1 = [55 65];

U4 = idinput([N, ch, Nu], Type, Band4, Range4);
U3 = idinput([N, ch, Nu], Type, Band3, Range3);
U2 = idinput([N, ch, Nu], Type, Band2, Range2);
U1 = idinput([N, ch, Nu], Type, Band2, Range1);

U4 = cast(U4, 'int16');
U3 = cast(U3, 'int16');
U2 = cast(U2, 'int16');
U1 = cast(U1, 'int16');

step_table = array2table([U4, U3, U2, U1]);

step_table.Properties.VariableNames(1:4) = {
'T4 Fan Factor', 'T3 Fan Factor', 'T2 Fan Factor', 'T1 Fan Factor'
    };

writetable(step_table, 'rgs_signals_6.csv');

clc;