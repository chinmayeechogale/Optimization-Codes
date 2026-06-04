clc; clear;

fun = @(X) X(1)^2 + X(2)^2 + 25*(sin(X(1))^2 + sin(X(2))^2);

% bounds
lb = [-2*pi , -2*pi];
ub = [2*pi , 2*pi];

% starting point
X0 = [0 0];
X  = X0;
F0 = fun(X);

% cooling settings
alpha = 0.80;
T_min = 0.10;
step_size = 0.50;

% estimate initial temperature from sampled worse moves
samples = [0 1; 0 2; 0 4];
deltas = zeros(size(samples,1),1);

for i = 1:size(samples,1)
    Fi = fun(samples(i,:));
    deltas(i) = Fi - F0;
end

deltas = deltas(deltas > 0);     % keep only worse moves
DeltaF_avg = mean(deltas);
p0 = 0.80;
T0 = -DeltaF_avg / log(p0);

T = T0;
iter = 0;
HIST = [];

while iter <= 10
    iter = iter + 1;

    % generate neighbor
    X_NEW = X + step_size*randn(1,2);

    % apply bounds
    X_NEW = min(max(X_NEW, lb), ub);

    F_NEW = fun(X_NEW);
    deltaF = F_NEW - F0;

    if deltaF<= 0
        P = 1;
    else
        P = 1/(1+exp(-deltaF/T));
    end

    if rand<P
        X = X_NEW;
        F0 = F_NEW;
    end

    HIST(iter,1) = iter;
    HIST(iter,2) = F0;
    HIST(iter,3) = T;
    HIST(iter,4) = X_NEW(1);
    HIST(iter,5) = X_NEW(2);

    T = alpha * T;
end

X_best = X;
F_best = F0;

plot(HIST(:,1), HIST(:,2), 'LineWidth', 1.5);
xlabel('Iteration');
ylabel('Objective value');
title('Simulated Annealing History');
grid on;