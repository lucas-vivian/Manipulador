%Programa para calcular o workspace do manipulador ARM 5E Mini

clc; clear; close all;

%Declaração dos ângulos máximos das juntas em graus
theta_slew = 120;
theta_shoulder = 90;
theta_elbow = 145;

%Parametros DH ARM 5E Mini medidos em mm
a1 = 115.8;
a2 = 315;
a3 = 92;
d4 = 407;
      
%Tabela DH
%Ordem parametros (theta d a alpha)
PJ_DH1 = [0 0        a1    -pi/2;
          0 0        a2    pi;
          0 0        a3    pi/2; 
          0 d4       0     0];

%linspace com offset do manipulador na mesa
t1=(linspace(0,theta_slew,50)*pi/180)-pi/2;
t2=(linspace(0,theta_shoulder,50)*pi/180)-pi/2;
t3=(linspace(0,theta_elbow,50)*pi/180)-75*pi/180;

%Criando matrizes 90x90x90 para cada variável
[T1,T2,T3]=ndgrid(t1,t2,t3);

%Definição das equações de posicionamento
xM = cos(T1).*(a1 + a3*cos(T2 - T3) - d4*sin(T2 - T3) + a2*cos(T2));
yM = sin(T1).*(a1 + a3*cos(T2 - T3) - d4*sin(T2 - T3) + a2*cos(T2));
zM = -a3*sin(T2 - T3) - d4*cos(T2 - T3) - a2*sin(T2);

%Parâmetros plot workspsace
s=30;
plot1 = scatter3(xM(:),yM(:),zM(:),s,zM(:),'filled')

%Comando para deixar gráfico translúcido
%plot1.MarkerFaceAlpha = .2;
%plot1.MarkerEdgeAlpha = .2;

grid on;
title('Workspace ARM 5E Mini');
xlabel('x (mm)');
ylabel('y (mm)');
zlabel('z (mm)');
colormap;