clc;
clear all;
close all;

slew = 120;
shoulder = 90;
elbow = 145;

% lb = [-deg2rad(slew), 0, -deg2rad(elbow)];
% ub = deg2rad([0 shoulder 0]);

lb = [0, 0, 0];
ub = deg2rad([slew shoulder elbow]);
rng default
x0 = [0.1; 0.1; 0.1];
[x,res] = lsqnonlin(@function_xyz,x0,lb,ub)
rad2deg(x)