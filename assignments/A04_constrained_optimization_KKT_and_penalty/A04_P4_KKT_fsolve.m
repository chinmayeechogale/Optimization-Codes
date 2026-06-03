clc;
clear;

fun = @(z) [
    (4 + 29*z(3)/50)*z(1) + (2 + 2*z(3)/25)*z(2);
    (2 + 2*z(3)/25)*z(1) + (4 + 12*z(3)/25)*z(2);
    (29/100)*z(1)^2 + (2/25)*z(1)*z(2) + (6/25)*z(2)^2 - 1
];

starts = [
     1   1   -1
    -1  -1   -1
     1  -1   -1
    -1   1   -1
     2   1  -10
    -2  -1  -10
     2  -1   -4
    -2   1   -4
];

opts = optimoptions('fsolve','Display','off','FunctionTolerance',1e-12,...
    'StepTolerance',1e-12);

sols = [];

for k = 1:size(starts,1)
    [z,~,flag] = fsolve(fun, starts(k,:), opts);
    if flag > 0
        z = round(z,10);
        if isempty(sols)
            sols = z.';
        else
            dup = false;
            for j = 1:size(sols,2)
                if norm(z.' - sols(:,j)) < 1e-8
                    dup = true;
                    break;
                end
            end
            if ~dup
                sols(:,end+1) = z.';
            end
        end
    end
end

fprintf('Distinct solutions of the reduced system:\n');
for j = 1:size(sols,2)
    x1 = sols(1,j);
    x2 = sols(2,j);
    mu = sols(3,j);
    x3 = x1 + x2;
    f  = x1^2 + x2^2 + x3^2;

    lambda1 = mu;
    lambda2 = -(2 + lambda1/2)*x1;

    fprintf('\nSolution %d\n', j);
    fprintf('x1 = %.10f\n', x1);
    fprintf('x2 = %.10f\n', x2);
    fprintf('x3 = %.10f\n', x3);
    fprintf('mu = %.10f\n', mu);
    fprintf('lambda1 = %.10f\n', lambda1);
    fprintf('lambda2 = %.10f\n', lambda2);
    fprintf('f = %.10f\n', f);
end

% identify global minimum
bestf = inf;
bestx = [];

for j = 1:size(sols,2)
    x1 = sols(1,j);
    x2 = sols(2,j);
    x3 = x1 + x2;
    f  = x1^2 + x2^2 + x3^2;

    if f < bestf
        bestf = f;
        bestx = [x1; x2; x3];
    end
end

fprintf('\nGlobal minimum found:\n');
fprintf('x* = [%.10f, %.10f, %.10f]\n', bestx(1), bestx(2), bestx(3));
fprintf('f* = %.10f\n', bestf);