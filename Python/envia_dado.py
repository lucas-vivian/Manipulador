#!/usr/bin/python
# coding: utf8
'''
Programa de teste para as demandas - teste atual: demanda de posicao

@author: Lucas Vivian
'''

import serial
from struct import pack
from dh_trajectory_nosymbol import *

porta='/dev/ttyUSB0'
baud_rate=115200
Obj_porta=serial.Serial(porta,baud_rate)

#byte de inicio da mensagem
Start_byte = 0xE7

#3 bytes de aquisicao dos sensores
Master_T = 0x00
Master_V = 0x00
Master_C = 0x00
#não é preenchido para o envio

#9 bytes por motor para motor data
#Exemplo para motor 1

demand_prefix = 0x00 # Motor data: demand, PID or sensors
pid_prefix = 0x01
sensor_prefix = 0x01

demand_stop = 0x00
demand_volt_CW = 0x01 # Demand type: Stop (0), Voltage CW (1), Voltage CCW (2), Speed CW (3), Speed CCW (4), Position (5)
demand_volt_CCW = 0x02
demand_speed_CW = 0x03
demand_speed_CCW = 0x04
demand_pos = 0x05

msb_voltage = 0x7F 
lsb_voltage = 0xFF #demanda de 4095 de 65535

msb_zero = 0x00
lsb_zero = 0x00

msb_speed_lim = 0x03
lsb_speed_lim = 0xFF #velocidade limitada a 1/4 da limitação máxima

msb_cur_lim = 0x07
lsb_cur_lim = 0xFF #corrente limitada a 1/4 da limitação máxima

motor_data = 0x00

#byte de checksum
    #fazer com overflow ja que o checksum so possui 8 bits
#chksum = 0x00

#byte de end of message
End_byte = 0xE5

def create_msg():
    msg = [Start_byte,
           Master_T,
           Master_V,
           Master_C,
           demand_prefix, #inicio do bloco SHOULDER
           demand_stop,
           msb_zero,
           lsb_zero,
           #demand_stop, #byte 5
           #msb_zero,
           #lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix, #SLEW
           #demand_volt_CW,
           #msb_voltage,
           #lsb_voltage,
           demand_stop, #byte 14
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix, #ELBOW
           demand_stop, #byte 23
           msb_zero,
           lsb_zero,
           #demand_volt_CW,
           #msb_voltage,
           #lsb_voltage,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix, #JAW ROTATE
           #demand_volt_CW,
           #msb_voltage,
           #lsb_voltage,
           demand_stop,
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data,
           demand_prefix, #JAW OPENING/CLOSE
           #demand_volt_CW, #(opening)
           #demand_volt_CCW,
           #msb_voltage,
           #lsb_voltage,
           demand_stop,
           msb_zero,
           lsb_zero,
           msb_speed_lim,
           lsb_speed_lim,
           msb_cur_lim,
           lsb_cur_lim,
           motor_data]
    #final_msg = complete_msg(msg)
    return msg
    
def checksum(msg_inc):
    chksum = 0x00
    for i in range(0,48):
          chksum += msg_inc[i]
    chksum = chksum % 256
    msg_inc.append(chksum)
    msg_inc.append(End_byte)
    return msg_inc

def send_msg(msg_final):
    #msg_final = create_msg() 
    print(msg_final)
    print('\n')
    print(type(msg_final))
    msg_empacotada = pack('<{}B'.format(len(msg_final)), *msg_final)
    print("\nEnviando mensagem ...")
    Obj_porta.write(msg_empacotada)
    print("\nMensagem enviada")
    
flag_rec = False
resp = 's'

def demanda_motor(): #Depois do "metodo" das perguntas, utilizar o parser
    #global flag_rec
    #if not flag_rec:
    global resp
    msg1 = create_msg()
    angs = [0,0,0,0,0]
    while resp != 'n' :
        motor_num = raw_input("\nQual motor deseja movimentar? (1-Shoulder, 2-Slew, 3-Elbow, 4-Jaw Rotate, 5-Jaw O/C) ")
        motor_num = int(motor_num)
        motor_change = 9*(int(motor_num)-1) + 5
        demand = raw_input("\nQual sera a demanda? (5-Posição) ")
        msg1[motor_change] = int(demand) #0x05 = 5?
        if demand == '5':
            ang = raw_input("\nQual o angulo desejado? ")
            ang = int(ang)
            angs[motor_num - 1] = ang
            #print(ang)
        #converter o angulo desejado em posicao
        pos = 0
        #print type(motor_num)
        if motor_num == 1:
            pos = (20200*ang)/90
            #print "posicao shoulder", pos
        elif motor_num == 2:
            pos = (20200*ang)/120
        elif motor_num == 3:
            pos = (20320*ang)/145
        elif motor_num == 4:
            pos = (1770*ang)/360
        #print "posicao", pos
        lsb = pos & 0xFF
        #print "lsb", lsb
        pos >>=8
        msb = pos
        msg1[motor_change+1] = msb
        msg1[motor_change+2] = lsb
        #print msb, lsb
        resp = raw_input("\nDeseja movimentar algum outro motor? (s ou n) ") #podemos fazer um while
    #if resp == 's':
    #    flag_rec = True
    #    demanda_motor()
    #else:
    subs_msg = checksum(msg1)
    while(1):
        print angs[0], " ",  angs[1], " ", angs[2]
        fowardk(angs[1],angs[0],angs[2],angs[3],angs[4])
        send_msg(subs_msg)
    
def zero():
    msg_zero = [Start_byte,
                Master_T,
                Master_V,
                Master_C,
                demand_prefix, #inicio do bloco SHOULDER
                demand_pos,
                msb_zero,
                lsb_zero,
                msb_speed_lim,
                lsb_speed_lim,
                msb_cur_lim,
                lsb_cur_lim,
                motor_data,
                demand_prefix, #SLEW
                demand_pos, #byte 14
                msb_zero,
                lsb_zero,
                msb_speed_lim,
                lsb_speed_lim,
                msb_cur_lim,
                lsb_cur_lim,
                motor_data,
                demand_prefix, #ELBOW
                demand_pos, #byte 23
                msb_zero,
                lsb_zero,
                msb_speed_lim,
                lsb_speed_lim,
                msb_cur_lim,
                lsb_cur_lim,
                motor_data,
                demand_prefix, #JAW ROTATE
                demand_stop,
                msb_zero,
                lsb_zero,
                msb_speed_lim,
                lsb_speed_lim,
                msb_cur_lim,
                lsb_cur_lim,
                motor_data,
                demand_prefix, #JAW OPENING/CLOSE,
                demand_stop,
                msb_zero,
                lsb_zero,
                msb_speed_lim,
                lsb_speed_lim,
                msb_cur_lim,
                lsb_cur_lim,
                motor_data]
    chksum = 0x00
    for i in range(0,48):
          chksum += msg_zero[i]
    chksum = chksum % 256
    msg_zero.append(chksum)
    msg_zero.append(End_byte)
    return msg_zero

def main():
    #send_msg()
    demanda_motor()
    '''
    while(1):
        comand = raw_input("Que ação deseja realizar? ")
        if comand == 'zero':
            while(1):
                msg2 = zero()  
                send_msg(msg2)
        elif comand == 'mover':
            cont = 0
            while (cont < 3000):
                msg = create_msg()
                msg = checksum(msg)
                send_msg(msg)
                cont += 1
    #while(1):
    #    send_msg()
    '''    
    

if __name__ == '__main__':
    main()
