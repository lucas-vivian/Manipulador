%Programa para calcular o workspace do manipulador ARM 5E Mini e aplicar
%cinemática direta com interface

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

%Definindo os elos do manipulador para o Toolbox PeterCorke com offset
%inicial da mesa
L11=Link([PJ_DH1(1,:) 0 -pi/2]);  %slew 120 - totalmente dobrado %offset pi/2 
L12=Link([PJ_DH1(2,:) 0 -pi/2]);  %shoulder 90 - totalmente virado p/ dir %offset pi/2
L13=Link([PJ_DH1(3,:) 0 -75*pi/180]); %elbow 145 - totalmente fechado 145 graus
L14=Link([PJ_DH1(4,:) 0 0]);

%Definindo limite dos ângulos das juntas
L11.qlim = [0 theta_slew*pi/180] %slew começando alinhado permite 90 para a esq e 30 para dir
L12.qlim = [0 theta_shoulder*pi/180]
L13.qlim = [0 theta_elbow*pi/180] %shoulder começando alinhado permite 70 para dentro e 75 para fora

SL1=SerialLink([L11 L12 L13 L14],'name', 'ARM 5E');

%Parâmetros plot workspsace
s=30;
plot1 = scatter3(xM(:),yM(:),zM(:),s,zM(:),'filled')

% Comando para deixar gráfico translúcido
%plot1.MarkerFaceAlpha = .1;
%plot1.MarkerEdgeAlpha = .1;

%Plot teach do SerialLink
SL1.teach()
SL1.plot(zeros(4))
grid on;
title('Workspace ARM 5E Mini');
xlabel('x (mm)');
ylabel('y (mm)');
zlabel('z (mm)');
colormap;
