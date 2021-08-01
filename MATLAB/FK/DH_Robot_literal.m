clc
clear all
close all

%syms t1 t2 t3  d3 t4 t5 t6 l1 l2 l3;
%syms a1 a2 a3 d4 t1 t2 t3
syms t1 t2 t3 t4 d1 d2 d3 d4 alpha1 alpha2 alpha3 alpha4 a1 a2 a3 a4;

display('Denavit-Hartenberg: ')
display('Tabela de parâmetros(theta d alpha a): ');

% PJ_DH =  [t1 0       -pi/2  a1;
%           t2 0       pi     a2;
%           t3 0       pi/2 a3;
%           0  d4      0     0];   
      
%PJ_DH =  [t1 d1      alpha1  a1;
%          t2 d2      alpha2  a2;
%          t3 d3      alpha3  a3;
%          t4 d4      alpha4  a4]; 
      
PJ_DH =  [t1 d1      alpha1  a1;
          t2 d2      alpha2  a2]; 
      
% Matrizes de transformação Ti-1->i
[Mt Mi] = MGD_DH(PJ_DH);

display('Matrizes de Transformação: ');
T01 = Mi(:,:,1)
T12 = Mi(:,:,2)
%T23 = Mi(:,:,3)
%T34 = Mi(:,:,4)
 
T02 = simplify(Mt)
 