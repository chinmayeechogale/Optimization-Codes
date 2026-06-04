clc;
clear;
close all;

% Number of variables
nvars = 7;

% Bounds
lb = [2.6  0.7  17   7.3  7.3  2.9  5.0];
ub = [3.6  0.8  28   8.3  8.3  3.9  5.5];

% Penalized objective
fun = @(x) speedReducerPenalized(x);

% PSO options
options = optimoptions('particleswarm', ...
    'Display', 'iter', ...
    'SwarmSize', 50, ...
    'MaxIterations', 10, ...
    'FunctionTolerance', 1e-8, ...
    'UseVectorized', false);

% Run built-in PSO
[xbest, fbest, exitflag, output] = particleswarm(fun, nvars, lb, ub, options);

% Round x3 for reporting
xbest(3) = round(xbest(3));

function fpen = speedReducerPenalized(x)

    % Enforce integer-like variable
    x(3) = round(x(3));
    
    x1 = x(1); x2 = x(2); x3 = x(3);
    x4 = x(4); x5 = x(5); x6 = x(6); x7 = x(7);
    
    % Original objective
    f = 0.7854*x1*x2^2*(3.3333*x3^2 + 14.9334*x3 - 43.0934) ...
        - 1.508*x1*(x6^2 + x7^2) ...
        + 7.4777*(x6^3 + x7^3) ...
        + 0.7854*(x4*x6^2 + x5*x7^2);
    
    % Constraints g(x) <= 0
    g = zeros(11,1);
    g(1)  = 27/(x1*x2^2*x3) - 1;
    g(2)  = 397.5/(x1*x2^2*x3^2) - 1;
    g(3)  = 1.93*x4^3/(x2*x3*x6^4) - 1;
    g(4)  = 1.93*x5^3/(x2*x3*x7^4) - 1;
    g(5)  = sqrt((745*x4/(x2*x3))^2 + 16.9e6)/(110*x6^3) - 1;
    g(6)  = sqrt((745*x5/(x2*x3))^2 + 157.5e6)/(85*x7^3) - 1;
    g(7)  = x2*x3/40 - 1;
    g(8)  = 5*x2/x1 - 1;
    g(9)  = x1/(12*x2) - 1;
    g(10) = (1.5*x6 + 1.9)/x4 - 1;
    g(11) = (1.1*x7 + 1.9)/x5 - 1;
    
    % Total nonlinear constraint violation
    violation = sum(max(0,g));
    
    % Penalty parameter
    rho = 1e7;
    
    % Penalized objective
    fpen = f + rho*violation^2;

end