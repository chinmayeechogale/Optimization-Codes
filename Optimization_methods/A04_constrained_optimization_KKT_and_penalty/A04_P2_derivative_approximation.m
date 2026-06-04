clear; clc; close all;

% Step sizes (log spaced)
dx = logspace(-15,1,200);

x = 1;

% ==============================
% FUNCTIONS
% ==============================
funcs = {@(x) x.^2, @(x) x.^3, @(x) exp(x)};
names = {'x^2','x^3','exp(x)'};

% Exact derivatives at x=1
df_exact = [2, 3, exp(1)];
d2f_exact = [2, 6, exp(1)];

for k = 1:3
    
    f = funcs{k};
    
    err_fd  = zeros(size(dx));
    err_cd  = zeros(size(dx));
    err_cs  = zeros(size(dx));
    
    err_cd2 = zeros(size(dx));
    err_cs2 = zeros(size(dx));
    
    for i = 1:length(dx)
        h = dx(i);
        
        % ==========================
        % First Derivative
        % ==========================
        
        % Forward Difference
        fd = (f(x+h) - f(x)) / h;
        
        % Central Difference
        cd = (f(x+h) - f(x-h)) / (2*h);
        
        % Complex Step
        cs = imag(f(x + 1i*h)) / h;
        
        % Errors
        err_fd(i) = abs(fd - df_exact(k));
        err_cd(i) = abs(cd - df_exact(k));
        err_cs(i) = abs(cs - df_exact(k));
        
        % ==========================
        % Second Derivative
        % ==========================
        
        % Central Difference
        cd2 = (f(x+h) - 2*f(x) + f(x-h)) / h^2;
        
        % Complex Step (given formula)
        cs2 = (2/h^2) * (f(x) - real(f(x + 1i*h)));
        
        % Errors
        err_cd2(i) = abs(cd2 - d2f_exact(k));
        err_cs2(i) = abs(cs2 - d2f_exact(k));
    end
    
    % ==============================
    % PLOTS
    % ==============================
    
    figure;
    loglog(dx, err_fd, 'r', 'LineWidth', 1.5); hold on;
    loglog(dx, err_cd, 'b', 'LineWidth', 1.5);
    loglog(dx, err_cs, 'k', 'LineWidth', 1.5);
    
    grid on;
    xlabel('\Delta x');
    ylabel('Error');
    title(['First Derivative Error - f(x) = ', names{k}]);
    legend('Forward Diff','Central Diff','Complex Step','Location','best');
    
    
    figure;
    loglog(dx, err_cd2, 'b', 'LineWidth', 1.5); hold on;
    loglog(dx, err_cs2, 'k', 'LineWidth', 1.5);
    
    grid on;
    xlabel('\Delta x');
    ylabel('Error');
    title(['Second Derivative Error - f(x) = ', names{k}]);
    legend('Central Diff','Complex Step','Location','best');
    
end