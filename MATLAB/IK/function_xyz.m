%funcao a ser utilizada no fmincon

function F = function_xyz(t)

%parametros denavit
a1 = 115.8;
a2 = 315;
a3 = 92;
d4 = 407;

%Usando de exemplo a posicao com todas as juntas zeradas do toolbox do
%peter corke
% x = 35.752;
% y = -35.752;
% z = 80.048;

x = 252.073;
y = -692.564;
z = 98.913;

%Colocando offset no angulo das juntas
t(1) = t(1) - pi/2;
t(2) = t(2) - pi/2;
t(3) = t(3) - 75*pi/180;

F(1) = cos(t(1))*(a1 + a3*cos(t(2) - t(3)) - d4*sin(t(2) - t(3)) + a2*cos(t(2))) - x;
F(2) = sin(t(1))*(a1 + a3*cos(t(2) - t(3)) - d4*sin(t(2) - t(3)) + a2*cos(t(2))) - y;
F(3) = - d4*cos(t(2) - t(3)) - a3*sin(t(2) - t(3)) - a2*sin(t(2)) - z;

% %Colocar as variaveis antes da equação fez a otimização ficar mais próxma
% %de zero
% F(1) = x - cos(t(1))*(a1 + a3*cos(t(2) + t(3)) - d4*sin(t(2) + t(3)) + a2*cos(t(2)));
% F(2) = y - sin(t(1))*(a1 + a3*cos(t(2) + t(3)) - d4*sin(t(2) + t(3)) + a2*cos(t(2)));
% F(3) = z - d4*cos(t(2) + t(3)) + a3*sin(t(2) + t(3)) + a2*sin(t(2));

end
