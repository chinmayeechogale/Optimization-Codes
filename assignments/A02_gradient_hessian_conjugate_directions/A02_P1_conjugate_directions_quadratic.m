% A02_P1_conjugate_directions_quadratic.m
% Assignment 02 - Problem 1
% Gradient and Hessian computation for a quadratic function.
% Conjugate gradient direction search with optimal step size.
% Verifies that consecutive search directions are A-orthogonal (conjugate).
% Course: MEEN 683 | Texas A&M University

syms X1 X2
F = 1.5*X1^2 + 2*X1*X2 + 3*X2^2 + 2*X1 - 8*X2; % Given Function

i = 1;
STEPMAX = 2; % Maximum steps taken
X0 = [1; 1]; % Starting point

% Computing the Gradient and Hessian
gradF = gradient(F, [X1, X2]);
disp('The Gradient for given function is')
disp(gradF)

H = hessian(F, [X1, X2]);
disp('The Hessian for given function is')
disp(H)

% Creating a matrix to store direction vectors
S = [];

% Main Loop
while i <= STEPMAX
    disp('Iteration')
    disp(i)
    S(:,i) = -subs(gradF, [X1 X2], [X0(1), X0(2)]);
    disp('Direction Vector is')
    disp(S(:,i))

    HXi = subs(H, [X1 X2], [X0(1), X0(2)]);
    alphanum = S(:,i).' * S(:,i);
    alphadeno = S(:,i).' * HXi * S(:,i);
    alpha = alphanum/(alphanum > 0) / (alphadeno/(alphadeno > 0));
    disp('Optimal Step Size is')
    disp(alpha)

    X0 = X0 + alpha * S(:,i);
    disp('New location is')
    disp(X0)
    i = i + 1;
end

% Check orthogonality of direction vectors
for n = 1:STEPMAX-1
    ORTHO = dot(S(:,n), S(:,n+1));
    if ORTHO == 0
        disp('Direction Vectors are orthogonal')
    else
        disp('Direction Vectors are not orthogonal')
    end
end
