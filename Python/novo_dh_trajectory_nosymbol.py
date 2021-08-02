#!/usr/bin/python
# coding: utf8
'''
Programa teste para a criação das matrizes de transformação com os parâmetros de Denavit-Hartengberg

https://sajidnisar.github.io/posts/python_kinematics_dh#Evaluation-of-tip-position

@author: Lucas Vivian
'''

#nova versao com toda a junta 4 removida
#adicionado o offset do manipulador posicionado a mesa
#input dos angulos para calculo da fk deve ser exatamente igual ao colocado no peter corke - matlab

from math import *


#a ordem dos parametros na matriz é theta d alpha a

'''
PJ_DH = [[0, 0,      pi/2, 0.1075],
         [0, 0,      0   , 0.3155],
         [0, 0,      pi/2, -0.080],
         [0, 0,      0     , 0   ],
         [0, 0.4275, 0     , 0   ]]
'''

'''
x1 = 0.143
x2 = 0.44278
x4 = 0.49938
x5 = -0.11852
'''

x1 = 115.8;
x2 = 315;
x3 = 92;
x4 = 407;

#Parametros DH medidos do manipulador em mm


#matriz com novas medições para os parametros
PJ_DH = [[0, 0,      -pi/2, x1],
         [0, 0,      pi   , x2],
         [0, 0,      pi/2 , x3],
         [0, x4,     0   , 0 ]]

#print "\n\n", PJ_DH

R0 = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]

R1 = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]

R2 = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]

R3 = [[0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0]]

def prod_matrix(X, Y):
    #print "\n\n matriz x:", X
    #print "\n\n matriz y:", Y
    result = [[0,0,0,0],
              [0,0,0,0],
              [0,0,0,0],
              [0,0,0,0]]
    # iterate through rows of X
    for i in range(len(X)):
        # iterate through columns of Y
        for j in range(len(Y[0])):
            # iterate through rows of Y
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    #print "\n\n result:", result
    return result
    

def fowardk(theta1, theta2, theta3, theta4):
    #convert to radian
    #com offset inicial desconsiderado
    theta1 = radians(theta1) + (-pi/2)
    theta2 = radians(theta2) + (-pi/2)
    theta3 = radians(theta3) + (75*pi/180)
    #theta1 = radians(theta1)
    #theta2 = radians(theta2)
    #theta3 = radians(theta3)
    #global result
    global PJ_DH
    
    #matrizes do tipo 4x4

    '''
    M = [[cos(PJ_DH(i,1)),  -sin(PJ_DH(i,1))*cos(PJ_DH(i,3)),  sin(PJ_DH(i,1))*sin(PJ_DH(i,3)) ,  PJ_DH(i,4)*cos(PJ_DH(i,1))]
        [sin(PJ_DH(i,1)),  cos(PJ_DH(i,1))*cos(PJ_DH(i,3)) ,  -cos(PJ_DH(i,1))*sin(PJ_DH(i,3)),  PJ_DH(i,4)*sin(PJ_DH(i,1))]
        [0              ,  sin(PJ_DH(i,3))                 ,  cos(PJ_DH(i,3))                 ,  PJ_DH(i,2)                ]
        [0              ,  0                               ,  0                               ,  1                        ]]
    '''
    
    M1 = [[cos(theta1)   ,  -sin(theta1)*cos(PJ_DH[0][2]),  sin(theta1)*sin(PJ_DH[0][2])   , PJ_DH[0][3]*cos(theta1)],
    [sin(theta1)    ,  cos(theta1)*cos(PJ_DH[0][2]) ,  -cos(theta1)*sin(PJ_DH[0][2])  , PJ_DH[0][3]*sin(theta1)],
    [0              ,  sin(PJ_DH[0][2])             ,  cos(PJ_DH[0][2])               , PJ_DH[0][1]],
    [0              ,  0                            ,  0                              , 1                        ]]

    #print "\n\n", M1

    M2 = [[cos(theta2),  -sin(theta2)*cos(PJ_DH[1][2]),  sin(theta2)*sin(PJ_DH[1][2]),  PJ_DH[1][3]*cos(theta2)],
    [sin(theta2),  cos(theta2)*cos(PJ_DH[1][2]) ,  -cos(theta2)*sin(PJ_DH[1][2]),  PJ_DH[1][3]*sin(theta2)],
    [0              ,  sin(PJ_DH[1][2])                 ,  cos(PJ_DH[1][2])                 ,  PJ_DH[1][1]],
    [0              ,  0                               ,  0                               ,  1                        ]]

    #print "\n\n", M2

    M3 = [[cos(theta3),  -sin(theta3)*cos(PJ_DH[2][2]),  sin(theta3)*sin(PJ_DH[2][2]),  PJ_DH[2][3]*cos(theta3)],
    [sin(theta3),  cos(theta3)*cos(PJ_DH[2][2]) ,  -cos(theta3)*sin(PJ_DH[2][2]),  PJ_DH[2][3]*sin(theta3)],
    [0              ,  sin(PJ_DH[2][2])                 ,  cos(PJ_DH[2][2])                 ,  PJ_DH[2][1]],
    [0              ,  0                               ,  0                               ,  1                        ]]

    #print "\n\n", M3

    M4 = [[cos(theta4),  -sin(theta4)*cos(PJ_DH[3][2]),  sin(theta4)*sin(PJ_DH[3][2]),  PJ_DH[3][3]*cos(theta4)],
    [sin(theta4),  cos(theta4)*cos(PJ_DH[3][2]) ,  -cos(theta4)*sin(PJ_DH[3][2]),  PJ_DH[3][3]*sin(theta4)],
    [0              ,  sin(PJ_DH[3][2])                 ,  cos(PJ_DH[3][2])                 ,  PJ_DH[3][1]],
    [0              ,  0                               ,  0                               ,  1                        ]]

    #print "\n\n", M4
    
    matrixArray = [M1,M2,M3,M4]
    
    Mt1 = [[1,1,1,1],
           [1,1,1,1],
           [1,1,1,1],
           [1,1,1,1]]
    
    
    #R0 = prod_matrix(Mt1, Mt1) 
    
    R1 = prod_matrix(matrixArray[0],matrixArray[1])
    
    #print "\n\n R1: ", R1
    
    R2 = prod_matrix(R1,matrixArray[2])
    
    #print "\n\n R2: ", R2
    
    R3 = prod_matrix(R2,matrixArray[3])
    #print "\n\n R3: ", R3
    
    #print "\n\n R4: ", R4
    
    print "\n X:", round(R3[0][3],3), " Y: ", round(R3[1][3],3), " Z: ", round(R3[2][3],3)
    print "\n"
    
    #print R0
    
    #R1 = prod_matrix(R1,matrixArray[4])
    #R1 = prod_matrix(R1,matrixArray[5])
    
    #print "\n\n", R1
    
def main():
    
    fowardk(-60, 45, -50, 0)
    
if __name__ == '__main__':
    
    main()
        
