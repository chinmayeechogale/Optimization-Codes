clc; clear;
syms X1 X2 M1 M2 M3 real

F = (X1-1)^2 + (X2-1)^2;
G1 = X1 + X2 - 1;
G2 = -X1;
G3 = -X2;

L = F + M1*G1 + M2*G2 + M3*G3;

GRAD_L_X1 = diff(L,X1) == 0;
GRAD_L_X2 = diff(L,X2) == 0;

disp('Case 1: G1 active, G2 and G3 inactive')
S1 = solve([GRAD_L_X1, GRAD_L_X2, G1==0, M2==0, M3==0], [X1, X2, M1, M2, M3]);
disp(S1)
if ~isempty(S1.X1) && isAlways(S1.M1 >= 0) && isAlways(S1.X1 > 0) && isAlways(S1.X2 > 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end

disp('Case 2: G1 and G2 active, G3 inactive')
S2 = solve([GRAD_L_X1, GRAD_L_X2, G1==0, G2==0, M3==0], [X1, X2, M1, M2, M3]);
disp(S2)
if ~isempty(S2.X1) && isAlways(S2.M1 >= 0) && isAlways(S2.M2 >= 0) && isAlways(S2.X2 > 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end

disp('Case 3: G1 and G3 active, G2 inactive')
S3 = solve([GRAD_L_X1, GRAD_L_X2, G1==0, G3==0, M2==0], [X1, X2, M1, M2, M3]);
disp(S3)
if ~isempty(S3.X1) && isAlways(S3.M1 >= 0) && isAlways(S3.M3 >= 0) && isAlways(S3.X1 > 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end

disp('Case 4: G2 and G3 active, G1 inactive')
S4 = solve([GRAD_L_X1, GRAD_L_X2, G2==0, G3==0, M1==0], [X1, X2, M1, M2, M3]);
disp(S4)
if ~isempty(S4.X1) && isAlways(S4.M2 >= 0) && isAlways(S4.M3 >= 0) ...
        && isAlways(subs(G1,[X1 X2],[S4.X1 S4.X2]) < 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end

disp('Case 5: G2 active, G1 and G3 inactive')
S5 = solve([GRAD_L_X1, GRAD_L_X2, G2==0, M1==0, M3==0], [X1, X2, M1, M2, M3]);
disp(S5)
if ~isempty(S5.X1) && isAlways(S5.M2 >= 0) ...
        && isAlways(subs(G1,[X1 X2],[S5.X1 S5.X2]) < 0) ...
        && isAlways(S5.X2 > 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end

disp('Case 6: G3 active, G1 and G2 inactive')
S6 = solve([GRAD_L_X1, GRAD_L_X2, G3==0, M1==0, M2==0], [X1, X2, M1, M2, M3]);
disp(S6)
if ~isempty(S6.X1) && isAlways(S6.M3 >= 0) ...
        && isAlways(subs(G1,[X1 X2],[S6.X1 S6.X2]) < 0) ...
        && isAlways(S6.X1 > 0)
    disp('Valid KKT')
else
    disp('Invalid KKT')
end