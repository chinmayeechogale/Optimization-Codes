%% Assignment 4 - Problem 1
% Unconstrained formulation and global optimum for the canal problem
clear; clc;

% Reduced 2-variable objective (K is a positive constant, so set K = 1)
p = @(d,t) 100./d + d.*(1 + 3*t.^2)./(2*t);

% Further reduced 1-variable objective after minimizing over d analytically
h = @(t) 1./t + 3*t;

% Because h''(t)=2/t^3 > 0 for t>0, h is strictly convex.
% Also h(t)->inf as t->0+ and as t->inf, so the minimizer is global.
opts = optimset('TolX',1e-12,'Display','iter');
[t_star, h_star] = fminbnd(h, 1e-8, 100, opts);

% Recover the remaining variables
phi_star = 2*atan(t_star);      % radians
d_star = 10*sqrt(2*t_star/(1 + 3*t_star^2));
b_star = 100/d_star - d_star*(1 - t_star^2)/(2*t_star);
p_star = p(d_star, t_star);

fprintf('Global optimum for reduced problem:\n');
fprintf('t*   = %.4f\n', t_star);
fprintf('phi* = %.4f rad = %.4f deg\n', phi_star, phi_star*180/pi);
fprintf('d*   = %.4f ft\n', d_star);
fprintf('b*   = %.4f ft\n', b_star);
fprintf('p*   = %.4f\n', p_star);

% Compare against exact solution
tex = 1/sqrt(3);
phiex = pi/3;
dex = 10/(3^(1/4));
bex = 20/(3^(3/4));
pex = 20*(3^(1/4));

fprintf('\nExact solution:\n');
fprintf('t*   = %.4f\n', tex);
fprintf('phi* = %.4f rad = %.4f deg\n', phiex, phiex*180/pi);
fprintf('d*   = %.4f ft\n', dex);
fprintf('b*   = %.4f ft\n', bex);
fprintf('p*   = %.4f\n', pex);

% Optional: verify with the original 2-variable unconstrained problem
f = @(x) 100/x(1) + x(1)*(1 + 3*x(2)^2)/(2*x(2));   % x = [d,t]

starts = [
    2    0.2
    5    0.5
    8    1.0
    12   2.0
    20   5.0
];

bestf = inf;
bestx = [NaN NaN];
options = optimset('Display','off','TolX',1e-12,'TolFun',1e-12);
for k = 1:size(starts,1)
    [xk, fk] = fminsearch(@(x) penalized_obj(x,f), starts(k,:), options);
    if fk < bestf
        bestf = fk;
        bestx = xk;
    end
end

fprintf('\nMulti-start check on (d,t):\n');
fprintf('d    = %.12f\n', bestx(1));
fprintf('t    = %.12f\n', bestx(2));
fprintf('p    = %.12f\n', bestf);

function val = penalized_obj(x,f)
    d = x(1); t = x(2);
    if d <= 0 || t <= 0 || ~isfinite(d) || ~isfinite(t)
        val = 1e12;
    else
        val = f(x);
    end
end